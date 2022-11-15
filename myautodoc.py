import pandas as pd
from myImageLib import readdata
import sys
import os

"""
myautodoc
=========

Extract docstrings from *\*.py* files and write them in *\*.rst* files in docs/source folder. The names are kept consistent with the *\*.py* files. 

.. rubric:: Syntax

.. code-block:: console

   python myautodoc.py

.. rubric:: Edit

* Nov 15, 2022 -- Initial commit.
"""

cwd = os.path.abspath(".")
doc_folder = os.path.join(cwd, "docs", "source")
index_string = "Welcome to script's documentation!\n==================================\n\nPython scripts to facilitate my data analysis.\n\nContents\n--------\n\n.. toctree::\n\n"

l = readdata(cwd, ext="py", mode="i")

for num, i in l.iterrows():
    with open(i.Dir, "r") as f:
        a = f.read()
    try:
        ind1 = a.index("\"\"\"") + 3
        ind2 = a.index("\"\"\"", ind1)
        docstring = a[ind1: ind2]
    except:
        print(i.Name + " does not have a proper docstring.")
        continue

    index_string += "   {}\n".format(i.Name)

    with open(os.path.join(doc_folder, "{}.rst".format(i.Name)), "w") as f:
        f.write(docstring)

with open(os.path.join(doc_folder, "index.rst"), "w") as f:
    f.write(index_string)
