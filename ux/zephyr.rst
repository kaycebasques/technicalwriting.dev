.. _zephyr:

================================
Studying Zephyr's in-site search
================================

The `Zephyr <https://docs.zephyrproject.org/latest/index.html>`__ in-site
search engine is helpful and well-designed. Let's figure out how it works!

.. _zephyr-background:

----------
Background
----------

.. _Sphinx: https://www.sphinx-doc.org/en/master/
.. _pw_i2c: https://pigweed.dev/pw_i2c

``pigweed.dev``, the docs site I work on, is powered by `Sphinx`_.
``docs.zephyrproject.org`` is also powered by Sphinx. Sphinx's default search
engine isn't working well for us. If you search for `pw_i2c`_ for example you
get a bunch of duplicate results from our changelog:

.. image:: /_static/zephyr1.png

.. _changelog: https://pigweed.dev/changelog.html

This particular duplication happens because our `changelog`_ has many sections
titled ``pw_i2c`` but even if we were to change that, which we won't because
this is an effective changelog structure
