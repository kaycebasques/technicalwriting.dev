.. _hyperlint:

==============================
First impressions of Hyperlint
==============================

I'm doing a meet & greet with `Hyperlint <https://hyperlint.com>`__ founder
Bill Chambers today. I figured I should try out the product before we meet.
Here are my notes as of 28 Apr 2025.

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

-------------------
Pull request review
-------------------

.. _pull request: https://github.com/technicalwriting/dev/pull/2

To get further, I realized I needed to submit a PR for something.
I committed my progress on this very ``First impressions of Hyperlint``
blog post and started a `pull request`_ for it.

It was cool to see Hyperlint start automatically doing stuff in the PR,
as expected.

It added a comment:


.. figure:: /_static/summary.png

It's unfortunate that the link checks only work on the first 30 links
and the results are cached. For teammates that iterate rapidly and review/submit
PRs quickly, it sounds like these limitations would allow broken links to
still leak into the codebase accidentally.

The link checker ran as an action:

.. figure:: /_static/linkcheck.png

In the `details <https://github.com/technicalwriting/dev/pull/2/checks?check_run_id=41297222489>`_
of the link check it says ``Issues found in the review`` but then all of the links listed
below it returned HTTP status code 200…?

.. figure:: /_static/linkcheck-details.png

---------------
PR review redux
---------------

For further evaluation, I tried introducing some mistakes in my content.
I omitted Oxford commas, broke some links, and used inconsistent capitalization
in headings. The link checker skipped its run, because of the previously discussed
caching limitations. So it missed the broken link. I did not see any updates to
the ``PR change summary``, so in my book it also missed the Oxford comma and inconsistent
capitalization issues. Do I need to enable the style guide check or something?
I was expecting Hyperlint to leave comments on my PR, highlighting each problem.

That's all the time I've got so I'll have to end the evaluation here!

--------
Thoughts
--------

I like the potential UX a lot. Back when I was content lead for `web.dev <https://web.dev>`_
and `developer.chrome.com <https://developer.chrome.com>`_ I actually built something
similar: `chrome-devrel-review-bot <https://github.com/GoogleChromeLabs/chrome-devrel-review-bot>`_

My main feedback right now is that Hyperlint needs to work on reliability. In order
to trust this tool I need to be confident that it works as expected on every iteration
in every PR.

