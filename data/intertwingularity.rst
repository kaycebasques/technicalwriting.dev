.. _intertwingularity:

==============================================
Exploring the intertwingularity of a docs site
==============================================

.. _Ted Nelson: https://en.wikipedia.org/wiki/Ted_Nelson
.. _link: https://en.wikipedia.org/wiki/Hyperlink
.. _Computer Lib/Dream Machines: https://en.wikipedia.org/wiki/Computer_Lib/Dream_Machines
.. _PDF: https://worrydream.com/refs/Nelson_T_1974_-_Computer_Lib,_Dream_Machines.pdf

`Intertwingularity <https://en.wikipedia.org/wiki/Intertwingularity>`__ is a
term coined by `Ted Nelson`_, the same guy who coined the term `link`_.
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

My first thought after readin gthat

Now, I don't know about you, but when I read stuff like that, my mind
immediately jumps to one conclusion:

.. figure:: /_static/boat.png
   :alt: I should build a web crawler.

.. _intertwingularity-mesh:

------------------
Why crawl the Mesh
------------------

.. _Mesh: https://www.w3.org/History/1989/proposal.html

(`Mesh`_ was Tim Berners-Lee's original name for the world wide web.
Mesh computing is dead, long live mesh computing!)

.. _PageRank: https://en.wikipedia.org/wiki/PageRank
.. _backlinks: https://en.wikipedia.org/wiki/Backlink

Short story long, I'm building a web crawler so that I can track how
pages in my docs site link to each other and to the outside web more
broadly. If a lot of my docs pages link to some particular page, then
that page is probably important. `PageRank`_ Lite, basically, except
with much more focus on intra-site `backlinks`_.

Why care about links
====================

.. _technical writer: https://en.wikipedia.org/wiki/Technical_writer
.. _pigweed.dev: https://pigweed.dev

Building a web crawler gives me another way to answer one of the
fundamental questions of technical writing:

  **What pages of my docs site are important?**

I can't give every page on my docs site the same level of tender loving
care. I must decide which pages get more of my time and energy and which ones
get less.

There is no single approach that provides a full answer to the question.
There are, however, lots of approaches that provide *partial* answers.

Pageviews
---------

.. _goto: https://en.wikipedia.org/wiki/Goto

Pageviews is a `goto`_ approach for deciding what pages are important.
My website analytics tell me what pages are visited the most. I infer that
the most-visited pages are important because this is where my users literally
spend the most time. So I review the top 10 most-visited pages, making sure
they're all high-quality. But then I face a problem. The next 50 pages all
have roughly the same amount of pageviews. I don't have time to review all
50 of these pages. How do I decide which ones are important?

Backlinks
---------

.. _load-bearing: https://en.wikipedia.org/wiki/Load-bearing_wall
.. _triangulated: https://en.wikipedia.org/wiki/Triangulation_(social_science)

When the pageview data is ambiguous, links can help me determine which
pages have the most `load-bearing`_ content. Suppose that Pages A, B, and
C all link to Page D. There's probably some important content on Page D.
Pages with more backlinks (e.g. Page D) should probably be prioritized
above pages with less backlinks.

.. csv-table::
   :header: "Page ID", "Number of pageviews", "Number of backlinks"

   "X", "1000", "17"
   "Y", "1000", "4"
   "Z", "1000", "36"

Given only the pageviews data, it's hard to tell whether to prioritize
X, Y, or Z. When the pageviews data is `triangulated`_ with the backlink
data it's easy to tell that Z should get prioritized, then X, then Y.

---------
Prior art
---------

* `Linkback <https://en.wikipedia.org/wiki/Linkback>`_
* `Referer <https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer>`_
* `Refback <https://en.wikipedia.org/wiki/Refback>`_
* `Trackback <https://en.wikipedia.org/wiki/Trackback>`_
* `Pingback <https://en.wikipedia.org/wiki/Pingback>`_
* `Webmention <https://en.wikipedia.org/wiki/Webmention>`_
* `Octothorpes <https://octothorp.es/docs>`_

---------------
To be continued
---------------

This post is a work in progress.

-----------------
Extra credit meme
-----------------

.. figure:: /_static/singularity.png
