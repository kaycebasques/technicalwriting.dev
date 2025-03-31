.. _sphazel-context:

======================================================================
The good, the bad, and the ugly of managing Sphinx projects with Bazel
======================================================================

In the spirit of :ref:`decisions` I would like to share my experience of
managing Sphinx projects with Bazel. My goal is to make it easier for you to
decide whether or not this setup is worthwhile for you.

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
`reStructuredText`_ or `Markdown`_ and then use Sphinx to transform the docs
into HTML and other output formats. It's also common to hook in auto-generated
API reference docs from tools like `Doxygen`_ alongside the reStructuredText
or Markdown docs.

.. _variety of reasons: https://bazel.build/about/why

`Bazel`_ is primarily a tool for building software. Software engineering teams
use it for a `variety of reasons`_ that mostly revolve around ensuring that
software is built correctly and improving team productivity.

"Managing a Sphinx project with Bazel" means orchestrating core Sphinx
workflows (such as transforming the docs into HTML) through Bazel's build
system.

.. _sphazel-context-background-experience:

My experience with Sphinx and Bazel
===================================

.. _pigweed.dev: https://pigweed.dev
.. _migrating pigweed.dev to Bazel: https://pigweed.dev/docs/blog/08-bazel-docgen.html

I have about 5 years of experience with Sphinx. In my first technical writing
job, I migrated my employer's docs from Microsoft Word to Sphinx. For the last
few years I've been leading `pigweed.dev`_, which is powered by Sphinx. I spent
most of Q4 2024 `migrating pigweed.dev to Bazel`_. The site has over 600 pages
of content and integrates with 3 different API reference auto-generation
pipelines. I.e. I've got a pretty good sense of managing a non-trivial Sphinx
project with Bazel.

.. _sphazel-context-none:

------------------------------
Why use a build system at all?
------------------------------

.. _sphinx-build: https://www.sphinx-doc.org/en/master/man/sphinx-build.html
.. _sphinx-quickstart: https://www.sphinx-doc.org/en/master/man/sphinx-quickstart.html

Many Sphinx projects don't use a build system whatsoever. They just have a little
custom shell script that invokes `sphinx-build`_ directly. Or they use the minimal
``Makefile`` that `sphinx-quickstart`_ generates.

.. _kayce.basqu.es: https://kayce.basqu.es

In my own small Sphinx projects (such as this site and `kayce.basqu.es`_) I'm
actually finding a Bazel-based build to be less work to maintain than the usual
custom shell scripts that I previously cobbled together. I like not needing to
futz around with :ref:`virtual environments <sphazel-context-good-virtualenv>`
anymore. And I like that I'm continuing to build up experience with Bazel
because it has :ref:`more momentum than I realized
<sphazel-context-good-ecosystem>`.

In medium-to-large Sphinx projects that have a lot of contributors I think the
:ref:`sphazel-context-good-setup`, :ref:`sphazel-context-good-cli`, and the ability
to :ref:`keep docs close to their relevant code <sphazel-context-good-sidecar>` are
pretty compelling features. They probably improve productivity by making it much
easier to contribute to the project.

.. _sphazel-context-other:

------------------------------------
Why not use some other build system?
------------------------------------

.. _global minimum: https://mohitmishra786687.medium.com/the-curse-of-local-minima-how-to-escape-and-find-the-global-minimum-fdabceb2cd6a

I'm not really trying to push Bazel in particular. It's not like I've done a
systematic review of every build system and concluded that Bazel is the `global
minimum`_. I just happen to know a fair bit about managing Sphinx projects with
Bazel now because my work required me to migrate `pigweed.dev`_ from a GN-based
build to a Bazel one.

.. _What went well: https://pigweed.dev/docs/blog/08-bazel-docgen.html#what-went-well
.. _GN: https://chromium.googlesource.com/chromium/src/tools/gn/+/48062805e19b4697c5fbd926dc649c78b6aaa138/README.md
.. _adopted Bazel as its primary build system: https://pigweed.dev/seed/0111.html
.. _significantly improve embedded developer productivity: https://blog.bazel.build/2024/08/08/bazel-for-embedded.html
.. _sidecar: https://passo.uno/docs-as-code-topologies/#sidecar-docs-and-code-living-together

Well, I guess I do have an opinion on GN versus Bazel. If given a choice, I
would choose Bazel over GN for the reasons mentioned in `What went well`_.
However, the switch from `GN`_ to Bazel was not motivated by any particular
failing of the old GN-based docs build system. Pigweed `adopted Bazel as its
primary build system`_ back in Q3 2023 because it can `significantly improve
embedded developer productivity`_. Our strategy is to dogfood every aspect of
embedded devleopment in Bazel, including our docs.

.. _sphazel-context-good:

--------
The good
--------

Here's what I like about managing Sphinx projects with Bazel.

.. _sphazel-context-good-cli:

Unified CLI
===========

.. _Tour of Pigweed: https://pigweed.dev/docs/showcases/sense/

I am phrasing the topic as "*managing* Sphinx projects with Bazel" rather than
"*building* Sphinx projects with Bazel" because Bazel is not just about
building software. You can run lots of other workflows through it. For example,
the `Tour of Pigweed`_ demo uses Bazel to run tests, start a simulator, connect
to a console, flash an embedded device, and more.

.. _sphazel-context-good-setup:

Easier development environment setup
====================================

With Bazel, building the docs can become a literal three-step process like
this:

.. code-block:: console

   $ git clone https://github.com/technicalwriting/dev.git
   $ cd dev
   $ ./bazelisk build //:docs

When Bazel attempts to build the ``//:docs`` target it detects that it doesn't
have all the tools and dependencies it needs to build the target, automatically
fetches them, sets them all up, and then proceeds with the build.

