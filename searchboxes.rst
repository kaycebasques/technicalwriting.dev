.. _searchboxes:

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

See :ref:`methodology` for background on my research approach.

-------
Summary
-------

* The search box is usually in the header. The position within the header
  varies. Some sites have it in the center. Others have it on the right. None
  had it on the left. Some have it take up the entire header.
* Most sites keep the position of the search box consistent across pages.
* Not all sites put an icon in their search box, but when they do, it's
  **always** a magnifying glass.
* The placeholder text varies a lot. Some search boxes have no placeholder
  text. The single word ``Search`` is the greatest common denominator.
* Search boxes often expand when you focus them.
* Results are usually shown immediately after typing.
* Some sites only surface results through modals i.e. they don't have
  dedicated search results pages.
* The keyboard shortcut used for accessing the search box is not standardized.
  Some sites use :kbd:`S`, others use :kbd:`/`, etc.
* There seems to be a lot of variety in search algorithms. Some sites seem to
  only check the doc title. Others check both the title and content. Others
  use popularity as a ranking signal.

--------------
Field research
--------------

For every site I looked at (something close to a) homepage and (something close
to a) quickstart tutorial.

Libraries
=========

Requests
--------

On the Requests homepage, there's a search box at the bottom of the site nav.
There's no placeholder text within the search box. The label above the search
box is ``Quick Search``. There's a submit button to the right of the search
box with the text ``Go``.

.. image:: /_static/requests-home-20240217.png

On the quickstart page the search box is below-the-fold.

.. image:: /_static/requests-quickstart-20240217.png

Typing ``test`` into the search box does nothing.

The search results page presents the total number of matches and previews of
where the search term occurs in the top matches. It seems to highlight 3
sections where there's a match in each doc.

.. image:: /_static/requests-serp-20240217.png

React
-----

The React homepage has a search box taking up most of the header. On the far
left of the search box there's a magnifying glass icon. The placeholder text is
``Search``. The keyboard shortcut for accessing the search box (:kbd:`Ctrl+K`)
is shown on the far right.

.. image:: /_static/react-home-20240218.png

The quickstart page has the same search box UI as the homepage.

.. image:: /_static/react-quickstart-20240218.png

Focusing the search box presents a modal. Typing ``test`` into the search box
yields a list of matches. The section headings (e.g. ``REACT V18.``) are the
doc titles. The query matches are highlighted in the brand color. The search
engine is powered by Algolia. An ``X`` icon shows up in the search box after
you enter text.

.. image:: /_static/react-searchbox-20240218.png

CLI tools
=========

Git
---

The Git homepage has a search box in the header. There's a magnifying glass
icon. The placeholder text is ``Search entire site...``. 

.. image:: /_static/git-home-20240218.png

Git doesn't seem to have a quickstart page; this reference page seemed like
the next best choice. It has the same search box UI as the homepage.

.. image:: /_static/git-reference-20240218.png

Typing ``test`` into the search box yields a dropdown of results. The dropdown
is structured like a table. The first 10 or so results are ``git`` commands.
The next 10 or so results seem to be section titles from an authoritative
book.

.. image:: /_static/git-searchbox-20240218.png

cURL
----

The cURL homepage doesn't have a search box:

.. image:: /_static/curl-home-20240218.png

Neither does the quickstart page:

.. image:: /_static/curl-quickstart-20240218.png

Frameworks
==========

.NET
----

The .NET homepage has a magnifying glass icon on the right side of the header
that represents the search box. 

.. image:: /_static/dotnet-home-20240218.png

The quickstart page has the same search box UI.

.. image:: /_static/dotnet-quickstart-20240218.png

Focusing the search box causes it to take up the entire header. The magnifying
glass icon becomes an ``X`` icon. Typing ``test`` seems to show keyphrases
related to the search query.

.. image:: /_static/dotnet-searchbox-20240218.png

The search results page is very similar to a Google Search results page.
Query matches are bold in the descriptions, but not in the titles. Below the
title you see the absolute path to each doc. You can filter by content type
or product. ``.NET`` is not selected in the product filter, even though that's
where I came from.

.. image:: /_static/dotnet-serp-20240218.png

Unreal
------

The Unreal homepage has 2 search boxes. In the header there's a magnifying
glass icon to the right. At the top of the content area, to the right, there's
another search box. The placeholder text for that one is
``Search Documentation...``. It also has a magnifying glass icon. 

.. image:: /_static/unreal-home-20240218.png

The quickstart page has the same search box UI.

The search box in the header seems broken; when I typed ``test`` and pressed
:kbd:`Enter` nothing happened. Focusing the other search box caused a blue
border around it. Typing ``test`` didn't cause any changes i.e. no dropdown
or modal appeared.

