.. PyCrash documentation master file, created by
   sphinx-quickstart on Tue Jan  1 13:03:56 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyCrash's documentation!
===================================

PyCrash is a python application crash reporting framework. It is based on
PyCrash over at http://pycrash.sourceforge.net/. However that project seems to
be dead.

I cloned off that version of PyCrash and then significantly updated it. I was
unable to contribute to that project as I could not get hold of Carmine I.D.
Noviello is author. Therfore Ive started a new clone of the project here.

My Version of pycrash has the folowing featires ...
    * Smarter XML generation using lxml
    * Smarter HTML generation using mako
    * A dispatcher framework that allows you to :
            * Get emails when you application crashes
            * Post crash reports to an ACR server.
            * Lots of other fixes and updates

Please note that this version of PyCrash is still in the pre release development
stages.

Contents:

.. toctree::
   :maxdepth: 2

   introduction.rst
   sample.rst
   dispatchers.rst

.. automodule:: pycrash


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
