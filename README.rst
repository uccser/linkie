|Linkie logo|

Linkie
==============================================================================

Linkie looks through files for broken links using Python 3.5+

|Build Status|

Usage
------------------------------------------------------------------------------

Linkie will search all files within the directory it's run and any
subdirectories, and requires a simple YAML config file to run.
You can then run Linkie from the command line.

.. code-block:: none

  linkie

You can also pass Linkie a YAML file of configuration values (for example
``linkie linkie.yaml``). The YAML file can contain two optional settings:

1) ``exclude_directories`` - Any directories listed will be ignored, these
   are relative to the directory Linkie is run from.
2) ``file_types`` - The file extensions to search for URLs.

Example configuration file (these are the default values Linkie uses):

.. code-block:: yaml

  exclude_directories:
    - .git/
    - docs/build/

  file_types:
    - html
    - md
    - rst
    - txt

License
------------------------------------------------------------------------------

Linkie is licensed under the MIT License. Read the `license file`_ for
more details.

FAQ
------------------------------------------------------------------------------

**Why was this created as a Python package?**

We required a script to check our repositories for broken links.
This tool was initially written in Python, and a published Python package makes
it easy for repositories to use this tool, in combination with pyup notifying
if the package is updated.

**Where is the changelog?**

The changelog is available within the `changelog file`_.

**How do I install the development version as local package?**

1. ``$ git clone https://github.com/uccser/linkie.git``
2. ``$ cd linkie``
3. ``$ pip3 install .``

.. |Linkie logo| image:: https://raw.githubusercontent.com/uccser/linkie/master/images/linkie-logo.png
   :target: https://github.com/uccser/linkie
   :alt: Linkie logo

.. _license file: LICENSE

.. |Build Status| image:: https://travis-ci.org/uccser/linkie.svg?branch=master
   :target: https://travis-ci.org/uccser/linkie
