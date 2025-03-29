.. _sphazel-tutorial:

=================================
Manage Sphinx projects with Bazel
=================================

This tutorial shows you how to manage core Sphinx workflows through Bazel.
Examples of core workflows:

* Building the docs
* Locally previewing the docs

Check out :ref:`sphazel-context` for help deciding whether or not
this setup is worthwhile for you.

.. _sphazel-tutorial-sphinx:

-----------------------
Set up a Sphinx project
-----------------------

First, let's create a bare-bones Sphinx project.

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
      release = '0.0.0'
      exclude_patterns = []
      extensions = []
      pygments_style = 'sphinx'

#. Create ``index.rst`` and add the following content to it:

   .. code-block:: rst

      .. _sphazel:

      =======
      sphazel
      =======

      Sphinx + Bazel = sphazel

.. _sphazel-tutorial-bazel:

------------
Set up Bazel
------------

.. _Bazel modules: https://bazel.build/external/module

.. _BUILD files: https://bazel.build/concepts/build-files

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


   This is how you declare to Bazel that your repo is a Bazel project.
   See `Bazel modules`_.

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

   `BUILD files`_ are the bread and butter of your Bazel-based build.
   In these files you declare to Bazel how exactly it should build your project.

#. Create ``.bazelversion`` and add the following content to it:

   .. code-block:: text

      8.1.1

   Bazel changes a lot from version to version. It's important to specify
   exactly what version of Bazel should be used to build your project.

.. _sphazel-tutorial-bazelisk:

---------------
Set up Bazelisk
---------------

.. _Bazelisk: https://bazel.build/install/bazelisk

.. _v1.25.0: https://github.com/bazelbuild/bazelisk/releases/tag/v1.25.0

`Bazelisk`_ is kinda hard to explain. It's basically how you're supposed to
run Bazel from the command line. It downloads the Bazel CLI executable that you
specify in ``.bazelversion`` and then basically runs the ``bazel`` executable
for you. It's honestly kinda needlessly convoluted. It seems like ``bazelisk``
should be the only way to run Bazel from the command line and the underlying
``bazel`` executable should be an implementation detail.

Anyways, we need a way to run Bazel from the command line, and ``bazelisk`` is
the way we're supposed to do it.

#. Download Bazelisk:

   .. code-block:: console

      $ curl -L -O https://github.com/bazelbuild/bazelisk/releases/download/v1.25.0/bazelisk-linux-amd64

   This is the executable for Linux running on x86-64. See `v1.25.0`_ for links to other
   platforms. E.g. if you're using macOS on Apple Silicon, then you need to download
   the ``bazelisk-darwin-arm64`` executable instead.

#. Make the file executable:

   .. code-block:: console

      $ chmod +x bazelisk-linux-amd64

In my own projects I personally just check in the Bazelisk executables alongside
the rest of the code. The more common approach is to have teammates download a 
Bazelisk executable to a typical location (e.g. ``~/.local/bin``) and then set up
an alias so that they can invoke ``bazelisk`` from any directory. In my approach you
have to specify the path to the executable when you invoke it.

.. _sphazel-tutorial-build:

--------------
Build the docs
--------------

That's all you need to start using Bazel.

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

When I need to inspect the generated HTML, I do this:

.. code-block:: console

   $ xdg-open 

https://linux.die.net/man/1/xdg-open

.. _sphazel-tutorial-preview:

------------------------
Locally preview the docs
------------------------


.. _sphazel-tutorial-deps:

-------------------------------
Set up third-party dependencies
-------------------------------

.. _hermetically: https://bazel.build/basics/hermeticity

.. _both direct and transitive dependencies: https://fossa.com/blog/direct-dependencies-vs-transitive-dependencies/

Bazel will build your Sphinx project `hermetically`_.

When you build Sphinx projects through Bazel, you need to declare all dependencies
explicitly.

#. Create ``requirements.txt`` and add the following content to it:

   .. code-block:: text

      matplotlib==3.9.2
      sphinx==8.2.3
      sphinx-reredirects==0.1.5

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

   The difference between ``requirements.txt`` and ``requirements.lock``
   is that the first file only specifies direct dependencies whereas
   the second file specifies `both direct and transitive dependencies`_.

#. Deactivate your virtual environment:

   .. code-block:: console

      $ deactivate

#. Delete the virtual environment:

   .. code-block:: console

      $ rm -rf venv



.. _sphazel-tutorial-extension:

----------------
Add an extension
----------------

#. Update ``index.rst`` and add the following content to it:

   .. code-block:: rst

      .. _sphazel:

      =======
      sphazel
      =======

      Hello, Sphinx + Bazel!

      .. plot::

         import matplotlib.pyplot as plt

         x_values = [1, 2, 3, 4, 5]
         y_values = [2, 3, 5, 7, 11]

         plt.plot(x_values, y_values, marker='o')
         plt.xlabel("X values")
         plt.ylabel("Y values")
         plt.title("Example plot")

#. Create ``conf.py`` and add the following content to it:

   .. code-block:: py

      project = 'sphazel'
      author = 'sphazel'
      copyright = f'2025, Hank Venture'
      release = '0.0.0'
      exclude_patterns = [
          'requirements.txt',
          'requirements.lock'
      ]
      extensions = [
          'matplotlib.sphinxext.plot_directive',
      ]
      pygments_style = 'sphinx'


#. Create ``BUILD.bazel`` and add the following content to it:

   .. code-block:: py

      load("@rules_python//sphinxdocs:sphinx.bzl", "sphinx_build_binary", "sphinx_docs")
      load("@rules_python//sphinxdocs:sphinx_docs_library.bzl", "sphinx_docs_library")

      sphinx_build_binary(
          name = "sphinx",
          deps = [
              "@pypi//matplotlib",
              "@pypi//sphinx",
              "@pypi//sphinx_reredirects",
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



Update lockfile

python3 -m venv venv && . venv/bin/activate.fish && python3 -m pip install -r requirements.txt && python3 -m pip freeze > requirements.lock && deactivate && rm -rf venv


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


