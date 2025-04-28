.. _hyperlint:

==============================
First impressions of Hyperlint
==============================

I'm doing a meet & greet with `Hyperlint <https://hyperlint.com>`__ founder
Bill Chambers today. I figured I should try out the product before we meet.
Here are my notes.

----------
Background
----------

Hyperlint describes itself like this:

  Hyperlint is an AI-powered tool that helps write, edit, and maintain
  documentation for developer products.

.. _product: https://hyperlint.com/product/

The `product`_ page says that Hyperlint supports automated:

* Style guide enforcement
* Docs updates
* SEO improvements
* Broken link fixes

Presumably, Hyperlint comments on your pull requests (PRs) and submits
PRs.

It also says that AI-assisted authoring is coming soon.

There are integrations with Docusaurus, Hugo, Sphinx, MkDocs, React,
and more. It's unclear to me how these integrations work.

--------------------------------------------
Style guide issues on home and product pages
--------------------------------------------

There are stylistic issues on the Hyperlint home and product pages. Given that
Hyperlint is supposed to help me enforce style guide consistency in my own
docs, I expect it to "lead by example" and have perfect styling in its own
content.

Incorrect capitalization of GitHub:

.. figure:: /_static/github.png

Lack of spaces between sentences:

.. figure:: /_static/spaces.png

-----
Setup
-----

I signed up for the free trial of the Starter package from the Hyperlint
homepage.

.. _technicalwriting.dev repo: https://github.com/technicalwriting/dev

To be useful, Hyperlint needs access to a GitHub repo, so I granted it
access to the `technicalwriting.dev repo`_.

I don't love the broad permissions that it requests:

  Read and write access to checks, code, commit statuses, issues,
  and pull requests

I get the need for read/write access to pull requests and issues.
I don't understand why it wants this access to my checks, code, or
commit statuses.

