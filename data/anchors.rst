.. _anchors:

=========================
Cool anchors don't change
=========================

----------
Background
----------

See `Cool URIs don't change <https://www.w3.org/Provider/Style/URI>`_
and this `discussion <https://news.ycombinator.com/item?id=23865484>`_.

-------
Problem
-------

.. _linkcheck: https://www.sphinx-doc.org/en/master/usage/builders/index.html#module-sphinx.builders.linkcheck

I am using Sphinx's `linkcheck`_ builder to find and fix broken links.
``linkcheck`` is telling me that the link in the text below is broken:

.. code-block:: rst

   - **Not inherently modular**: Bazel expects the overwhelming majority of a
     C/C++ toolchain to be specified as part of a call to
     ``create_cc_toolchain_config_info()``. Because this is a Starlark method,
     there's a lot of flexibility with how you construct a toolchain config, but
     very little by way of existing patterns for creating something that is
     testable, sharable, or in other ways modular. The existing
     `tutorial for creating a C/C++ toolchain <https://bazel.build/tutorials/ccp-toolchain-config#configuring_the_c_toolchain>`_
     illustrates expanding out the toolchain definition as a no-argument Starlark
     rule.

--------
Solution
--------
