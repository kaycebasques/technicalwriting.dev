.. _pdf:

=======================================
You can deeplink to a specific PDF page
=======================================

2024 Jul 11

Just append ``#page=X`` to your URL, where ``X`` is a placeholder for
the page you want to link to. For example, the following link should
jump you to page 5 of the Raspberry Pi Pico getting started guide:
https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf#page=5

Note that the PDF authors consider this to be page 4, whereas the browser
considers it page 5. This is because the browser always treats the first
page of the PDF as page 1 whereas authors sometimes don't.

-------------
Compatibility
-------------
.. _Browser support for basic PDF navigation features: https://pdfa.org/pdf-fragment-identifiers/#Browser_support_for_basic_PDF_navigation_features

See `Browser support for basic PDF navigation features`_.
