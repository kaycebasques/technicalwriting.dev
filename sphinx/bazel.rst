.. _sphazel:

=================================
Manage Sphinx projects with Bazel
=================================

This post shows you how to use Bazel to run core Sphinx workflows like
building the docs and locally previewing the docs.

The next section, :ref:`sphazel-context`, helps you decide whether
or not using Bazel with Sphinx is right for you. If you're already sold on the
idea, skip ahead to :ref:`sphazel-sphinx`.

.. _sphazel-context:

-------
Context
-------

.. _Sphinx: https://www.sphinx-doc.org
.. _reStructuredText: https://en.wikipedia.org/wiki/ReStructuredText
.. _Markdown: https://en.wikipedia.org/wiki/Markdown
.. _Doxygen: https://www.doxygen.nl
.. _Bazel: https://bazel.build

`Sphinx`_ is a tool for authoring documentation. You write your docs in
`reStructuredText`_ or `Markdown`_ and use Sphinx to transform the docs into
HTML or other output formats. You can also hook in content that has been
auto-generated with tools like `Doxygen`_.

.. _variety of reasons: https://bazel.build/about/why

`Bazel`_ is primarily a tool for building software. Software engineering teams
use it for a `variety of reasons`_ that mostly revolve around improving team
productivity.

.. _Tour of Pigweed: https://pigweed.dev/docs/showcases/sense/

I titled the post ``Manage Sphinx projects with Bazel`` rather than ``Build
Sphinx with Bazel`` because Bazel is not just about building software. You can
run lots of other workflows through it. For example, the `Tour of Pigweed`_
project uses Bazel to run tests, start a simulator, connect to a console, flash
an embedded device, and more. 

Why manage Sphinx with Bazel?
=============================

.. _migrating pigweed.dev to Bazel: https://pigweed.dev/docs/blog/08-bazel-docgen.html
.. _GN: https://chromium.googlesource.com/chromium/src/tools/gn/+/48062805e19b4697c5fbd926dc649c78b6aaa138/README.md
.. _adopted Bazel as its primary build system: https://pigweed.dev/seed/0111.html
.. _great promise for improving embedded developer productivity: https://blog.bazel.build/2024/08/08/bazel-for-embedded.html

I spent most of Q4 2024 `migrating pigweed.dev to Bazel`_. In the case of
pigweed.dev, the switch from `GN`_ to Bazel was not motivated by any particular
failing of the old GN-based docs build system. Pigweed had `adopted Bazel as
its primary build system`_ back in Q3 2023 because it holds `great promise for
improving embedded developer productivity`_. By the time Q4 2024 rolled around,
all of the Pigweed codebase except the docs had been migrated to Bazel.
Managing the docs in one build system (GN) and everything else in another build
system (Bazel) was slowing us down.

However, through this experience I learned that Bazel can streamline many
core Sphinx project workflows, such as:

* Development environment setup. With Bazel, building or locally previewing
  the docs can become a literal three-step process like this:

  .. code-block:: console

     $ git clone https://github.com/technicalwriting/dev.git
     $ cd dev
     $ ./bazelisk build //:docs

  When Bazel attempts to build the ``//:docs`` target it detects that it
  doesn't have all the tools and dependencies it needs to build the target.
  It automatically fetches them, sets them all up, and then proceeds with the build.

  (Think of ``bazelisk`` as the way you run Bazel from the CLI. You'll learn
  more about it in :ref:`sphazel-bazelisk`. Also, I'm a cheating a
  little by assuming that the ``bazelisk`` executable is checked into the repo,
  which is not a common practice.)

* Hermeticitiy. Bazel builds your Sphinx project in an isolated sandbox to guarantee
  that certain inputs always produce the same outputs. For embedded development this feature
  is very important because it's common for slight variations to get introduced into the
  compiled firmware depending on 
  a huge problem around slight variations getting introduced into the compiled firmware depending
  on whether the source code was built on Windows versus Linux (for example). For Sphinx
  projects that's not much of a concern, but Bazel's hermeticity does provide another
  tangible benefit: no more need to fiddle around with Python virtual environments.

.. _bzlmod: https://bazel.build/external/overview#bzlmod
.. _rules_python: https://rules-python.readthedocs.io/en/latest/

* Surprisingly robust developer ecosystem. `bzlmod`_ is the main mechanism for sharing your
  Bazel "libraries" A.K.A. modules with others. When I migrated pigweed.dev to Bazel I was surprised to discover
  that most of what I needed was already available through community modules. For example,
  `rules_python`_ has extensive support for building Sphinx projects. It even has a built-in
  workflow for locally previewing the docs!

Why NOT manage Sphinx with Bazel?
=================================

For large Sphinx projects, there's quite a bit of upfront investment:

* Everything that the Sphinx project depends on must be declared explicitly.
  It takes a while to figure out how to hook up everything together correctly.

* Bazel naturally introduces more complexity into the Sphinx project because
  there's a new layer of indirection.

There's one very big developer experience problem:

* Incremental builds don't work out-the-box. I.e. you change one line in the docs
  and Bazel rebuilds all of the docs from scratch. Bazel is supposedly very good at
  caching so I'm confident that I'll eventually figure out how to get incremental builds
  working. But it definitely doesn't work out-the-box.

.. _sphazel-sphinx:

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

.. _sphazel-deps:

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

.. _sphazel-bazel:

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

.. _sphazel-bazelisk:

---------------
Set up Bazelisk
---------------

#. Download Bazelisk:

   .. code-block:: console

      $ curl -L -O https://github.com/bazelbuild/bazelisk/releases/download/v1.25.0/bazelisk-linux-amd64

#. Make the file executable:

   .. code-block:: console

      $ chmod +x bazelisk-linux-amd64

.. _sphazel-build:

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

.. _sphazel-inspect:

--------------------------
Inspect the generated HTML
--------------------------

#. Open

https://linux.die.net/man/1/xdg-open

.. _sphazel-preview:

------------------------
Locally preview the docs
------------------------

.. _sphazel-git:

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


