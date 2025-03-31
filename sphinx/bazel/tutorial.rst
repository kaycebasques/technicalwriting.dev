.. _sphazel-tutorial:

=================================
Manage Sphinx projects with Bazel
=================================

.. _Sphinx: https://www.sphinx-doc.org
.. _Bazel: https://bazel.build

This tutorial shows you how to manage core `Sphinx`_ workflows through `Bazel`_.
You'll learn how to: 

* Set up the Bazel build system
* Build the Sphinx docs
* Inspect the built docs
* Spin up a local server to preview the docs
* Add an extension
* Deploy to GitHub Pages

Check out :ref:`sphazel-context` for help deciding whether or not
this setup is worthwhile for you.

I'm going to assume that you're familiar with Sphinx but not familiar with
Bazel. I.e. Sphinx concepts will not be explained whereas Bazel ones will.

.. _sphazel-tutorial-hermeticity:

-------------------
A key Bazel concept
-------------------

.. _Hermeticity: https://bazel.build/basics/hermeticity

`Hermeticity`_. Bazel builds your Sphinx project in an isolated sandbox so that
it can guarantee that a certain set of inputs always produces the same
output(s). You must explicitly declare to Bazel all the inputs (i.e. source
files, tools, and third-party dependencies) that your Sphinx project needs.
Bazel basically copies all the inputs into a temporary directory, locks down
the directory from reading anything outside of it, resets all OS environment
variables, and then builds the project under those controlled conditions.

This is the most important concept to understand because you will inevitably
forget to declare an input to Bazel and you will see an ``<input> not found`` error
of one sort or another.

.. _sphazel-tutorial-sphinx:

-----------------------
Set up a Sphinx project
-----------------------

.. _direct and transitive dependencies: https://fossa.com/blog/direct-dependencies-vs-transitive-dependencies/

First, let's create a bare-bones Sphinx project.

#. Create a directory for your project:

   .. code-block:: console

      mkdir sphazel

#. Make the project directory your working directory:

   .. code-block:: console

      cd sphazel

#. Create ``conf.py`` and configure the Sphinx project:

   .. code-block:: py

      project = 'sphazel'
      author = 'sphazel'
      copyright = f'2025, Hank Venture'
      release = '0.0.0'
      exclude_patterns = [
          '**/*bazel*',
          'requirements.*',
      ]
      extensions = []
      pygments_style = 'sphinx'

#. Create ``.gitignore`` and specify that Bazel output directories
   should be ignored:

   .. code-block:: text

      bazel-*

#. Create ``index.rst`` and add the following content to it:

   .. code-block:: rst

      .. _sphazel:

      =======
      sphazel
      =======

      Sphinx + Bazel = sphazel

#. Create ``requirements.txt`` and declare your project's direct dependencies there:

   .. code-block:: text

      sphinx==8.2.3

#. Freeze your `direct and transitive dependencies`_ into a new file called
   ``requirements.lock``:

   .. code-block:: console

      python3 -m venv venv &&
          . venv/bin/activate &&
          python3 -m pip install -r requirements.txt && 
          python3 -m pip freeze > requirements.lock &&
          deactivate &&
          rm -rf venv

   Here we spin up a temporary virtual environment, install the dependencies
   into the virtual environment, record the full list of dependencies into
   ``requirements.lock``, and then delete the virtual environment because it's
   no longer needed.

   The lockfile is not optional. You'll learn why in the next section.

.. _sphazel-tutorial-bazel:

------------
Set up Bazel
------------

Next, we set up the Bazel build system.

.. _Bazel modules: https://bazel.build/external/module
.. _BUILD files: https://bazel.build/concepts/build-files
.. _bazel_dep: https://bazel.build/rules/lib/globals/module#bazel_dep
.. _rules_python: https://github.com/bazel-contrib/rules_python
.. _sphinxdocs: https://rules-python.readthedocs.io/en/latest/sphinxdocs/index.html
.. _pip: https://en.wikipedia.org/wiki/Pip_(package_manager)
.. _Python Package Index: https://pypi.org/
.. _Bazel Central Registry: https://registry.bazel.build/
.. _sphinx-build: https://www.sphinx-doc.org/en/master/man/sphinx-build.html
.. _artifact: https://bazel.build/basics/artifact-based-builds

