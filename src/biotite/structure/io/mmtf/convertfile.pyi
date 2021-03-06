# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

from typing import Union, Tuple, List, overload
from ...atoms import AtomArray, AtomArrayStack
from .file import MMTFFile


@overload
def get_structure(
    pdbx_file: MMTFFile,
    model: None = None,
    insertion_code: List[Tuple[int, str]] = [],
    altloc: List[Tuple[int, str]] = [],
    extra_fields: List[str] = [],
    include_bonds: bool = False
) -> AtomArrayStack: ...
@overload
def get_structure(
    pdbx_file: MMTFFile,
    model: int,
    insertion_code: List[Tuple[int, str]] = [],
    altloc: List[Tuple[int, str]] = [],
    extra_fields: List[str] = [],
    include_bonds: bool = False
) -> AtomArray: ...