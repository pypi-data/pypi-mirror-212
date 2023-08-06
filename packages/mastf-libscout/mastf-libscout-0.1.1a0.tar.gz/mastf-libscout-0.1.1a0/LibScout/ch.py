# Copyright (c) 2015-2017  Erik Derr [derr@cs.uni-saarland.de]
# Copyright (c) 2023 MatrixEditor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import re
import lief

from LibScout.config import FW_TYPES
from LibScout.pkg.tree import PackageTree
from LibScout.pkg.utils import normalize_name, to_packages, internal_name


TYPE_DESCRIPTOR = {
    "void": "V",
    "bool": "Z",  # LIEF returns bool
    "byte": "B",
    "short": "S",
    "char": "C",
    "int": "I",
    "long": "J",
    "float": "F",
    "double": "D",
}


def is_inner_class(class_name: str) -> bool:
    """Checks if a class is an inner class.

    >>> is_inner_class("Lcom/example/R$1;")
    True

    :param class_name: Name of the class.
    :return: True if the class is an inner class, False otherwise.
    """
    return "$" in class_name


def is_resource_class(class_name: str) -> bool:
    """Checks if a class is a resource class.

    >>> is_resource_class("ABC")
    False
    >>> is_resource_class("BuildConfig")
    True

    :param class_name: Name of the class.
    :return: True if the class is a resource class, False otherwise.
    """
    return (
        class_name == "R" or class_name.startswith("R$") or class_name == "BuildConfig"
    )


def is_app_class(class_def: lief.DEX.Class, framework_tree: PackageTree = None) -> bool:
    """Checks if a class is an application class.

    :param class_def: The lief.DEX.Class object representing the class.
    :param framework_tree: Optional. The PackageTree representing the framework classes.
                           If provided, the class will be checked against the framework tree.
    :return: True if the class is an application class, False otherwise.
    """
    # IMPORTANT: app classes can be retrieved by using x.source_filename
    # as those ones will always have a .java filename. All other classes
    # won't be covered
    if not class_def.source_filename:
        return False

    # Normalization:
    # filter empty dummy classes as well as framework classes that
    # are within the framework tree (optional)
    class_name = class_def.pretty_name
    if is_inner_class(class_name):
        # check whether the class is an anonymous inner class
        if re.match(r"^.+\$\d+$", class_name):
            # Check whether there are no "real" methods
            methods = class_def.methods
            if len(methods) == 0 or (
                len(methods) == 1 and methods[0].name == "<clinit>"
            ):
                # apply last checks:
                return (
                    len(list(filter(lambda x: x.is_static, class_def.fields))) == 0
                    and len(list(filter(lambda x: not x.is_static, class_def.fields)))
                    == 0
                    and not class_def.has_parent
                )

    # Synthetic classes won't be covered
    if class_def.has(lief.DEX.ACCESS_FLAGS.SYNTHETIC):
        return False

    if is_resource_class(class_def.name):
        return False

    if not framework_tree:
        # We return True as the tree won't be covered (UNSAFE)
        return True

    return class_name not in framework_tree


def is_app_method(method: lief.DEX.Method) -> bool:
    """Checks if a method is an application method.

    :param method: The lief.DEX.Method object representing the method.
    :return: True if the method is an application method, False otherwise.
    """
    # Normalization:
    # filter out compiler-generated classes
    access_flags = method.access_flags

    if lief.DEX.ACCESS_FLAGS.SYNTHETIC in access_flags:
        return False

    return True


def simple_name(class_name: str) -> str:
    """Extracts the simple name of a class.

    >>> simple_name("Ljava/lang/Integer;")
    'Integer'

    :param class_name: Name of the class.
    :return: The simple name of the class.
    """
    return to_packages(class_name, include_class=True, is_internal=True)[-1]


CUSTOM_TYPE_REPLACEMENT = "X"


def get_method_signature(method: lief.DEX.Method) -> str:
    """Generates the method signature for a given method object.

    >>> get_method_signature(...)
    'java.lang.String.toString()java.lang.String'

    :param method: The lief.DEX.Method object representing the method.
    :return: The method signature.
    """
    class_name = method.cls.pretty_name
    method_name = method.name
    prototype = method.prototype
    param_types = []

    for ptype in prototype.parameters_type:
        if ptype.type == lief.DEX.Type.TYPES.PRIMITIVE:
            param_types.append(TYPE_DESCRIPTOR[str(ptype)])
        else:
            param_types.append(str(ptype))

    rtype = prototype.return_type

    if rtype.type == lief.DEX.Type.TYPES.PRIMITIVE:
        rtype = TYPE_DESCRIPTOR[str(rtype)]
    else:
        rtype = str(rtype)

    descriptor = f"({''.join(param_types)}){rtype}"

    return f"{class_name}.{method_name}{descriptor}"


def is_app_type(parameter: str, vm, framework_tree) -> bool:
    """
    Checks if a given parameter type is an application type.

    :param parameter: The parameter type.
    :param vm: The virtual machine object.
    :param framework_tree: The PackageTree representing the framework classes.
    :return: True if the parameter type is an application type, False otherwise.
    """
    class_def = vm.get(parameter, None)
    name = parameter

    if name.removeprefix("L").startswith(FW_TYPES):
        return False

    return (class_def and is_app_class(class_def, framework_tree)) or (
        class_def and not class_def.source_filename
    )