(I'm a cheating a little by assuming that the ``bazelisk`` executable is
checked into the repo, which is an uncommon practice.)

.. _sphazel-context-good-virtualenv:

No need for virtual environments
================================

.. _works on my machine: https://medium.com/@josetecangas/but-it-works-on-my-machine-cc8cca80660c
.. _hermeticity: https://bazel.build/basics/hermeticity
.. _reproducible builds: https://reproducible-builds.org/docs/definition/

One of the main problems that Bazel solves for software engineers is the `works
on my machine`_ problem. E.g. the source code compiles for teammate A, yet the
exact same source code doesn't compile for teammate B. Many hours of debugging
ensue to pinpoint the difference in their development environments. Through
`hermeticity`_ Bazel can guarantee that a given set of inputs always produce
the exact same outputs for all teammates. This is also known as `reproducible
builds`_.

.. _hot button: https://www.merriam-webster.com/dictionary/hot%20button

Reproducible builds aren't a hot button issue for Sphinx projects. If Sphinx
doesn't build the docs exactly the same for all teammates, it's usually not a
big deal.

However, hermeticity does bring one tangible benefit to Sphinx projects: no
more need for virtual environments. Bazel always runs all Sphinx workflows from
an isolated sandbox so there's no need to also spin up a virtual environment.

.. _sphazel-context-good-sidecar:

Sidecar friendly
================

.. _sidecar: https://passo.uno/docs-as-code-topologies/#sidecar-docs-and-code-living-together

In terms of docs-as-code topologies, a `sidecar`_ is when your docs live in the
same repo as the rest of your source code. This is a powerful setup because it
increases the chances that software engineers keep their docs up-to-date. In my
experience most software engineers are actually fine with updating docs, so
long as its easy to find the relevant docs. If an engineer changes an API in
``//src/logger/lib.cpp`` and they see ``docs.rst`` right next to ``lib.cpp``,
it's very obvious that ``docs.rst`` might also need an update. On the other
hand, if the relevant doc lives at ``//docs/guides/logging/docs.rst``, then there's
less of a chance that the engineer will remember to update the doc. Out of sight,
out of mind.

.. _Built-in support for reorganizing sources: https://pigweed.dev/docs/blog/08-bazel-docgen.html#built-in-support-for-reorganizing-sources
.. _information architecture: https://en.wikipedia.org/wiki/Information_architecture

See `Built-in support for reorganizing sources`_ for more explanation of how
Bazel makes it easier to keep your docs in sight. The gist of the idea is to
prioritize keeping your docs right next to the code, and then use Bazel's features
to reorganize the docs into a usable `information architecture`_ on the docs website.

.. _sphazel-context-good-ecosystem:

Surprisingly robust ecosystem
=============================

.. _bzlmod: https://bazel.build/external/overview#bzlmod
.. _rules: https://bazel.build/extending/rules
.. _rules_python: https://rules-python.readthedocs.io/en/latest/
.. _rickeylev: https://github.com/rickeylev
.. _TendTo: https://github.com/TendTo

`bzlmod`_ ("Bazel mod") is the main mechanism for sharing your Bazel
`rules`_ (i.e. libraries) with others. When I migrated `pigweed.dev`_ to Bazel
I was surprised to discover that most of the rules I needed were already
available through community modules. For example, `rules_python`_ has extensive
support for building Sphinx projects, including a built-in workflow for
spinning up a server so that you can locally preview the HTML output in a
browser. This is the main reason the `pigweed.dev`_ migration went faster than
expected. People like `rickeylev`_ and `TendTo`_ had already built most everything
I needed.

.. _sphazel-context-bad:

-------
The bad
-------

Adopting Bazel requires some upfront investment and creates more complexity
for docs authors.

.. _sphazel-context-bad-explicit:

Explicit build graphs
=====================

As explained in :ref:`sphazel-context-good-virtualenv` and
:ref:`sphazel-tutorial-hermeticity`, Bazel builds your
Sphinx project in an isolated sandbox. You need to explicitly
declare all inputs in the build system. This can take a while to
set up correctly and wrap your head around.

It's not quite right to call this "bad". I actually really like declaring the
entire build graph explicitly. But it does take time and I imagine that some
teammates will never "get it" and will find it needlessly complex.

.. _sphazel-context-bad-indirection:

More indirection
================

Bazel necessarily introduces more complexity into a Sphinx project because
it introduces new layers of indirection.

Suppose that you previously built the HTML docs directly like this:

.. code-block:: console

   $ sphinx-build -M html ./src ./_build

The generated HTML is easy to find: ``./_build/html/…``

When you build the HTML docs through Bazel with a command like this:

.. code-block:: console

   $ ./bazelisk build //:docs

You can still inspect the generated HTML. But it's at a less-obvious path:
``./bazel-bin/docs/_build/html/…``

This is just one of many ways that Bazel introduces more indirection into the
project.

.. _sphazel-context-ugly:

--------
The ugly
--------

There's one major issue related to developer experience.

Lack of incremental builds
==========================

Suppose you have a medium-sized Sphinx project. You build the HTML docs
directly with Sphinx's build command:

.. code-block:: console

   $ sphinx-build -M html ./src ./_build

Sphinx builds everything and caches the outputs somewhere. This command takes
10 seconds.

Now suppose that you change one line in your docs and run ``sphinx-build``
again. This subsequent build takes only 1 second. It's fast because Sphinx only
rebuilds the changed content and went to its cache for the rest. This is what I
mean by incremental builds.

Incremental builds don't work out-the-box when managing Sphinx projects through
Bazel. Continuing with the example, every docs build takes 10 seconds, even if
you only change one line of code in the docs source.

Sphinx and Bazel both support caching so I'm hopeful that there's a solution
here. But it definitely doesn't work out-of-the-box as far as I can tell.