#. Create ``MODULE.bazel`` and add the following content to it:

   .. code-block:: py

      bazel_dep(name = "rules_python", version = "1.2.0")

      pip = use_extension("@rules_python//python/extensions:pip.bzl", "pip")
      pip.parse(
          hub_name = "pypi",
          python_version = "3.11",
          requirements_lock = "//:requirements.lock",
      )
      use_repo(pip, "pypi")

   ``MODULE.bazel`` is how we declare to the world that this is a Bazel project.
   ``MODULE.bazel`` is the only valid name for this file, which makes it easy to
   discover. See `Bazel modules`_. 

   The call to `bazel_dep`_ tells Bazel to pull the `rules_python`_ module into
   our project as a dependency. ``rules_python`` provides most of the mechanisms
   for managing our Sphinx project. Bazel fetches ``rules_python``
   over the network via the `Bazel Central Registry`_. 

   The rest of the code sets up the project to be able to use `pip`_ to
   install third-party Python dependencies from the `Python Package Index`_
   as needed. 

   One important thing to note is that you must pass in ``requirements.lock``,
   i.e. the full list of `direct and transitive dependencies`_.
   ``rules_python`` only installs the exact packages that you tell it about.
   This is different than how ``pip`` usually works. For example, when you run
   ``python3 -m pip install requests``  usually ``pip`` will not only install
   the ``requests`` package that you explicitly requested (pun intended) but
   also all the packages that ``requests`` itself depends on. When using
   ``pip`` from Bazel there is no attempt to resolve transitive dependencies
   for you.

