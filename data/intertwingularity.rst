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
I just learned that fact and had to work it into this post somehow.
Mesh computing is dead, long live mesh computing!)

.. _PageRank: https://en.wikipedia.org/wiki/PageRank

Short story long, I'm building a web crawler so that I can meticulously
track how the pages of my docs site link to each other and to the outside
web more broadly. E.g. if all of my docs pages link to some particular
page, then that page is probably important. `PageRank`_ Lite,
basically, except with much more focus on intra-site links.

A longer explanation
====================

.. _technical writer: https://en.wikipedia.org/wiki/Technical_writer
.. _pigweed.dev: https://pigweed.dev

Building a web crawler gives me another way to answer one of the
fundamental questions of technical writing:

  **What pages of my docs site are important?**

.. _TLC: https://www.merriam-webster.com/dictionary/tender%20loving%20care

As a technical writer I think about this question a lot because of one
simple law of nature: the rate of change in a project's
data / metadata / information / knowledge / wisdom (DMIKW\ :sup:`1`)
often far exceeds the resources allocated for maintaining all that DMIKW.
I.e. I can't give every page on my docs site the same level of tender loving
care. I must decide which pages get more of my time and energy and which ones
get less.

There is no single approach that can *fully* answer the fundamental question,
"what docs pages are important?" There are, however, lots of approaches that
provide *partial* answers.

.. _Every Page Is Page One: https://everypageispageone.com/the-book/

Studying pageviews is one such approach. Your website analytics tell you what pages
are visited the most. You infer that the most-visited pages are important
because this is where your users literally spend the most time. That is good
and useful data.

Pageviews, however, can't tell you much about how your docs pages relate
to *each other*. Links can. Think of each docs page as a jumble of DMIKW.
When a docs page links to another page, it's really just one jumble of DMIKW
connecting itself to another jumble of DMIKW located elsewhere.
`Every Page Is Page One`_ calls this "subject affinity":

  You should be thinking of links not as citations or references but
  as the natural expression of every significant subject affinity in
  your content.

Links are the tangible manifestation of subject affinities:

  Web organization is always local... Each page has its own set of
  associations and affinities... The page locates itself in a semantic
  cluster formed by links and keywords.

When I think of links as the means of ideas connecting to each other,
I start to feel some of the reverence for links that Ted "Self-Published
Fever Dream" Nelson probably also felt when he came up with the term.\ :sup:`2`

:sup:`1` This acronym sucks but it's important to remember that
technical writing isn't really about documentation. It's not even
just about knowledge management. It's about managing the firehose of data /
metadata / information / knowledge / wisdom that your project incessantly
generates. Hence why I'm forcing you to look at this unwieldy DMIKW
acronym. Suggestions on more catchy ways to get this idea across are very
much welcome.

.. _As We May Think: https://dl.acm.org/doi/pdf/10.1145/227181.227186

:sup:`2` Although Nelson coined the term "link" the genesis of the idea
itself seems to trace back to `As We May Think`_ by Vannevar Bush.

---------------
To be continued
---------------

This post is a work in progress.

-----------------
Extra credit meme
-----------------

.. figure:: /_static/singularity.png
