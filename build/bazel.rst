.. _bazel:

===============================================
Development log: Migrating pigweed.dev to Bazel
===============================================

I have been charged with the fascinating and sometimes-overwhelming task
of migrating pigweed.dev's build system from GN to Bazel. These are my
chronological notes on the project.

.. _bazel-20240924:

---------------
Tue Sep 24 2024
---------------

I wrote a design doc today summarizing the project and plan. Here's the
gist of the design doc.

.. _Sphinx: https://www.sphinx-doc.org/en/master/

pigweed.dev is powered by `Sphinx`_. Sphinx expects your docs to be structured
under a root directory, like this:

.. code-block:: text

   .
   ├── a
   │   └── a.rst
   ├── b
   │   └── b.rst
   ├── c
   │   └── c.rst
   ├── conf.py
   └── index.rst

The directory containing ``conf.py`` and ``index.rst`` is the root directory.
``a/a.rst``, ``b/b.rst``, and ``c/c.rst`` are easy to integrate into the
Sphinx system because they're all in subdirectories relative to the root
directory.

pigweed.dev on the other hand is structured like this:

.. code-block:: text

   .
   ├── a
   │   └── a.rst
   ├── b
   │   └── b.rst
   ├── c
   │   └── c.rst
   └── docs
       ├── conf.py
       └── index.rst

Some of our docs are in sibling directories relative to the root directory.
Sphinx doesn't like this.

Our GN build system mainly just gathers up all the documentation-related
files that are spread across the Pigweed repo and packages them up into the
directory structure that Sphinx expects. Then we just ``cd`` into that new
directory and run Sphinx normally. This is the main functionality that I need
to recreate in Bazel.

.. _rules_python/sphinxdocs: https://github.com/bazelbuild/rules_python/tree/main/sphinxdocs

We're going to use `rules_python/sphinxdocs`_ as the foundation of our
Bazel-based build system. At first glance it seems to provide everything we
need.

.. _Sphinx Extensions: https://www.sphinx-doc.org/en/master/usage/extensions/index.html

The main challenge of this project is that pigweed.dev is a fairly big docs
site and it's not easy to migrate to Bazel incrementally. For example,
Sphinx has a wonderful cross-reference feature that guarantees that all internal
links are correct. If you try to link to a doc that doesn't exist, Sphinx treats
this as an error and stops the build. There's probably a way to downgrade this
particular error to just a warning where Sphinx complains about the problem
but continues building the site. My main point is that there are lots of things
like this that make incremental migration difficult.
