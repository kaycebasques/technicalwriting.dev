.. _sphazel-context:

===============================
Sphinx and Bazel decision guide
===============================

This post aims to help you decide whether or not using managing Sphinx
projects through Bazel is right for you. If you're already sold on the
idea, check out :ref:`sphazel-tutorial`.

.. _sphazel-context-background:

----------
Background
----------

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

.. _sphazel-context-good:

--------
The good
--------

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

.. _sphazel-context-good-setup:

Simplified development environment setup
========================================

With Bazel, building or locally previewing the docs can become a literal three-step process like this:

.. code-block:: console

   $ git clone https://github.com/technicalwriting/dev.git
   $ cd dev
   $ ./bazelisk build //:docs

When Bazel attempts to build the ``//:docs`` target it detects that it
doesn't have all the tools and dependencies it needs to build the target.
It automatically fetches them, sets them all up, and then proceeds with the build.

(Think of ``bazelisk`` as the way you run Bazel from the CLI. You'll learn
more about it in :ref:`sphazel-tutorial-bazelisk`. Also, I'm a cheating a
little by assuming that the ``bazelisk`` executable is checked into the repo,
which is not a common practice.)

.. _sphazel-context-good-hermeticity:

Hermeticity
===========

Bazel builds your Sphinx project in an isolated sandbox to guarantee
that certain inputs always produce the same outputs. For embedded development this feature
is very important because it's common for slight variations to get introduced into the
compiled firmware depending on 
a huge problem around slight variations getting introduced into the compiled firmware depending
on whether the source code was built on Windows versus Linux (for example). For Sphinx
projects that's not much of a concern, but Bazel's hermeticity does provide another
tangible benefit: no more need to fiddle around with Python virtual environments.

.. _sphazel-context-good-ecosystem:

(Surprisingly) robust developer ecosystem
=========================================

.. _bzlmod: https://bazel.build/external/overview#bzlmod
.. _rules_python: https://rules-python.readthedocs.io/en/latest/

`bzlmod`_ is the main mechanism for sharing your Bazel "libraries" A.K.A.
modules with others. When I migrated pigweed.dev to Bazel I was surprised to
discover that most of the features I needed were already available through community
modules. For example, `rules_python`_ has extensive support for building Sphinx
projects, including a built-in workflow for spinning up a server so that you can
locally preview the HTML output in a browser.

.. _sphazel-context-bad:

-------
The bad
-------

For large Sphinx projects, there's quite a bit of upfront investment.
There's also one very important issue with the developer experience.

.. _sphazel-context-bad-explicit:

Explicit build graphs
=====================

Everything that the Sphinx project depends on must be declared explicitly.
It takes a while to figure out how to hook up everything together correctly.

.. _sphazel-context-bad-complexity:

More complexity
===============

Bazel naturally introduces more complexity into the Sphinx project because
there's a new layer of indirection.

.. _sphazel-context-bad-hermeticity:

Hermeticity (redux)
===================

…

.. _sphazel-context-ugly:

--------
The ugly
--------

Lack of incremental builds
==========================

Incremental builds don't work out-the-box. I.e. you change one line in the docs
and Bazel rebuilds all of the docs from scratch. Bazel is supposedly very good at
caching so I'm confident that I'll eventually figure out how to get incremental builds
working. But it definitely doesn't work out-the-box.

--------------
More resources
--------------

…
