.. _intertwingularity:

==============================================
Exploring the intertwingularity of a docs site
==============================================

.. _Ted Nelson: https://en.wikipedia.org/wiki/Ted_Nelson
.. _link: https://en.wikipedia.org/wiki/Hyperlink
.. _Computer Lib/Dream Machines: https://en.wikipedia.org/wiki/Computer_Lib/Dream_Machines
.. _PDF: https://worrydream.com/refs/Nelson_T_1974_-_Computer_Lib,_Dream_Machines.pdf

`Intertwingularity <https://en.wikipedia.org/wiki/Intertwingularity>`__ is a
term coined by `Ted Nelson`_, the same guy who coined the term `link`_.\ :sup:`1`
In `Computer Lib/Dream Machines`_ (`PDF`_) Nelson explains intertwingularity
like this:

  EVERYTHING IS DEEPLY INTERTWINGLED. In an important sense there are no
  "subjects" at all; there is only all knowledge, since the cross-connections
  among the myriad topics of this world simply cannot be divided up neatly.

That same book (more of a self-published fever dream, really) hints at how
links enable us to get closer to the intertwingled nature of knowledge:

  Hierarchical and sequential structures, especially popular since Gutenberg,
  are usually forced and artificial. Intertwingularity is not generally
  acknowledged—people keep pretending they can make things hierarchical,
  categorizable and sequential when they can't.

After reading those quotes, my first thought was:

.. figure:: /_static/boat.png
   :alt: I should build a web crawler.

.. _As We May ThinK: https://dl.acm.org/doi/pdf/10.1145/227181.227186
.. _Memex: https://en.wikipedia.org/wiki/Memex

:sup:`1` Nelson is credited with coining the term "link" but the underlying
idea traces back to `As We May Think`_ by Vannevar Bush and his hypothetical
`Memex`_ device.

.. _intertwingularity-background:

----------
Background
----------

.. _PageRank: https://en.wikipedia.org/wiki/PageRank
.. _backlinks: https://en.wikipedia.org/wiki/Backlink

Short story long, I'm building a web crawler so that I can track how
pages in my docs site link to each other and to the outside web more
broadly. If a lot of my docs pages link to some particular page, then
that page is probably important. `PageRank`_ Lite, basically, except
with much more focus on intra-site `backlinks`_.

(Also, I'm building a web crawler because it's fun. Try it!)

Importance
==========

.. _technical writer: https://en.wikipedia.org/wiki/Technical_writer
.. _pigweed.dev: https://pigweed.dev

Building a web crawler gives me another way to answer one of the
fundamental questions of technical writing:

  **What pages of my docs site are important?**

I can't give every page on my docs site the same level of tender loving
care. I must decide which pages get more of my time and energy and which ones
get less.

There is no single approach that provides a *full* answer to this question.
There are, however, lots of approaches that provide *partial*
answers.

Pageviews
---------

Pageviews is one such partial-answer approach.
My website analytics tell me what pages are visited the most. I infer that
the most-visited pages are important because this is where my users literally
spend the most time. But what if each of the top 10 pages has the same amount
of pageviews and I only have time to review 5? Which 5 do I prioritize?

.. csv-table::
   :header: "Page ID", "Pageviews"

   "Q", "1000"
   "R", "1000"
   "S", "1000"
   "T", "1000"
   "U", "1000"
   "V", "1000"
   "W", "1000"
   "X", "1000"
   "Y", "1000"
   "Z", "1000"

Backlinks
---------

.. _load-bearing: https://en.wikipedia.org/wiki/Load-bearing_wall

When the pageview data is ambiguous, links can help me determine which
pages have the most `load-bearing`_ content. Suppose that Pages A, B, and
C all link to Page D. There's probably some important content on Page D.
Pages with more backlinks (e.g. Page D) should probably be prioritized
above pages with less backlinks. Think about it in terms of user journey.
Users on Pages A, B, and C all have a chance of ending up on Page D. There's
some idea (or data, or knowledge, or whatever) on Page D that Pages A, B, and
C all depend on.

.. _triangulate: https://en.wikipedia.org/wiki/Triangulation_(social_science)

Returning to the docs review prioritization problem, when I `triangulate`_
the pageview data with the backlink data, it becomes easier to decide which 5
to prioritize:

.. csv-table::
   :header: "Page ID", "Pageviews", "Backlinks"

   "Q", "1000", "4"
   "R", "1000", "11"
   "S", "1000", "17"
   "T", "1000", "2"
   "U", "1000", "26"
   "V", "1000", "20"
   "W", "1000", "15"
   "X", "1000", "31"
   "Y", "1000", "3"
   "Z", "1000", "1"

Networked knowledge
===================

.. _Too Big To Know: https://en.wikipedia.org/wiki/Too_Big_to_Know

I have another motivation for studying backlinks. I simply want to know
more about how the ideas within my docs site relate and connect to each
other. The concept of *networked knowledge* from `Too Big To Know`_
fascinates me:

  The change in the infrastructure of knowledge is altering knowledge's
  shape and nature. As knowledge becomes networked, the smartest person
  in the room isn't the person at the front lecturing us, and isn't the
  collective wisdom of those in the room. The smartest person in the
  room is the room itself: the network that joins the people and ideas
  in the room, and connects to those outside of it. It's not that the
  network is becoming a conscious super-brain\ :sup:`2`. Rather knowledge is
  becoming inextricable from—literally unthinkable without— the network
  that enables it. Our task is to learn how to build smart rooms—that is,
  how to build networks that make us smarter...

:sup:`2` David Weinberger 

---------------------
Anatomy of my crawler
---------------------

I got the core crawler logic working in about 200 lines of Python code,
depending on ``requests`` for HTTP stuff and ``beautifulsoup4`` for scraping
stuff. Here's the gist of the logic:

* Designate an entrypoint URL, e.g. ``https://technicalwriting.dev``. URLs
  that start with this entrypoint are considered intra-site. URLs that don't
  start with the entrypoint are considered external.
* Grab all links that are found within the main content of the entrypoint.
* Whenever an intra-site URL is found, visit and scrape that page's links.
* External URLs just need to be noted and tracked. They don't need to be
  visited or scraped.

---------------
To be continued
---------------

This post is a work in progress.

--------
Appendix
--------

Prior art
=========

There are lot of web platform features and third-party tools related to
backlinks.

* `Linkback <https://en.wikipedia.org/wiki/Linkback>`_
* `Referer <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer>`_
* `Refback <https://en.wikipedia.org/wiki/Refback>`_
* `Trackback <https://en.wikipedia.org/wiki/Trackback>`_
* `Pingback <https://en.wikipedia.org/wiki/Pingback>`_
* `Webmention <https://en.wikipedia.org/wiki/Webmention>`_
* `Octothorpes <https://octothorp.es/docs>`_
* `Ahrefs Backlink Checker <https://ahrefs.com/backlink-checker/>`_

Extra credit meme
=================

.. figure:: /_static/singularity.png
