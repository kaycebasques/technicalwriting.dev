.. _home:

====================
technicalwriting.dev
====================

Field notes from the frontier of technical writing.

.. _categories:

----------
Categories
----------

* :ref:`links`

* :ref:`ml`

* :ref:`sphinx`

* :ref:`strategy`

.. _analytics:

---------
Analytics
---------

* :ref:`sheets`. This tutorial shows you how to use Google Apps Script to
  export your Google Analytics data to Google Sheets. The data automatically
  updates every night. There’s also a custom menu item within Sheets to update
  the data on-demand. You can also optionally also expose the data over HTTPS
  to the public internet.

.. _links:

-----
Links
-----

* :ref:`link-text-automation`. A killer feature from Sphinx that more docs systems
  should adopt.

* :ref:`pdf`. Just append ``#page=X`` to your URL, where ``X`` is a placeholder
  for the page you want to link to.

* :ref:`intertwingularity`. I’m building a web crawler so that I can track how pages in my docs
  site link to each other and to the outside web more broadly. If a lot of my docs pages link to
  some particular page, then that page is probably important.

.. _ml:

----------------
Machine learning
----------------

.. _embeddings:

Embeddings
==========

* :ref:`underrated`. Machine learning (ML) has the potential to
  advance the state of the art in technical writing. No, I'm not talking
  about text generation models. The ML technology that might end up having the biggest
  impact on technical writing is **embeddings**. What embeddings offer to technical writers is
  **the ability to discover connections between texts at previously impossible scales**.

* :ref:`tasks`.

* :ref:`bookmarks`. Embeddings-related papers, projects, etc.

.. _ml-reviews:

Yearly reviews
==============

* :ref:`ml-reviews-2024`.

* :ref:`ml-reviews-2023`.

Miscellaneous
=============

* :ref:`pocketflow`.

* :ref:`gn`. I used Gemini 2.0 Flash and a little Python to automate
  the process of removing code from over 200 GN build files. Here's how it
  went.

* :ref:`hyperlint`.

.. _sphinx:

------
Sphinx
------

* :ref:`link-text-automation`. A killer feature from Sphinx that more docs systems
  should adopt.

* :ref:`sphazel-context`.

* :ref:`sphazel-tutorial`.

* :ref:`incremental`.

.. _strategy:

--------
Strategy
--------

* :ref:`challenges`. There are 3 intractable challenges in technical writing.
  I do not believe we will ever be able to completely solve these challenges
  using only the practices and technologies of the 2010s.

* :ref:`decisions`. Docs should aim to help people decide what to do.
  Only documenting procedures is usually not enough.

.. toctree::
   :hidden:

   404
   about
   analytics/index
   links/index
   ml/index
   sphinx/index
   strategy/index
