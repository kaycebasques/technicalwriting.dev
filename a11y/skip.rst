.. _skip:

=======================================================
Please support "skip to main content" on your docs site
=======================================================

2024 Jun 3

.. _embarked on a journey: https://biodigitaljazz.net/blog/pcrowdoodle.html

Last month I `embarked on a journey`_ to get comfortable with keyboard-based
computer navigation. In other words, when using my computer I don't want to
move my right hand from my keyboard to my mouse hundreds or thousands of times
per day just to do basic navigation tasks like changing tabs, scrolling the
screen, etc.

I personally am learning keyboard-based navigation for "power user" reasons:
I've heard that keyboard-only navigation is faster. But more importantly,
`keyboard compatibility <https://www.w3.org/WAI/perspective-videos/keyboard/>`_
is a P0 website accessibility feature.

On day 1 of this journey I realized how important the ``Tab`` key is for
website navigation. ``Tab`` lets you jump between focusable elements
such as links and buttons. If you're viewing this page from a computer with
a keyboard you can try it now:

1. Press ``Tab`` on this page. You should see a ``Skip to main content``
   link pop up. This is the thing that most docs sites are missing. More on
   this in a moment.
2. Press ``Tab`` again. The focus moves to the ``Home`` link. The link
   gets a colored border around it; that's how you know it's focused.
3. Keep pressing ``Tab`` and notice how the focus moves from link to link.

(To actually navigate to a focused link you press ``Enter``.)

On day 2 of my journey I realized that a lot of docs sites suck at
``Tab``-based navigation, including the one I work on, ``pigweed.dev``. They don't
give you a ``Skip to main content`` link, like the one you just saw. You have
to tab through the header, site nav, and searchbox before focus lands on the main
content. Big docs sites often have hundreds of links in the site nav, which means you
have to tab hundreds of times before the main content is in focus! ༼ ༎ຶ ෴ ༎ຶ༽

Here are examples of professional sites that implement this feature. These sites
probably "have their shit together" when it comes to accessibility:

* https://www.google.com/search?q=accessibility
* https://en.wikipedia.org/wiki/Accessibility
* https://www.w3.org/WAI/fundamentals/accessibility-intro/

This issue doesn't seem hard-to-fix. Here's the change I just put in for
Pigweed: https://pwrev.dev/213659

(a11y/webdev people: let me know if I implemented incorrectly/suboptimally.)

And here's an issue I just created to fix this across Sphinx's core themes:
https://github.com/sphinx-doc/sphinx/issues/12407
