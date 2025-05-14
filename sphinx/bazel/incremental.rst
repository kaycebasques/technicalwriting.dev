.. _incremental:

==================================
Incremental Sphinx builds in Bazel
==================================

These are my notes on a docs infrastructure issue that I'm currently wrestling with.

(This post is a work in progress.)

-------
Problem
-------

.. _migrated pigweed.dev to Bazel: https://pigweed.dev/docs/blog/08-bazel-docgen.html

In Q1 2025 we `migrated pigweed.dev to Bazel`_. Our biggest developer experience
pain point is the lack of incremental builds. E.g. every docs build takes 80 seconds.
It's fine for the first docs build from scratch to take 80 seconds. There's potentially
no avoiding that. But then you change a single line in the docs, and that subsequent
build also takes 80 seconds. That subsequent build should only take a second or two.

----------
References
----------

* `Document how Sphinx's change detection works <https://github.com/sphinx-doc/sphinx/issues/11556>`_
* `sphinxdocs: implement content-based change detection plugin <https://github.com/bazel-contrib/rules_python/issues/2879>`_
