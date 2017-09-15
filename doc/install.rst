Installation instructions
=========================

Biopython 2.0 comes in two flavors: A binary distribution with some extra
C-accelerated functions (e.g. for alignments or mmCIF parsing) and a
source distribution without the extension modules. Note that the source
distribution still has the same functionality - some operations are just a lot
slower.

Binary distribution
-------------------

Biopython 2.0 uses *wheels* for binary package distributions. This is the
default way to install Biopython 2.0, therefore you can just type this:

.. code-block:: python

   pip install biopython>=2.0

If *pip* finds an appropriate *wheel* for your system configuration on *PyPI*,
it will download and install it. Congratulations, you just installed 
Biopython 2.0! If no fitting *wheel* is found, *pip* will fall back to the
already mentioned source distribution. If you want to prevent *pip* to do that,
use the following command:

.. code-block:: python

   pip install biopython>=2.0 --only-binary :all:

In case there is no *wheel* available for you, but you still want the
juicy performance increase, you have to build the *wheel* on your own.
In order to do that, you first need to download the repository from GitHub.
Then open a terminal in the top-level folder (the one, ``setup.py`` is in) and
type the following:

.. code-block:: python

   python setup.py bdist_wheel

Note that this step requires *Cython* and a C-compiler (typically GCC) to be
installed. Then you navigate into the ``dist`` folder and type

.. code-block:: python

   pip install <package.whl>
   
where ``<package.whl>`` is the *wheel* file existing in the directory
(it should be the only file there, you can't miss it).

You can check if your Biopython 2.0 distribution successfully uses
C-extensions via the `has_c_extensions()` function.

.. code-block:: python

   >>> import biopython
   >>> print(biopython.has_c_extensions())
   True

If the function returns `False` or, even worse, an exception, then something
went wrong.

Source distribution
-------------------

The source distribution, written in pure Python, should be seen as a fallback
option, which is useful, if there is either no *wheel* available for you or the
available *wheel* is not working for some reason (or you just don't like fast
code).
*pip* will automatically install the source distribution if it does not find
an appropriate *wheel*. If you want to insist on using the source distribution,
type the following command:

.. code-block:: python

   pip install biopython>=2.0 --no-binary :all:

Calling the `has_c_extensions()` function should now return `False`.

