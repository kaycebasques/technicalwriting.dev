.. _searchbox:

============================
Field research: search boxes
============================

.. _field research: https://en.wikipedia.org/wiki/Field_research
.. _search box: https://en.wikipedia.org/wiki/Search_box

This page contains my `field research`_ around the following questions:

* Where should I put the `search box`_ on my documentation site?
* What text should I put inside the search box?
* What should happen when I type stuff into the search box?
* What should the search results page look like?

---------
Libraries
---------

Requests
========

On the Requests homepage, there's a search box at the bottom of the site nav.
There's no placeholder text within the search box. The label above the search
box is ``Quick Search``. There's a submit button to the right of the search
box with the text ``Go``.

.. image:: /_static/requests-home-20240217.png

On the quickstart page the search box is below-the-fold.

.. image:: /_static/requests-quickstart-20240217.png

Typing ``test`` into the search box does nothing.

The search results page presents the total number of matches and previews of
where the search term occurs in the top matches. It seems to highlight the
query term up to 3 times in each doc.

.. image:: /_static/requests-serp-20240217.png

---------
Languages
---------

Rust
====

The Rust homepage doesn't have a search box.

.. image:: /_static/rust-home-20240217.png

The quickstart page also doesn't have a search box.

.. image:: /_static/rust-quickstart-20240217.png

The search box for rustdoc, however, takes up pretty much the entire header.

.. image:: /_static/rustdoc-home-20240217.png

The search results page presents a table of matches. The default tab is
``In Names`` but there's also a tab for ``In Parameters`` and ``In Return
Types``.

.. image:: /_static/rustdoc-serp-20240217.png

There's also a search help modal that shows keyboard shortcuts and structured
search tricks.

.. image:: /_static/rustdoc-searchhelp-20240217.png

---------
Platforms
---------

Stripe
======

The Stripe homepage has a search box in the center of the header. There's a
magnifying glass icon. The placeholder text is ``Search the docs``. There's
also a forward slash character (``/``) to indicate the keyboard shortcut for
accessing the search box.

.. image:: /_static/stripe-home-20240217.png

The quickstart page has the same search box UI as the homepage.

.. image:: /_static/stripe-quickstart-20240217.png

Typing ``test`` into the search box yields a search results modal. It seems
to always return 7 results max. Below the results there's a single code
example and a link to view more code examples. There's no "view more results"
UI element; perhaps the Stripe site does not have the concept of a search
results page?

.. image:: /_static/stripe-searchbox-20240217.png

Clicking ``See more code examples`` doesn't show a search results page but
rather another modal.

.. image:: /_static/stripe-codesamples-20240217.png

MDN Web Docs
============

The MDN homepage has 2 search boxes: a small one on the right side of the
header and a big one in the middle of the splash page content. Both search
boxes have a magnifying glass icon. The placeholder text in the small search
box is just an underscore character (``_``). Typing ``_`` does not seem to be
a keyboard shortcut for accessing the search box.

.. image:: /_static/mdn-home-20240217.png

The quickstart page has the same small search box in the header as the
homepage.

.. image:: /_static/mdn-quickstart-20240217.png

Typing ``test`` into the search box yields a modal with 5 results and a "view
more results" UI element.

.. image:: /_static/mdn-searchbox-20240217.png

The search results page shows the total number of matches, previews of where
the term occurs in the top matches. It also presents options to filter by
relevance or popularity. Presumably the "best" filter is a combination of
relevance and popularity?

.. image:: /_static/mdn-serp-20240217.png
