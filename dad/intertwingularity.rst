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
I just learned that fact and had to work it into this post somehow.)

.. _technical writer: https://en.wikipedia.org/wiki/Technical_writer
.. _pigweed.dev: https://pigweed.dev

Building a web crawler gives me another way to answer one of the
fundamental questions of technical writing:

  **What pages of my docs site are important?**

.. _TLC: https://www.merriam-webster.com/dictionary/tender%20loving%20care

As a technical writer I think about this question a lot because of one
simple law of nature: the rate of change in a project's
data/metadata/information/knowledge/wisdom ("knowledge" for short) often far
exceeds the resources allocated for maintaining all that knowledge. I.e. I
can't give every page the same level of tender loving care (TLC).
I must decide which ones get more TLC and which ones get less.

There is no single approach that can *fully* answer the fundamental question
("what pages of my docs site are important?"). There are, however, lots of
approaches that provide *partial* answers.

.. _Every Page Is Page One: https://everypageispageone.com/the-book/

Pageviews is one such approach. Your website analytics tell you what pages
are visited the most. You infer that the most-visited pages are important
because this is where your users literally spend the most time.

Pageviews, however, can't tell you much about how your pages relate to each
other. This is where links and web crawlers come in. Think of each page as
a set of ideas. Links let that page connect itself to other related ideas.
`Every Page Is Page One`_ calls this "subject affinity":

  You should be thinking of links not as citations or references but
  as the natural expression of every significant subject affinity in
  your content.

Links are the tangible manifestation of subject affinities:

  Web organization is always local... Each page has its own set of
  associations and affinities... The page locates itself in a semantic
  cluster formed by links and keywords.

.. _PageRank: https://en.wikipedia.org/wiki/PageRank

Short story long, I'm building a web crawler so that I can meticulously
track how the pages of my docs site link to each other and to the outside
web more broadly. E.g. if all of my docs pages link to some particular
page, then that page is probably very important. `PageRank`_ Lite,
basically, except with much more focus on intra-site links.

---------------
To be continued
---------------

This post is a work in progress.

----------
Bonus meme
----------

.. figure:: /_static/singularity.png
