.. Crisk documentation master file, created by sphinx-quickstart on Tue Feb 17 15:39:52 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

About Crisk
===========

Crisk is a simple risk management tool. Its objective is to provide risk analysts, security professionals and secure software developers  with a tool to organize vulnerabilities, assets and (futurely) controls, generating reports and graphics for easy analysis.

Tickets and Bug Reporting
=========================

Crisk uses the `Lighthouse App as bug tracking system <http://core.lighthouseapp.com/projects/25415-crisk/>`_. Feel free to report bugs or suggest new features.

Getting Crisk
=============

Crisk right now is avaiable on source form only. You may:

* `Download a tarball <http://github.com/coredump/crisk/zipball/master>`_
* `Download a zipfile <http://github.com/coredump/crisk/tarball/master>`_
* Clone the git repository: ``$ git clone git://github.com/coredump/crisk``

Dependencies
------------

Crisk depends on some other modules that are right now kinda hard to package. To get Crisk working you will need:

* Matplotlib (0.98 or higher)
* Reportlab (2.2 or higher)
* `Geraldo <http://geraldo.sourceforge.net/>`_
* Elixir (0.6 or higher)
* PyGTK
* `Kiwi <http://www.async.com.br/projects/kiwi/>`_ 

I suggest using your distribution packages when possible and `easy_install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ when everything else fails. Reportlab does not install correctly with ``easy_install`` so it is better do download and install from source. 

Installers and MS Windows
~~~~~~~~~~~~~~~~~~~~~~~~~

Crisk runs perfectly on Microsoft Windows. Unfortunately I had some problems packaging the software with py2exe and decided to spend my time improving Crisk instead of dealing with neverending problems. So, you can install Python 2.5, install easy_install, install the dependencies above and Crisk will run find. I will eventually get around the py2exe errors, but don't hold your breath.

Contents
========
.. toctree::
   :maxdepth: 2

   screenshots
   using
   todo
   crisk

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