.. image:: /_static/unreal-quickstart-20240218.png

The search results page shows the number of results, the usual list of titles
and descriptions, and query matches in bold. It also lets you filter content
to only see stuff from certain parts of the ecosystem e.g. news, documentation,
forums, etc.

.. image:: /_static/unreal-serp-20240218.png

Languages
=========

Rust
----

The Rust homepage doesn't have a search box.

.. image:: /_static/rust-home-20240217.png

The quickstart page also doesn't have a search box.

.. image:: /_static/rust-quickstart-20240217.png

The search box for rustdoc, however, takes up pretty much the entire header.
The keyboard shortcut for accessing the search box is ``S``. The placeholder
text is ``Click or press 'S' to search, '?' for more options...``.

.. image:: /_static/rustdoc-home-20240217.png

The search results page presents a table of matches. The default tab is
``In Names`` but there's also a tab for ``In Parameters`` and ``In Return
Types``.

.. image:: /_static/rustdoc-serp-20240217.png

There's also a search help modal (keyboard shortcut: ``?``) that shows more
keyboard shortcuts and structured search tricks.

.. image:: /_static/rustdoc-searchhelp-20240217.png

Java
----

The Java homepage has a search box on the far right of the header. There's a
magnifying glass icon on the left side of the search box. There's no
placeholder text in the search box.

.. image:: /_static/java-home-20240218.png

The quickstart page has the same search box UI.

.. image:: /_static/java-quickstart-20240218.png

The search box expands when you focus it. Typing ``test`` yields a list of
results very similar to the old-school Google SERPs. Each section heading
is a document title, and these are styled like classic links. Below the title
there is a brief summary of the page. The query is highlighted in blue if it
occurs in the title or the summary. An ``X`` icon shows up on the far right
of the search box after you enter text.

.. image:: /_static/java-searchbox-20240218.png

Go
--

The Go homepage doesn't have a search box:

.. image:: /_static/go-home-20240218.png

Neither does the quickstart page:

.. image:: /_static/go-quickstart-20240218.png

Platforms
=========

Stripe
------

The Stripe homepage has a search box in the center of the header. There's a
magnifying glass icon. The placeholder text is ``Search the docs``. There's
also a forward slash character (``/``) to indicate the keyboard shortcut for
accessing the search box.

.. image:: /_static/stripe-home-20240217.png

The quickstart page has the same search box UI as the homepage.

.. image:: /_static/stripe-quickstart-20240217.png

Typing ``test`` into the search box yields a search results modal. It seems
to always return 7 results max. Below the results there's a single code
example and a link to view more code examples. There's no dedicated SERP.
An ``X`` icon shows up in the far right of the search box after you enter text.

.. image:: /_static/stripe-searchbox-20240217.png

Clicking ``See more code examples`` doesn't show a search results page but
rather another modal.

.. image:: /_static/stripe-codesamples-20240217.png

MDN Web Docs
------------

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
more results" UI element. An ``X`` icon shows up at the far right of the search
box after you enter text.

.. image:: /_static/mdn-searchbox-20240217.png

The search results page shows the total number of matches and previews of where
the term occurs in the top matches. It also presents options to filter by
relevance or popularity. Presumably the "best" filter is a combination of
relevance and popularity?

.. image:: /_static/mdn-serp-20240217.png

Amazon Web Services
-------------------

The search box on the AWS homepage takes up most of the header. There's a
magnifying glass icon and the placeholder text is
``Search in AWS documentation``. No keyboard shortcut is mentioned.

.. image:: /_static/aws-home-20240218.png

Typing ``test`` into the search box shows a dropdown of results. The results
seem to be queries that other users entered? An ``X`` icon shows up at the far
right after you enter text.

.. image:: /_static/aws-home-searchbox-20240218.png

The quickstart page that I arbitrarily picked has only a magnifying glass icon
to represent the search box. The location of the search box moved to the right.

.. image:: /_static/aws-quickstart-20240218.png

Typing ``test`` yields a dropdown of results. The results seem to be organized
by content type e.g. "blogs". The search engine seems to look for the query
term in the doc title.

.. image:: /_static/aws-quickstart-searchbox-20240218.png

The search results page highlights query matches in bold. Products like
``Hourglass Smart Test Job Runner`` seem to show the price of the product
below the title. You can narrow your search by content type (``Documentation``,
``AWS Blogs``, etc.). You can sort by relevance, title, or date. The results
page shows you how many query matches there were and it lets you choose whether
to show 25, 50, or 100 results per page.
