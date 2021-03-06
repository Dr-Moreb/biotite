# This source code is part of the Biotite package and is distributed
# under the 3-Clause BSD License. Please see 'LICENSE.rst' for further
# information.

import biotite.sequence as seq
from biotite.application.muscle import MuscleApp
from biotite.application.mafft import MafftApp
from biotite.application.clustalo import ClustalOmegaApp
import numpy as np
import pytest
import shutil

@pytest.mark.skipif(shutil.which("muscle")   is None or
                    shutil.which("mafft")    is None or
                    shutil.which("clustalo") is None,
                    reason="At least one MSA application is not installed")
@pytest.mark.parametrize("app_cls, exp_ali, exp_order",
    [(MuscleApp,
      "BIQT-ITE\n"
      "TITANITE\n"
      "BISM-ITE\n"
      "-IQL-ITE",
      [1,2,0,3]),                
     (MafftApp,
      "-BIQTITE\n"
      "TITANITE\n"
      "-BISMITE\n"
      "--IQLITE",
      [0,3,2,1]),
     (ClustalOmegaApp, 
      "-BIQTITE\n"
      "TITANITE\n"
      "-BISMITE\n"
      "--IQLITE",
     [1,2,0,3])]
)
def test_msa(app_cls, exp_ali, exp_order):
    seq1 = seq.ProteinSequence("BIQTITE")
    seq2 = seq.ProteinSequence("TITANITE")
    seq3 = seq.ProteinSequence("BISMITE")
    seq4 = seq.ProteinSequence("IQLITE")
    app = app_cls([seq1, seq2, seq3, seq4])
    app.start()
    app.join()
    alignment = app.get_alignment()
    order = app.get_alignment_order()
    print(order)
    assert str(alignment) == exp_ali
    assert order.tolist() == exp_order