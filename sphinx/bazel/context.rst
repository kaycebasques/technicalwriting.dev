.. _sphazel-context:

==============================================================
The good, bad, and ugly of managing Sphinx projects with Bazel
==============================================================

In the spirit of :ref:`decisions` I would like to share my experience of
managing Sphinx projects with Bazel. My goal is to make it easier for others
to decide whether this setup is worthwhile for them.

.. _pigweed.dev: https://pigweed.dev
.. _migrating pigweed.dev to Bazel: https://pigweed.dev/docs/blog/08-bazel-docgen.html

I have about 5 years of professional experience with Sphinx. In my first
technical writing job, I migrated my employer's docs from Microsoft Word to
Sphinx. For the last few years I have been leading `pigweed.dev`_, which is
powered by Sphinx. I spent most of Q4 2024 `migrating pigweed.dev to Bazel`_.
The site has over 600 pages of content and integrates with 3 different API
reference auto-generation pipelines so I've got a pretty good sense of what
it's like to manage a real, production Sphinx project with Bazel.

If you're already sold on the idea of managing your Sphinx project with Bazel
and just need setup guidance, check out :ref:`sphazel-tutorial`.

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
`reStructuredText`_ or `Markdown`_ and then use Sphinx to transform the docs into
HTML and other output formats. You can also hook in auto-generated API reference
information from tools like `Doxygen`_.

.. _variety of reasons: https://bazel.build/about/why

`Bazel`_ is primarily a tool for building software. Software engineering teams
use it for a `variety of reasons`_ that mostly revolve around improving team
productivity.

"Managing a Sphinx project with Bazel" means orchestrating core Sphinx workflows
(such as transforming the docs into HTML) through Bazel's build system.

.. _sphazel-context-build-system:

------------------------------
Why use a build system at all?
------------------------------

.. _sphinx-build: https://www.sphinx-doc.org/en/master/man/sphinx-build.html

