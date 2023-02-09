"""
Extract docstrings from *\*.py* files and write them in *\*.rst* files in docs/source folder. The names are kept consistent with the *\*.py* files. 

.. rubric:: Syntax

.. code-block:: console

   python myautodoc.py

.. rubric:: Edit

* Nov 15, 2022 -- Initial commit.
* Feb 08, 2023 -- Rewrite in function wrapper form, to make autodoc work properly. (autodoc import the script and execute it, so anything outside ``if __name__=="__main__"`` will be executed, causing problems)
* Feb 09, 2023 -- Repurpose this script to write "scripts.rst" file, which use ``autosummary`` to document all the scripts.
"""
import pandas as pd
from myimagelib.myImageLib import readdata
import sys
import os

if __name__ == "__main__":
    cwd = os.path.abspath(".")
    doc_folder = os.path.join(cwd, "docs", "source")
    index_string = "Scripts\n=======\n\n.. autosummary::\n   :template: mymodule.rst\n   :toctree: scripts\n\n"

    l = readdata(cwd, ext="py", mode="i")

    for num, i in l.iterrows():
        with open(i.Dir, "r") as f:
            a = f.read()
        try:
            ind1 = a.index("\"\"\"") + 3
            ind2 = a.index("\"\"\"", ind1)
        except:
            print(i.Name + " does not have a proper docstring.")
            continue

        index_string += "   {}\n".format(i.Name)

    with open(os.path.join(doc_folder, "scripts.rst"), "w") as f:
        f.write(index_string)
