|Linkie logo|

Linkie
==============================================================================

Linkie looks through files for broken links using Python 3.5+

|Build Status|

Usage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Linkie will search all files within the directory it's run and any
subdirectories, and requires a simple YAML config file to run.
You can then run Linkie from the command line.

.. code-block:: bash

  linkie

You can also pass Linkie a YAML file of configuration values (for example
``linkie linkie.yaml``). The YAML file can contain the following optional
settings:

1) ``exclude_directories`` - Any directories listed will be ignored, these
   are relative to the directory Linkie is run from.
2) ``file_types`` - The file extensions to search for URLs.
3) ``skip_urls`` - URLs to skip checking.

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

Linkie can also be used within Python:

.. code-block:: python3

  import linkie
  checker = linkie.Linkie()  # Creates a linkie object.
  result = checker.run()     # Returns 1 if broken links found, otherwise 0.

You can also use a config file within Python:

.. code-block:: python3

  import linkie
  checker = linkie.Linkie('linkie.yaml')  # Creates a linkie object with custom settings.

You can also access the following attributes from the linkie after it's run:

.. code-block:: python3

  linkie.urls  # Dictionary of processed URLs and their data.
  linkie.status_counts  # Dictionary of status codes and their counts.
  linkie.file_count     # Number of files processed.

License
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Linkie is licensed under the MIT License. Read the `license file`_ for
more details.

Changelog
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.1.1
------------------------------------------------------------------------------

- Update method for URLs with brackets.

1.1.0
------------------------------------------------------------------------------

- Allow adding URLs to skip to configuration file.
- Skip checking URLs that have already been checked.
- Show connection error names instead of 999 status.
- Uses class based object allowing user to retrieve values after running.

1.0.0
------------------------------------------------------------------------------

- Initial linkie release.

FAQ
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Why was this created as a Python package?
------------------------------------------------------------------------------

We required a script to check our repositories for broken links.
This tool was initially written in Python, and a published Python package makes
it easy for repositories to use this tool, in combination with pyup notifying
if the package is updated.

Can you update linkie to support this specific URL?
------------------------------------------------------------------------------

Probably not. This script was initally created as an internal tool so we are
not actively developing and supporting it compared to our other repositories.
However we have published it freely under the MIT License to allow you to
copy and modify linkie as you wish.

Will you get around to writing proper documentation?
------------------------------------------------------------------------------

Maybe. This script was initally created as an internal tool so doesn't have
the same level of polish as other projects we create. If we have more time
down the road, we may spend more time developing linkie.

How do I install the development version as local package?
------------------------------------------------------------------------------

1. ``$ git clone https://github.com/uccser/linkie.git``
2. ``$ cd linkie``
3. ``$ pip3 install .``

.. |Linkie logo| image:: https://raw.githubusercontent.com/uccser/linkie/master/images/linkie-logo.png
   :target: https://github.com/uccser/linkie
   :alt: Linkie logo

.. _license file: LICENSE

.. |Build Status| image:: https://travis-ci.org/uccser/linkie.svg?branch=master
   :target: https://travis-ci.org/uccser/linkie