#. Create ``BUILD.bazel`` and add the following content to it:

   .. code-block:: py

      load("@rules_python//sphinxdocs:sphinx.bzl", "sphinx_build_binary", "sphinx_docs")
      load("@rules_python//sphinxdocs:sphinx_docs_library.bzl", "sphinx_docs_library")

      sphinx_docs_library(
          name = "sources",
          srcs = [
              "index.rst",
          ],
      )

      sphinx_build_binary(
          name = "sphinx",
          deps = [
              "@pypi//sphinx",
          ]
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

   `BUILD files`_ tell Bazel how exactly it should build the project. The only
   allowed names for these files are ``BUILD`` or ``BUILD.bazel``.

   The ``load`` functions import the core mechanisms for building the
   Sphinx project: ``sphinx_build_binary``, ``sphinx_docs``, and
   ``sphinx_docs_library``. All of these come from ``rules_python``.

   The ``sphinx_docs_library`` rule is where we declare all of the source files
   of the Sphinx project.

   ``sphinx_build_binary`` sets up the `sphinx-build`_ binary. Note how
   third-party PyPI packages (such as ``sphinx``) are passed as dependencies
   to this rule. This will come up again in :ref:`sphazel-tutorial-extension`.

   ``sphinx_docs`` is where the Sphinx build actually happens. Note the colon
   (``:``) before ``:sphinx`` and ``:sources``. This indicates that the thing
   you're passing in is an `artifact`_ that is produced somewhere in
   the Bazel build.

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

.. _nvm: https://github.com/nvm-sh/nvm

`Bazelisk`_ is kinda hard to explain. It's basically how you're supposed to run
Bazel from the command line. It downloads the Bazel CLI executable that you
specify in ``.bazelversion`` but then you also use it to run all your
command-line Bazel workflows. It's like if `nvm`_ and ``npm`` were combined
into a single program. It's honestly kinda needlessly convoluted. It seems like
``bazelisk`` should be called ``bazel`` and it should be the only way to use
Bazel from the command line. And the thing currently called ``bazel`` should be
an implementation detail.

Anyways, we need a way to run Bazel from the command line, and ``bazelisk`` is
the way we're supposed to do it.

#. Download Bazelisk:

   .. code-block:: console

      curl -L -O https://github.com/bazelbuild/bazelisk/releases/download/v1.25.0/bazelisk-linux-amd64

   This is the executable for Linux running on x86-64. See `v1.25.0`_ for links to other
   platforms. E.g. if you're using macOS on Apple Silicon, then you need to download
   the ``bazelisk-darwin-arm64`` executable instead.

   It's also possible to install via ``apt``, ``npm``, ``homebrew``, etc. but in
   my experience you sometimes get a very old version of Bazelisk. Better to just
   directly download the latest release.

#. Make the file executable:

   .. code-block:: console

      chmod +x bazelisk-linux-amd64

In my own projects I personally just check in the Bazelisk executables
alongside the rest of the code. The more common approach is to have teammates
download the relevant Bazelisk executable for their machine to a typical
location (e.g. ``~/.local/bin``) and then set up an alias so that they can
invoke ``bazelisk`` from any directory. In my approach you have to specify the
path to the executable when you invoke it but you eliminate the need for each
teammate to manually set up Bazel on their own machine.

.. _sphazel-tutorial-build:

--------------
Build the docs
--------------

That's all you need to start using Bazel.

#. Build the docs:

   .. code-block:: console

      ./bazelisk-linux-amd64 build //:docs

   In plain English this command is saying "build the artifact named ``docs`` that
   is defined in the ``BUILD.bazel`` (or ``BUILD``) file in the root directory of
   this Bazel project". 

   Example output from a successful build:

   .. code-block:: console

      Starting local Bazel server (8.1.1) and connecting to it...
      INFO: Analyzed target //:docs (122 packages loaded, 6072 targets configured).
      INFO: Found 1 target...
      Target //:docs up-to-date:
        bazel-bin/docs/_build/html
      INFO: Elapsed time: 11.967s, Critical Path: 2.47s
      INFO: 8 processes: 7 internal, 1 linux-sandbox.
      INFO: Build completed successfully, 8 total actions

Debug the docs build
====================

If your Sphinx project has errors and you're building the project hermetically,
the output can be pretty noisy and hard-to-read. You can sometimes trim away
the noise by building the Sphinx project non-hermetically:

.. code-block:: console

   bazelisk run //docs:docs.run

.. _sphazel-tutorial-inspect:

--------------------------
Inspect the generated HTML
--------------------------

When I need to inspect the generated HTML, I just do something like this:

.. code-block:: console

   vim bazel-bin/docs/_build/html/index.html

.. _sphazel-tutorial-preview:

------------------------
Locally preview the docs
------------------------

One very cool thing about ``rules_python`` is that it also has a
built-in local server for previewing the docs:

.. code-block:: console

   ./bazelisk-linux-amd64 run //:docs.serve

It should output a ``localhost`` URL where you can preview the docs:

.. code-block:: text

   INFO: Analyzed target //:docs.serve (0 packages loaded, 461 targets configured).
   INFO: Found 1 target...
   Target //:docs.serve up-to-date:
     bazel-bin/docs.serve
   INFO: Elapsed time: 0.843s, Critical Path: 0.15s
   INFO: 5 processes: 5 internal.
   INFO: Build completed successfully, 5 total actions
   INFO: Running command line: bazel-bin/docs.serve bazel-out/k8-fastbuild/bin/docs/_build/html
   Serving...
     Address: http://0.0.0.0:8001
     Serving directory: /home/kayce/github/kaycebasques/sphazel/bazel-out/k8-fastbuild/bin/docs/_build/html
         url: file:///home/kayce/github/kaycebasques/sphazel/bazel-out/k8-fastbuild/bin/docs/_build/html
     Server CWD: /home/kayce/.cache/bazel/_bazel_kayce/74072e0325cb6dc49620a5c889c58931/execroot/_main/bazel-out/k8-fastbuild/bin/docs.serve.runfiles/_main

   *** You do not need to restart this server to see changes ***
   *** CTRL+C once to reprint this info ***
   *** CTRL+C twice to exit ***

.. _sphazel-tutorial-extension:

----------------
Add an extension
----------------

.. _Extensions: https://www.sphinx-doc.org/en/master/usage/extensions/index.html
.. _sphinx-reredirects: https://pypi.org/project/sphinx-reredirects/

`Extensions`_ are one of my favorite aspects of the Sphinx ecosystem.
My projects use them heavily. Here's how to add one to the Bazel build.

#. Update ``requirements.txt`` to indicate that you're going to use
   `sphinx-reredirects`_ to generate client-side redirects.

   .. code-block:: console

      sphinx==8.2.3
      sphinx-reredirects==0.1.5

#. Update your lockfile again to capture the new direct and
   transitive dependencies:

   .. code-block:: console

      python3 -m venv venv &&
          . venv/bin/activate &&
          python3 -m pip install -r requirements.txt && 
          python3 -m pip freeze > requirements.lock &&
          deactivate &&
          rm -rf venv

#. Update ``conf.py`` to use the extension:

   .. code-block:: py
      :emphasize-lines: 2, 4

      # …
      extensions = ["sphinx_reredirects"]
      pygments_style = 'sphinx'
      redirects = {'example': 'https://example.com'}

#. Declare the dependency to Bazel by updating ``BUILD.bazel``:

   .. code-block:: py
      :emphasize-lines: 7

      # …

      sphinx_build_binary(
          name = "sphinx",
          deps = [
              "@pypi//sphinx",
              "@pypi//sphinx_reredirects",
          ]
      )

      # …

.. _sphazel-tutorial-pages:

------------------------
Deploy with GitHub Pages
------------------------

I'll assume that you're familiar with setting up Pages via the GitHub web UI
and just show you the YAML.

#. Create ``.github/workflows/deploy.yml`` and add the following
   content to it:

   .. code-block:: yaml

      name: deploy
      on:
        push:
          branches: ['main']
        workflow_dispatch:
      permissions:
        contents: read
        pages: write
        id-token: write
      jobs:
        deploy:
          environment:
            name: github-pages
            url: ${{steps.deployment.outputs.page_url}}
          runs-on: ubuntu-latest
          steps:
            - name: checkout
              uses: actions/checkout@v4
            - name: configure
              uses: actions/configure-pages@v5
            - name: build
              run: ${{github.workspace}}/bazelisk-linux-amd64 build //:docs
            - name: upload
              uses: actions/upload-pages-artifact@v3
              with:
                path: ${{github.workspace}}/bazel-out/k8-fastbuild/bin/docs/_build/html
            - name: deploy
              id: deployment
              uses: actions/deploy-pages@v4

.. _sphazel-tutorial-examples:

-------------
More examples
-------------

* `Main BUILD.bazel file for technicalwriting.dev <https://github.com/technicalwriting/dev/blob/main/BUILD.bazel>`_
* `Main BUILD.bazel file for pigweed.dev <https://cs.opensource.google/pigweed/pigweed/+/main:docs/BUILD.bazel>`_ 
