.. _sphazel-tutorial:

=================================
Manage Sphinx projects with Bazel
=================================

This tutorial shows you how to manage core Sphinx workflows such as
building the docs and locally previewing the docs through Bazel.

Check out :ref:`sphazel-context` for help deciding whether or not
this setup is worthwhile for you.

.. _sphazel-tutorial-sphinx:

-----------------------
Set up a Sphinx project
-----------------------

First, we spin up a minimal Sphinx project.

#. Create a directory for your project:

   .. code-block:: console

      $ mkdir sphazel

#. Make the project directory your working directory:

   .. code-block:: console

      $ cd sphazel

#. Create ``conf.py`` and add the following content to it:

   .. code-block:: py

      project = 'sphazel'
      author = 'sphazel'
      copyright = f'2025, Hank Venture'
      release = '0.0.1'
      exclude_patterns = [
          '.gitignore',
          'requirements.txt',
          'requirements.lock',
      ]
      pygments_style = 'sphinx'

   The files listed in ``exclude_patterns`` don't exist yet. You'll create them later.

#. Create ``index.rst`` and add the following content to it:

   .. code-block:: rst

      .. _sphazel:

      =======
      sphazel
      =======

      Hello, Sphinx + Bazel!

.. _sphazel-tutorial-deps:

-------------------------------
Set up third-party dependencies
-------------------------------

.. _hermetically: https://bazel.build/basics/hermeticity

Bazel will build your Sphinx project `hermetically`_.

When you build Sphinx projects through Bazel, you need to declare all dependencies
explicitly.

#. Create ``requirements.txt`` and add the following content to it:

   .. code-block:: text

      sphinx==8.2.3

#. Create a virtual environment:

   .. code-block:: console

      $ python3 -m venv venv

#. Activate the virtual environment.

   Bash:

   .. code-block:: console

      $ source venv/bin/activate

   fish:

   .. code-block:: console

      $ . venv/bin/activate.fish

#. Use the latest version of ``pip`` in the virtual environment:

   .. code-block:: console

      $ python3 -m pip install --upgrade pip

#. Install your third-party dependencies into the virtual environment:

   .. code-block:: console

      $ python3 -m pip install -r requirements.txt

#. Record your full list of dependencies in a lockfile:

   .. code-block:: console

      $ python3 -m pip freeze > requirements.lock

#. Deactivate your virtual environment:

   .. code-block:: console

      $ deactivate

#. Delete the virtual environment:

   .. code-block:: console

      $ rm -rf venv

.. _sphazel-tutorial-bazel:

------------
Set up Bazel
------------

#. Create ``MODULE.bazel`` and add the following content to it:

   .. code-block:: py

      bazel_dep(name = "rules_python", version = "1.2.0")

      pip = use_extension("@rules_python//python/extensions:pip.bzl", "pip")
      pip.parse(
          hub_name = "pypi",
          python_version = "3.12",
          requirements_lock = "//:requirements.lock",
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

#. Create ``.bazelversion`` and add the following content to it:

   .. code-block:: text

      8.1.1

.. _sphazel-tutorial-bazelisk:

---------------
Set up Bazelisk
---------------

#. Download Bazelisk:

   .. code-block:: console

      $ curl -L -O https://github.com/bazelbuild/bazelisk/releases/download/v1.25.0/bazelisk-linux-amd64

#. Make the file executable:

   .. code-block:: console

      $ chmod +x bazelisk-linux-amd64

.. _sphazel-tutorial-build:

--------------
Build the docs
--------------

#. Build the docs:

   .. code-block:: console

      $ ./bazelisk-linux-amd64 build //:docs

   Example of a successful build:

   .. code-block:: console

      $ ./bazelisk-linux-amd64 build //:docs

      INFO: Analyzed target //:docs (120 packages loaded, 6055 targets configured).
      INFO: Found 1 target...
      Target //:docs up-to-date:
        bazel-bin/docs/_build/html
      INFO: Elapsed time: 13.725s, Critical Path: 2.62s
      INFO: 8 processes: 7 internal, 1 linux-sandbox.
      INFO: Build completed successfully, 8 total actions

.. _sphazel-tutorial-inspect:

--------------------------
Inspect the generated HTML
--------------------------

#. Open

https://linux.die.net/man/1/xdg-open

.. _sphazel-tutorial-preview:

------------------------
Locally preview the docs
------------------------

.. _sphazel-tutorial-git:

-----------------------
Check the code into Git
-----------------------

#. Create ``.gitignore`` and add the following content to it:

   .. code-block:: text

	    bazel-bin
	    bazel-out
	    bazel-sphazel
	    bazel-testlogs

#. Check in everything else:

   .. code-block:: console

      $ git add .

#. And commit:

   .. code-block:: console

      $ git commit -m 'Init'


