.. _link-text-automation:

==============================
Link text automation in Sphinx
==============================

.. _explicit target: https://docs.readthedocs.io/en/stable/guides/cross-referencing-with-sphinx.html#explicit-targets
.. _Sphinx: https://www.sphinx-doc.org
.. _Structure link text: https://developers.google.com/style/link-text#structure-link-text
.. _A Link is a Promise: https://www.nngroup.com/articles/link-promise/
.. _"Learn More" Links\: You Can Do Better: https://www.nngroup.com/articles/learn-more-links/
.. _Better Link Labels\: 4 Ss for Encouraging Clicks: https://www.nngroup.com/articles/better-link-labels/
.. _toil: https://sre.google/sre-book/eliminating-toil/
.. _no raisin: https://www.youtube.com/watch?v=V3ZUhWuiQ20
.. _MyST: https://myst-parser.readthedocs.io/en/latest/
.. _reStructuredText: https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html
.. _IfThisThenThat: https://fuchsia.dev/fuchsia-src/development/source_code/presubmit_checks#ifthisthenthat
.. _If I wasn't so lazy: https://www.youtube.com/watch?v=siGFs_NhcOk

2023 Mar 30

Sphinx's approach to link text improves docs maintainability and reduces
toil.

(Throughout this post I use the term **docs site systems** to refer to the
static site generators (SSGs) and content management systems (CMSs) that
most documentation websites are built on top of: Docusaurus, Jekyll, Sphinx,
WordPress, and so on.)

----------
Background
----------

The Nielsen Norman Group has done quite a bit of research on how to create
effective link text:

* `A Link is a Promise`_
* `"Learn More" Links: You Can Do Better`_
* `Better Link Labels: 4 Ss for Encouraging Clicks`_

Long story short, effective link text is specific, sincere, substantial, and
succinct.

The `Structure link text`_ section of the Google Developer Documentation Style
Guide has a helpful rule-of-thumb that gets you most of the way there without
having to think much: just use the exact text of the title or section heading
that you're referencing.

-------
Problem
-------

In most docs site systems, you have to manually create and maintain the link text.
For example, over in ``guide.md`` we might have a section heading like this:

.. code-block:: none

   ## How to enable text compression { #compression }

(Assume that ``{ #compression }`` is a non-standard feature that allows you
to define the ID for that section heading.)

Over in ``reference.md`` we link to this section like this:

.. code-block:: none

   See [How to enable text compression](./guide#compression).

(Assume that both docs live in the same directory.)

The link text in ``reference.md`` will rot over time. Someone will change the
section heading in ``guide.md`` from ``How to enable text compression`` to
something else. They will forget to also update the link text in ``reference.md``.
Or perhaps they don't even know that ``reference.md`` links to ``guide.md``.

This is textbook `toil`_. The link text in ``reference.md`` should always
stay synchronized with the true section heading text in ``guide.md``.

--------
Solution
--------

`Sphinx`_ provides an automated solution for ensuring that link text
always stays in-sync with the actual section heading text.

Over in ``guide.rst`` you create an [explicit target] (``.. _compression:``)
to the section heading:

.. code-block:: rst

   .. _compression:

   ==============================
   How to enable text compression
   ==============================

(The filename changed from ``guide.md`` to ``guide.rst`` because most Sphinx sites
use `reStructuredText`_ (reST), not Markdown. Sphinx also supports a Markdown-y
syntax called `MyST`_.)

And then in ``reference.rst`` you simply add a reference to that section heading:

.. code-block:: rst

   See :ref:`compression`.

This gets replaced with ``How to enable text compression`` at build time.

Another huge benefit of this approach is that the build system warns you when
you're linking to a section that no longer exists:

.. code-block:: none

   $ make html
   Running Sphinx v6.1.3
   ...
   /.../reference.rst:4: WARNING: undefined label: 'compression'

-----------------------------------------------------
The status of this feature in other docs site systems
-----------------------------------------------------

`If I wasn't so lazy`_ I would list out the exact status of this feature on
other docs site systems. I am not going to do that, however, because, as previously
alluded to, I am lazy. I don't mean to imply that this feature is not supported
on any other docs site systems. I am sure there is some other docs site system out there that
has "seen the light." From what I can tell, though, most do not.
