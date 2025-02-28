.. _sphinx-bazel:

==============================
Build a Sphinx site with Bazel
==============================

.. _migrating pigweed.dev to Bazel: https://pigweed.dev/docs/blog/08-bazel-docgen.html
.. _Sphinx: https://www.sphinx-doc.org
.. _Bazel: https://bazel.build
.. _minimal, reproducible example: https://stackoverflow.com/help/minimal-reproducible-example

I spent most of Q4 2024 `migrating pigweed.dev to Bazel`_. I now know quite a bit
about building `Sphinx`_ sites with `Bazel`_! This tutorial provides a
`minimal, reproducible example`_ of how to build a Sphinx site with Bazel.

Note what versions of Sphinx and Bazel this was written against

----------
Motivation
----------

Why build a Sphinx site with Bazel?

* Hermeticity

* Lots of features provided by rules_python

-----------------------
Set up a Sphinx project
-----------------------

#. Create a directory for your project:

   .. code-block:: console

      $ mkdir venture-industries-website

#. Make the project directory your working directory:

   .. code-block:: console

      $ cd venture-industries-website

#. Create ``conf.py`` and add the following content to it:

   .. code-block:: py

      project = 'venture-industries-website'
      author = 'Dean Venture'
      copyright = f'2025, Venture Industries'
      release = '0.0.1'
      exclude_patterns = [
          '.github',
          '.gitignore',
          'requirements.txt',
          'requirements.lock',
      ]
      pygments_style = 'sphinx'

#. Create ``index.rst`` and add the following content to it:

   .. code-block:: rst

      .. _home:

      ==================
      Venture Industries
      ==================

      Rusty Venture, CEO of Venture Industries, has officially declared that
      Dean is his favorite son. He also noted that his other son, Hank, is a
      dork.

-------------------------------
Set up third-party dependencies
-------------------------------

#. Create ``requirements.txt`` and add the following content to it:

   .. code-block:: text

      sphinx==8.1.3

#. Create a virtual environment:

   .. code-block:: console

      $ python3 -m venv venv

#. Activate the virtual environment:

   .. code-block:: console

      $ source venv/bin/activate

#. Install your third-party dependencies in the virtual environment:

   .. code-block:: console

      $ python3 -m pip install -r requirements.txt

#. Record your full list of dependencies in a lockfile:

   .. code-block:: console

      $ python3 -m pip freeze > requirements.lock

------------
Set up Bazel
------------

#. Create ``MODULE.bazel`` and add the following content to it:

   .. code-block:: py

      bazel_dep(name = "rules_python", version = "1.1.0")

      pip = use_extension("@rules_python//python/extensions:pip.bzl", "pip")
      pip.parse(
          hub_name = "pypi",
          python_version = "3.11",
          requirements_lock = "//:deps_full.txt",
      )
      use_repo(pip, "pypi")

#. Create ``BUILD.bazel`` and add the following content to it:

   .. code-block:: py

      load("@rules_python//sphinxdocs:sphinx.bzl", "sphinx_build_binary", "sphinx_docs")
      load("@rules_python//sphinxdocs:sphinx_docs_library.bzl", "sphinx_docs_library")

      sphinx_build_binary(
          name = "sphinx",
          deps = [
              "@pypi//sphinx",
          ]
      )

      sphinx_docs_library(
          name = "sources",
          srcs = [
              "index.rst",
          ],
      )

      sphinx_docs(
          name = "docs",
          config = "conf.py",
          formats = [
              "html",
          ],
          sphinx = ":sphinx",
          deps = [
              ":sources",
          ]
      )

--------------
Build the docs
--------------

TODO

------------------------
Locally preview the docs
------------------------
