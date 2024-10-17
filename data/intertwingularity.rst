.. _intertwingularity:

==============================================
Exploring the intertwingularity of a docs site
==============================================

.. _Ted Nelson: https://en.wikipedia.org/wiki/Ted_Nelson
.. _link: https://en.wikipedia.org/wiki/Hyperlink
.. _Computer Lib / Dream Machines: https://en.wikipedia.org/wiki/Computer_Lib/Dream_Machines
.. _PDF: https://worrydream.com/refs/Nelson_T_1974_-_Computer_Lib,_Dream_Machines.pdf

`Intertwingularity <https://en.wikipedia.org/wiki/Intertwingularity>`__ is a
term coined by `Ted Nelson`_, the same guy who coined the term `link`_.\ :sup:`1`
In `Computer Lib / Dream Machines`_ (`PDF`_) Nelson explains intertwingularity
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
care. Especially now that I'm soon to be a first-time dad (!!) I must decide
which pages get more of my time and energy and which ones get less.

There is no single approach that provides a *full* answer to this question.
There are, however, lots of approaches that provide *partial*
answers.

Pageviews
---------

Pageviews is one such partial-answer approach.
My website analytics tell me what pages are visited the most. I infer that
the most-visited pages are important because this is where my users literally
spend the most time. But what if each of the top 5 pages has the same amount
of pageviews and I only have time to review 3? Which 3 do I prioritize?

.. csv-table::
   :header: "Page ID", "Pageviews"

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
some idea (or information, or knowledge, or whatever) on Page D that Pages A, B,
and C all depend on.

.. _triangulate: https://en.wikipedia.org/wiki/Triangulation_(social_science)

Returning to the docs review prioritization problem, when I `triangulate`_
the pageview data with the backlink data, it becomes easier to decide which 3
to prioritize:

.. csv-table::
   :header: "Page ID", "Pageviews", "Backlinks"

   "V", "1000", "20"
   "W", "1000", "15"
   "X", "1000", "31"
   "Y", "1000", "3"
   "Z", "1000", "1"

(The correct answer in this example is pages X, V, and W, in that order.)

Networked knowledge
===================

.. _Too Big To Know: https://en.wikipedia.org/wiki/Too_Big_to_Know

I have another motivation for studying backlinks. I simply want to know
more about how the ideas within my docs site relate and connect to each
other. The concept of *networked knowledge* from `Too Big To Know`_
is pretty cool:

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

.. _GPT-3 paper: https://arxiv.org/pdf/2005.14165
.. _Common Crawl: https://commoncrawl.org/

:sup:`2` While it's true that the network has not spontaneously developed
consciousness (as far as I'm aware), networked knowledge played a major
role in the rise of large language models. From the `GPT-3 paper`_:
"the majority of our data is derived from raw `Common Crawl`_ with only quality-based
filtering"

---------------------
Anatomy of my crawler
---------------------

I got the core crawler logic working in about 200 lines of Python code,
leaning heavily on ``requests`` for HTTP stuff and ``beautifulsoup4`` for scraping
stuff. Here's the gist of my crawler's logic:

* Designate an entrypoint URL, e.g. ``https://technicalwriting.dev``. URLs
  that start with this entrypoint are considered intra-site. URLs that don't
  start with the entrypoint are considered external.
* Grab all links that are found within the main content\ :sup:`3` of the entrypoint.
* Whenever an intra-site URL is found, visit and scrape that page's links.
* External URLs just need to be noted and tracked. They don't need to be
  visited or scraped.

:sup:`3` Don't scrape the whole page! Your stats will get messed up. E.g.
every page of your docs site probably includes a header, and that header
probably always links back to your homepage. Your homepage will get listed
as the most load-bearing page, when in reality it's rare for the main content
of a docs page to link back to the homepage.

--------------------------
Analyzing a real docs site
--------------------------

After quite a bit of sighing in frustration and muttering to myself I was able
to fully crawl the docs site that I work on, `pigweed.dev <https://pigweed.dev>`_, and
I have to admit: the results are pretty fascinating. There were quite a few surprises.
I was honestly expecting the conclusion of this experiment to be "yeah… I tried that
backlink approach and nothing interesting came up."

Here are the top 10 most load-bearing pages:

.. csv-table::
   :header: Backlinks, URL

   "55","`/pw_protobuf/docs.html <https://pigweed.dev/pw_protobuf/docs.html>`_"
   "42","`/pw_status/reference.html <https://pigweed.dev/pw_status/reference.html>`_"
   "36","`/docs/module_structure.html <https://pigweed.dev/docs/module_structure.html>`_"
   "24","`/pw_chrono/docs.html <https://pigweed.dev/pw_chrono/docs.html>`_"
   "23","`/pw_function/docs.html <https://pigweed.dev/pw_function/docs.html>`_"
   "21","`/pw_log/docs.html <https://pigweed.dev/pw_log/docs.html>`_"
   "18","https://bazel.build/concepts/build-ref"
   "17","`/pw_log_tokenized/docs.html <https://pigweed.dev/pw_log_tokenized/docs.html>`_"
   "17","`/pw_tokenizer/docs.html <https://pigweed.dev/pw_tokenizer/docs.html>`_"
   "17","`/pw_rpc <https://pigweed.dev/pw_rpc>`_"

(``55`` backlinks for ``/pw_protobuf/docs.html`` means that
55 other pages linked to ``/pw_protobuf/docs.html``.)

Here's what's surprising:

* ``/pw_protobuf/docs.html``, ``/pw_chrono/docs.html``, and ``/pw_function/docs.html`` are fairly
  popular in terms of pageviews but I did not expect them to have top spots in terms of
  backlinks. We have been gradually updating our `module <https://pigweed.dev/docs/glossary.html#module>`_
  docs to follow our `guidelines <https://pigweed.dev/docs/contributing/docs/modules.html>`_.
  I did not consider ``pw_chrono`` and ``pw_function`` to be top-priority modules,
  but this data suggests that maybe I should.
* An external link (``https://bazel.build/concepts/build-ref``) is
  one of our most backlinked pages! It's in my own self-interest to
  make sure that this external doc is high-quality. If I had to persuade
  my manager to let me update that external doc, I could cite this concrete
  data for rationale.
* ``https://pigweed.dev/pw_rpc`` is one of our most popular pages in
  terms of pageviews yet in terms of backlinks it's only #10.

--------
Appendix
--------

Prior art
=========

There are lot of web platform features and third-party tools related to
backlinks. I didn't see anything out there that provided what I needed.
I still would have built my own web crawler because part of the goal here
was just to have fun.

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
