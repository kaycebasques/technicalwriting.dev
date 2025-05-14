.. _incremental:

==================================
Incremental Sphinx builds in Bazel
==================================

These are my notes on a docs infrastructure issue that I'm currently wrestling with.

-------
Problem
-------

.. _migrated pigweed.dev to Bazel: https://pigweed.dev/docs/blog/08-bazel-docgen.html

In Q1 2025 we `migrated pigweed.dev to Bazel`_. Our biggest developer experience
pain point is the lack of incremental builds. E.g. every docs build takes 80 seconds.
It's fine for the first docs build from scratch to take 80 seconds. There's potentially
no avoiding that. But then you change a single line in the docs, and that subsequent
build also takes 80 seconds. That subsequent build should only take a second or two.