def param_name(
    parameter: lief.DEX.Type,
    vm: dict[str, lief.DEX.Class],
    framework_tree: PackageTree = None,
) -> str:
    if parameter.type == lief.DEX.Type.TYPES.PRIMITIVE:
        # just add primitive types
        return TYPE_DESCRIPTOR[str(parameter)]

    elif parameter.type == lief.DEX.Type.TYPES.ARRAY:
        atype: lief.DEX.Type = parameter.underlying_array_type
        if atype.type == lief.DEX.Type.TYPES.PRIMITIVE:
            return "".join(("[" * parameter.dim, TYPE_DESCRIPTOR[str(atype)]))
        else:
            return (
                CUSTOM_TYPE_REPLACEMENT
                if is_app_type(str(atype), vm, framework_tree)
                else "".join(("[" * parameter.dim, internal_name(str(atype))))
            )
    else:
        name = str(parameter)
        if is_app_type(name, vm, framework_tree):
            return CUSTOM_TYPE_REPLACEMENT
        else:
            return internal_name(name)


def normalize_inner_cls_descriptor(
    method: lief.DEX.Method,
    vm: dict[str, lief.DEX.Class],
    framework_tree: PackageTree = None,
) -> str | None:
    # The normalization of constructors for anonymous inner classes is necessary
    # because the dx compiler sometimes adds the superclass of the enclosing class
    # as a second parameter, while the javac compiler does not. This difference in
    # behavior leads to different hashes for these classes, even though they are of
    # the same version. As a result, this library cannot be matched exactly. To
    # address this issue, during the generation of the fuzzy descriptor, this
    # normalization process skips the second argument.
    declaring_class = method.cls
    cls_simple_name = simple_name(declaring_class.fullname)
    prototype = method.prototype
    # 1. Check anonymous inner inner classes
    if (
        re.match(r"^.+\$\d+\$\d+$", cls_simple_name)
        and method.name == "<init>"
        and len(prototype.parameters_type) > 1
    ):  # this can be anything -> normalize constructor to (X)V
        return "(X)V"

    # 2. Check anonymous inner classes
    if not (
        re.match(r"^.+\$\d+$", cls_simple_name)
        and method.name == "<init>"
        and len(prototype.parameters_type) > 2
    ):
        return None

    enclosing_class_name = cls_simple_name[: cls_simple_name.rfind("$")]
    # check if both argument types are custom types
    for i in range(2):
        ptype = prototype.parameters_type[i]
        if ptype.type == lief.DEX.Type.TYPES.ARRAY:
            ptype = ptype.underlying_array_type

        if ptype.type == lief.DEX.Type.TYPES.PRIMITIVE or not is_app_type(
            str(ptype), vm, framework_tree
        ):
            return None

    super_cls = vm.get(enclosing_class_name, None)
    if not super_cls:
        return None

    arg_type1 = simple_name(str(prototype.parameters_type[0]))
    arg_type2 = simple_name(str(prototype.parameters_type[1]))
    # now check whether this normalization needs to be applied
    if arg_type1 == enclosing_class_name and arg_type2 == simple_name(super_cls):
        params = []
        parameters = prototype.parameters_type
        for i in range(2, len(parameters)):
            params.append(param_name(parameters[i], vm, framework_tree))

        return "(%s)V" % "".join(params)


def get_fuzzy_descriptor(
    method: lief.DEX.Method,
    vm: dict[str, lief.DEX.Class],
    framework_tree: PackageTree = None,
) -> str | None:
    """Generates a fuzzy descriptor for a given method.

    A descriptor describes only the input argument types and the return type.
    For example, the descriptor of ``AdVideoView.onError(Landroid/media/MediaPlayer;II)Z``
    is ``(Landroid/media/MediaPlayerII)Z``. To create a fuzzy descriptor that is resilient
    to identifier renaming, we replace each custom type with a fixed replacement.
    For instance, we receive a descriptor like ``(XII)Z``.

    It is important to note that library dependencies, such as lib A depending on lib B,
    do not pose a problem. When analyzing lib A without loading lib B, any type from lib
    B will be loaded with the Application classloader but will not be included in the
    class hierarchy.

    >>> # assume the method's descriptor := '(Ljava/lang/String;[BI)[Lcom/example/MyClass;
    >>> get_fuzzy_descriptor(...)
    '(Ljava/lang/String;[BI)X'
    >>> # assume the method's descriptor := '(Lcom/example/MyClass;Ljava/lang/String;)V
    >>> get_fuzzy_descriptor(...)
    '(XLjava/lang/String)V'

    :param method: The ``lief.DEX.Method`` object representing the method.
    :param vm: The dictionary containing the class definitions.
    :param framework_tree: The PackageTree representing the framework classes.
    :return: The fuzzy descriptor of the method.
    """
    prototype = method.prototype
    if not prototype:
        raise RuntimeError("Could not get prototype of method: %s", method)
    # REVISIT: Necessary?
    descriptor = normalize_inner_cls_descriptor(method, vm, framework_tree)
    if descriptor is not None:
        return descriptor

    rtype = prototype.return_type
    ptypes = prototype.parameters_type
    param_names = []
    for parameter in ptypes:
        param_names.append(param_name(parameter, vm, framework_tree))

    n_return_type = param_name(rtype, vm, framework_tree)
    return f"({''.join(param_names)}){n_return_type}"
