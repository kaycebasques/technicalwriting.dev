.. _skip-to-main-content:

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

Discussions:

* https://news.ycombinator.com/item?id=40569458
* https://lobste.rs/s/vbp8wa
* https://www.reddit.com/r/technicalwriting/comments/1d7kg2k

----------
Background
----------

I personally am learning keyboard-based navigation for "power user" reasons:
I've heard that keyboard-only navigation is faster. But more importantly,
`keyboard compatibility <https://www.w3.org/WAI/perspective-videos/keyboard/>`_
is a P0 (top priority) website accessibility feature. (I don't know if this
"skip to main content" feature per se should be considered P0, but keyboard
navigation in general definitely should be. C-Loftus on Hacker News shared this
helpful survey on screen reader user preferences: https://webaim.org/projects/screenreadersurvey/)

------------
How it works
------------

On day 1 of this journey I realized how important the ``Tab`` key is for
website navigation. Pressing ``Tab`` on my Linux machine (macOS and Windows
people, see next section), lets me jump between focusable elements
such as links and buttons. If you're viewing this page from a computer with
a keyboard you can try it now:

1. Press ``Tab`` on this page. You should see a ``Skip to main content``
   link pop up. This is the thing that most docs sites are missing. More on
   this in a moment.
2. Press ``Tab`` again. The focus moves to the ``Home`` link. The link
   gets a colored border around it; that's how you know it's focused.
3. Keep pressing ``Tab`` and notice how the focus moves from link to link.

(To actually navigate to a focused link you press ``Enter``.)

macOS and Windows
=================

.. _comments: https://news.ycombinator.com/item?id=40569458

Browser/OS compatibility notes from Hacker News `comments`_:

* macOS
  * Safari: The shortcut is ``Option``+``Tab``
  * Firefox: Enable **System Settings** > **Keyboard** > **Keyboard Navigation**
    and then ``Tab`` should work.
* Windows
  * Firefox: ``Tab`` should work "out-of-the-box" but it sounds like my
    implementation doesn't work as expected.

-----------
The problem
-----------

On day 2 of my journey I realized that a lot of docs sites suck at
``Tab``-based navigation, including the one I work on, ``pigweed.dev``. They don't
give you a ``Skip to main content`` link, like the one you just saw. You have
to tab through the header, site nav, and searchbox before focus lands on the main
content. In practice, the link/button/etc. that you actually want to interact with
is probably in the main content. Big docs sites often have hundreds of links in the
site nav, which means you have to tab hundreds of times before the main content
is in focus! ༼ ༎ຶ ෴ ༎ຶ༽

-----------------------
Keyboard-friendly sites
-----------------------

Here are examples of professional sites that implement this feature. These sites
probably "have their shit together" when it comes to accessibility:

* https://www.google.com/search?q=accessibility
* https://en.wikipedia.org/wiki/Accessibility
* https://www.w3.org/WAI/fundamentals/accessibility-intro/

-------
The fix
-------

This issue doesn't seem hard-to-fix. Here's the change I just put in for
Pigweed: https://pwrev.dev/213659

(a11y/webdev people: let me know if I implemented incorrectly/suboptimally.
Edit: a comment from Hacker News suggests that my implementation doesn't work
correctly on Windows.)

And here's an issue I just created to fix this across Sphinx's core themes:
https://github.com/sphinx-doc/sphinx/issues/12407

Implementation
==============

1. Add the skip link as the very first element after ``<body>``. It should
   be the very first element to ensure that it's the first thing that
   receives focus.

   .. code-block:: html

      ...
      <body>
        <a id="skip" href="#skip-target">Skip to main content</a>
        ...

2. Add the ``skip-target`` ID to an element near your main content. You can
   add an empty ``<span>`` or you can add the ID to an existing element.

   .. code-block:: html

      ...
      <span id="skip-target"></span>
      <main>
      ...

   When the "skip to main content" link is focused and you press ``Enter``,
   you navigate to the element with the ``skip-target`` ID. Since it's
   an in-page link, this basically just jumps focus to the ``skip-target``
   element.

3. Style the skip link so that it's hidden by default (by pushing it far outside
   of the visible viewport) and then is shown in the top-left corner when it receives focus:

   .. code-block:: css

      #skip {
        position: absolute;
        top: -1000%;
        left: -1000%;
      }

      #skip:focus {
        top: 10px;
        left: 10px;
      }
