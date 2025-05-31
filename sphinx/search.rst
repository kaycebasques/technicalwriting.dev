=================================
Notes on Sphinx's built-in search
=================================

WIP

----------------------
Disable search summary
----------------------

Maybe this? Didn't work via Chrome DevTools Console.

.. code-block:: js

   DOCUMENTATION_OPTIONS.SHOW_SEARCH_SUMMARY = false;

----------------------------
Speeding up index generation
----------------------------

Install PyStemmer: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_search_language

---------------------------
Customize the search scorer
---------------------------

Set this config flag: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_search_scorer

And then implement the custom scorer in a JS file.

-----------
OpenSearch?
-----------

Not sure what this does: https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_use_opensearch

---------------------------------
Remove a page from search results
---------------------------------

Just add ``:nosearch:`` to top of page. https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html

Thanks to Documatt for making me aware of that feature

----------
References
----------

Backend (search index) implementation:

* `//sphinx/search/__init__.py <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/search/__init__.py>`_
* `//sphinx/search/_stopwords/en.txt <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/search/_stopwords/en.txt>`_
* `//sphinx/search/_stopwords/en.py <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/search/_stopwords/en.py>`_
* `//sphinx/search/en.py <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/search/en.py>`_
* `//sphinx/search/non-minified-js/base-stemmer.js <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/search/non-minified-js/base-stemmer.js>`_
* `//sphinx/search/non-minified-js/english-stemmer.js <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/search/non-minified-js/english-stemmer.js>`_

Frontend (search UI) implementation:

* `//sphinx/themes/basic/search.html <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/themes/basic/search.html>`_
* `//sphinx/themes/basic/searchbox.html <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/themes/basic/searchbox.html>`_
* `//sphinx/themes/basic/searchfield.html <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/themes/basic/searchfield.html>`_
* `//sphinx/themes/basic/static/searchtools.js <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/themes/basic/static/searchtools.js>`_
* `//sphinx/themes/basic/static/sphinx_highlight.js <https://github.com/sphinx-doc/sphinx/blob/master/sphinx/themes/basic/static/sphinx_highlight.js>`_
* `What is Sphinx built-in search, and how to use it in themes? <https://documatt.com/blog/25/sphinx-builtin-search-theme/>`_
