.. _sphazel-context:

======================================
Why manage Sphinx projects with Bazel?
======================================

.. _migrating pigweed.dev to Bazel: https://pigweed.dev/docs/blog/08-bazel-docgen.html

After spending most of Q4 2024 `migrating pigweed.dev to Bazel`_ I now have a
pretty good idea of the benefits and challenges of managing Sphinx projects
through Bazel. This page helps you decide whether Sphinx + Bazel is right for you.

.. _sphazel-context-background:

----------
Background
----------

First, let's make sure we're on the same page.

.. _Sphinx: https://www.sphinx-doc.org
.. _Bazel: https://bazel.build

`Sphinx`_ is a system for authoring docs.

https://bazel.build/basics/hermeticity