Many Sphinx projects don't use a build system whatsoever. They just run
`sphinx-build`_ directly from the root directory of the docs (e.g. ``//docs``)
and the output gets generated alongside the source (e.g. ``//docs/_build``).

.. _migrating pigweed.dev to Bazel: https://pigweed.dev/docs/blog/08-bazel-docgen.html
.. _GN: https://chromium.googlesource.com/chromium/src/tools/gn/+/48062805e19b4697c5fbd926dc649c78b6aaa138/README.md
.. _adopted Bazel as its primary build system: https://pigweed.dev/seed/0111.html
.. _significantly improve embedded developer productivity: https://blog.bazel.build/2024/08/08/bazel-for-embedded.html
.. _sidecar: https://passo.uno/docs-as-code-topologies/#sidecar-docs-and-code-living-together

In the case of `pigweed.dev`_, the switch from `GN`_ to Bazel was not motivated
by any particular failing of the old GN-based docs build system. Pigweed
`adopted Bazel as its primary build system`_ back in Q3 2023 because it can
`significantly improve embedded developer productivity`_. Eventually everything
in the Pigweed codebase was powered by Bazel except for the docs. (Pigweed uses
a `sidecar`_ docs-as-code topology, where the docs live alongside the code in a
single repo.) Managing the docs in GN and everything else in Bazel was slowing
us down and creating needless complexity.

.. _sphazel-context-good:

--------
The good
--------

Here are the ways that Bazel seemingly improves productivity 

Through the experience of migrating `pigweed.dev`_ to Bazel I learned that
Bazel can streamline many common workflows related to developing Sphinx projects.

.. _sphazel-context-good-cli:

A single CLI entrypoint for all development workflows
=====================================================

.. _Tour of Pigweed: https://pigweed.dev/docs/showcases/sense/

I am phrasing the topic as "*managing* Sphinx projects with Bazel" rather than
"*building* Sphinx projects with Bazel" because Bazel is not just about building
software. You can run lots of other workflows through it. For example, the
`Tour of Pigweed`_ demo uses Bazel to run tests, start a simulator, connect
to a console, flash an embedded device, and more.

.. _sphazel-context-good-setup:

Simplified development environment setup
========================================

With Bazel, building the docs can become a literal three-step process like
this:

.. code-block:: console

   $ git clone https://github.com/technicalwriting/dev.git
   $ cd dev
   $ ./bazelisk build //:docs

.. _technicalwriting.dev: https://technicalwriting.dev

(This example works. You're welcome to try it. `technicalwriting.dev`_ is a
Sphinx project and I actually do manage it with Bazel now. If you're on macOS
use ``./bazelisk-mac`` instead of ``./bazelisk``. For Windows, use
``./bazelisk-windows``.)

When Bazel attempts to build the ``//:docs`` target it detects that it
doesn't have all the tools and dependencies it needs to build the target.
It automatically fetches them, sets them all up, and then proceeds with the build.

(I'm a cheating a little by assuming that the ``bazelisk`` executable is
checked into the repo, which is an uncommon practice.)

.. _sphazel-context-good-virtualenv:

No more fiddling with virtual environments
==========================================

.. _works on my machine: https://medium.com/@josetecangas/but-it-works-on-my-machine-cc8cca80660c
.. _hermeticity: https://bazel.build/basics/hermeticity
.. _reproducible builds: https://reproducible-builds.org/docs/definition/

One of the main problems that Bazel solves for software engineers is
the `works on my machine`_ problem. E.g. the source code compiles for teammate
A, yet the exact same source code doesn't compile for teammate B. Many hours of
debugging ensue to pinpoint the difference in their development environments.
Through `hermeticity`_ Bazel can guarantee that a given set of inputs always
produce the exact same outputs for all teammates. This is also known as
`reproducible builds`_.

.. _hot button: https://www.merriam-webster.com/dictionary/hot%20button

Reproducible builds aren't a hot button issue for Sphinx projects. No one's
really worried about whether Sphinx builds the docs exactly the same for all
teammates.

However, hermeticity does bring one tangible benefit to Sphinx projects:
no more need for virtual environments. Bazel always runs all Sphinx workflows
from an isolated sandbox so there's no need to also spin up a virtual environment.

.. _sphazel-context-good-sidecar:

Sidecar friendly
================

.. _sidecar: https://passo.uno/docs-as-code-topologies/#sidecar-docs-and-code-living-together

In terms of docs-as-code topologies, a `sidecar`_ is when your docs live in the same
repo as the rest of your source code. This is a powerful setup because it increases the
chances that software engineers keep their docs up-to-date. In my experience most software
engineers are actually fine with updating docs, so long as its easy to find the relevant
docs. If an engineer changes an API in ``//src/module_a/lib.cpp`` and they see ``docs.rst``
right next to ``lib.cpp``, it's very obvious that ``docs.rst`` might also need an update.
On the other hand, if the relevant doc lives at ``//docs/guides/logs/docs.rst``, then it's not
obvious that the change to ``//src/module_a/lib.cpp`` affected the doc.

Bazel makes it easier to put your docs right next to the source code that they're related to.

For example, in the Pigweed repo we structure our docs and source code like this:

.. code-block:: text

   .
   ├── a
   │   ├── a.cpp
   │   └── a.rst
   ├── b
   │   ├── b.cpp
   │   └── b.rst
   └── docs
       ├── conf.py
       └── index.rst

Sphinx, however, expects a structure like this:

.. code-block:: text

   .
   ├── a
   │   └── a.cpp
   ├── b
   │   └── b.cpp
   └── docs
       ├── a
       │   └── a.rst
       ├── b
       │   └── b.rst
       ├── conf.py
       └── index.rst

By default, Sphinx considers the directory containing ``conf.py`` to
be the root docs directory. All ``*.rst`` (reST) files should be at or
below the root docs directory.

In the old GN-based system we had to hack together this reorganization
logic ourselves. Bazel has built-in support for source reorganization via
its ``prefix`` and ``strip_prefix`` features.

.. _sphazel-context-good-ecosystem:

Surprisingly robust ecosystem
=============================

.. _bzlmod: https://bazel.build/external/overview#bzlmod
.. _rules_python: https://rules-python.readthedocs.io/en/latest/

`bzlmod`_ ("Bazel mod") is the main mechanism for sharing your Bazel "libraries" A.K.A.
modules with others. When I migrated pigweed.dev to Bazel I was surprised to
discover that most of the features I needed were already available through community
modules. For example, `rules_python`_ has extensive support for building Sphinx
projects, including a built-in workflow for spinning up a server so that you can
locally preview the HTML output in a browser. This is the main reason the
`pigweed.dev`_ migration went faster than expected.

.. _sphazel-context-bad:

-------
The bad
-------

For large Sphinx projects, there can be quite a bit of upfront investment.

.. _sphazel-context-bad-explicit:

Explicit build graphs
=====================

As explained in :ref:`sphazel-context-good-virtualenv`, Bazel builds your
Sphinx project in an isolated sandbox. I'm not sure if this is technically correct,
but I imagine Bazel copying the source code into a separate directory, building
everything based off the copies, and then deleting all the copies. For this reason,
everything that the Sphinx project depends on must be declared explicitly in Bazel files.
If you don't declare something, it won't get copied over to the isolated sandbox.
This can take a while to set up.

.. _sphazel-context-bad-indirection:

More indirection
================

Bazel necessarily introduces more complexity into a Sphinx project because
it introduces new layers of indirection.

Suppose that you previously built the HTML docs directly like this:

.. code-block:: console

   $ sphinx-build -M html ./src ./_build

The generated HTML is easy to find: ``./_build/html/…``

When you build through the HTML docs through Bazel with a command like this:

.. code-block:: console

   $ ./bazelisk build //:docs

You can still inspect the generated HTML. But it's at a more convoluted
and non-obvious path: ``./bazel-bin/docs/_build/html/…``

This is just one of many ways that Bazel introduces more indirection into the project.

.. _sphazel-context-ugly:

--------
The ugly
--------

There's one major issue related to developer experience.

Lack of incremental builds
==========================

Suppose you have a medium-sized Sphinx project. You build the HTML docs directly
with Sphinx's build command, using the same command as before:

.. code-block:: console

   $ sphinx-build -M html ./src ./_build

Sphinx builds everything and caches the outputs somewhere. I'm not sure where exactly.
This command takes 10 seconds.

Now suppose that you change one line in your docs and run ``sphinx-build`` again. This
subsequent build takes only 1 second. It's fast because Sphinx only rebuilds the
changed content. This is what I mean by incremental builds.

Incremental builds don't work out-the-box when managing Sphinx projects through Bazel.
Continuing with the example, every docs build takes 10 seconds, even if you only
change one line of code in the docs source.

Sphinx and Bazel both have robust support for incremental builds so I'm hopeful that
there's a solution here. But it definitely doesn't work out-of-the-box as far as I can tell.
