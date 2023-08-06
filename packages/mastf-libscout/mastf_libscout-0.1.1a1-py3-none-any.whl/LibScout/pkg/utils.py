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


def to_packages(
    class_name: str, include_class: bool = False, is_internal: bool = False
) -> list[str]:
    """Splits a class name into individual package components.

    >>> to_packages("Ljava/lang/String;", is_internal=True)
    ['java', 'lang']
    >>> to_packages("Ljava/lang/String;", is_internal=True, include_class=True)
    ['java', 'lang', 'String']

    :param class_name: The fully qualified class name.
    :param include_class: Flag to include the class name in the result.
    :param is_internal: A flag indicating if the class is internal.
    :return: A list of package components.
    """
    delimiter = "."
    if is_internal:
        class_name = normalize_name(class_name)

    class_name = class_name.removesuffix(".class")
    result = class_name.split(delimiter)
    return result[:-1] if not include_class else result


def to_path(*elements) -> str:
    """Joins the elements into a dot-separated path.

    >>> to_path("foo", "bar")
    'foo.bar'
    >>> to_path("", "foo", "", "bar")
    'foo.bar'

    :param elements: The elements to be joined.
    :return: The dot-separated path.
    """
    values = []
    for element in map(lambda x: x.strip(), elements):
        if element:
            values.append(element)

    return ".".join(values)


def get_package_name(class_name: str, is_internal: bool = False) -> str:
    """Retrieves the package name from a fully qualified class name.

    >>> get_package_name("java.lang.String")
    'java.lang'
    >>> get_package_name("Ljava/lang/Object;", is_internal=True)
    'java.lang'

    :param class_name: The fully qualified class name.
    :param is_internal: Flag indicating if the class is internal.
    :return: The package name.
    """
    return to_path(*to_packages(class_name, is_internal=is_internal))


def normalize_name(class_name: str) -> str:
    """
    Normalizes the class name by replacing slashes with dots and removing prefixes
    and suffixes.

    >>> normalize_name("Ljava/lang/String;")
    'java.lang.String'

    :param class_name: The class name to be normalized.
    :return: The normalized class name.
    """
    class_name = class_name.replace("/", ".")
    # remove L and ;
    return class_name.removeprefix("L").removesuffix(";")

def internal_name(class_name: str) -> str:
    class_name = class_name.replace(".", "/")
    if not class_name.startswith("L"):
        class_name = f"L{class_name}"
    # NOTE: no trailing ';' here
    return class_name.removesuffix(";")
