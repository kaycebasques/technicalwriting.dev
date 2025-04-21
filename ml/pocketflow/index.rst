.. _pocketflow:

=====================================================
First impressions of Pocket Flow's tutorial generator
=====================================================

.. _Tutorial-Codebase-Knowledge: https://github.com/The-Pocket/Tutorial-Codebase-Knowledge
.. _Pocket Flow: https://github.com/The-Pocket/PocketFlow

These are my initial notes on `Tutorial-Codebase-Knowledge`_ (TCK) by `Pocket Flow`_.

----------
Background
----------

.. _README: https://github.com/The-Pocket/Tutorial-Codebase-Knowledge/blob/main/README.md

In its `README`_, TCK describes itself like this:

  Ever stared at a new codebase written by others feeling completely lost? This
  tutorial shows you how to build an AI agent that analyzes GitHub repositories
  and creates beginner-friendly tutorials explaining exactly how the code works.

.. _tutorials: https://diataxis.fr/tutorials/

As a technical writer, I have a specific understanding of `tutorials`_. A tutorial
gives you hands-on experience in building up a specific skill. You start from
a very specific point A and end at a very specific point B. I believe that
most technical writers agree on this definition but I know that other roles
(e.g. software engineers) use different definitions.

The ``explaining exactly how the code works`` part of the description suggests
that TCK is specifically intended to help onboard new codebase contributors.
I.e. it's not intended to create end user tutorials. E.g. if I provide it the
React codebase, I expect to get a tutorial that teaches me how to contribute
bug fixes or new features to the React codebase, not how to build websites
with React.

----------------
First evaluation
----------------

.. _Sphinx: https://www.sphinx-doc.org/en/master/

Let's start with the `Sphinx`_ codebase. I use Sphinx in most of my docs projects.
One of my top goals this year is to contribute to the upstream Sphinx codebase
more.

I like the simple setup process:

.. code-block:: console

   $ fish  # The activate command below assumes a fish shell.
   $ mkdir pocketflow
   $ cd pocketflow
   $ git clone git@github.com:sphinx-doc/sphinx.git
   $ git clone https://github.com/The-Pocket/Tutorial-Codebase-Knowledge.git
   $ cd Tutorial-Codebase-Knowledge
   # Edit utils/call_llm.py to use your API key.
   # The language model can also be configured from this file.
   $ python3 -m venv venv
   $ . venv/bin/activate.fish
   $ python3 -m pip install -r requirements.txt
   $ time python main.py --dir ../sphinx

The default model is ``gemini-2.5-pro-exp-03-25``. I quickly hit rate limits
with that one. The rate limit error message told me to use
``gemini-2.5-pro-preview-03-25`` instead but that one also hit rate limits. I
then tried ``gemini-2.5-flash-preview-04-17`` but again, rate limits. I finally
downgraded all the way to ``gemini-2.0-flash`` but that one had a different
problem: 

.. code-block:: text

   The input token count (1366296) exceeds the maximum
   number of tokens allowed (1000000).

The fact that we're hitting an input limit here suggests that TCK
feeds in all of the source files as input to the language model.

To proceed, I guess I either need to reduce the amount of input, or choose a
smaller project. Let's try excluding all of Sphinx's documentation (``*.rst``)
files. In real-world usage, I imagine that codebase owners will use TCK to
kickstart their own docs. In other words, their codebase won't have any docs,
and they will use TCK to get a first draft of the docs going.

.. code-block:: console

   $ time python main.py --dir ../sphinx --exclude "*.rst"

Still hitting input limits:

.. code-block:: text

   The input token count (1569286) exceeds the maximum
   number of tokens allowed (1000000).

.. _microbit: https://docs.rs/microbit/latest/microbit/
.. _BBC micro\:bit: https://microbit.org

I'll give up on Sphinx for now and try the `microbit`_ Rust crate instead.
This crate lets you write embedded software for the `BBC micro:bit`_ in Rust.

.. code-block:: console

   $ cd ..
   $ git clone https://github.com/nrf-rs/microbit
   $ cd Tutorial-Codebase-Knowledge
   $ time python main.py --dir ../microbit

This time it worked:

.. code-block:: text

   Starting tutorial generation for: ../microbit in English language
   Crawling directory: ../microbit...
   Fetched 2 files.
   Identifying abstractions using LLM...
   Identified 5 abstractions.
   Analyzing relationships using LLM...
   Generated project summary and relationship details.
   Determining chapter order using LLM...
   Determined chapter order (indices): [0, 1, 2, 3, 4]
   Preparing to write 5 chapters...
   Writing chapter 1 for: microbit (crate)
    using LLM...
   Writing chapter 2 for: Board
    using LLM...
   Writing chapter 3 for: Display
    using LLM...
   Writing chapter 4 for: GPIO (General Purpose Input/Output) Pins
    using LLM...
   Writing chapter 5 for: HAL (Hardware Abstraction Layer)
    using LLM...
   Finished writing 5 chapters.
   Combining tutorial into directory: output/microbit
     - Wrote output/microbit/index.md
     - Wrote output/microbit/01_microbit__crate__.md
     - Wrote output/microbit/02_board_.md
     - Wrote output/microbit/03_display_.md
     - Wrote output/microbit/04_gpio__general_purpose_input_output__pins_.md
     - Wrote output/microbit/05_hal__hardware_abstraction_layer__.md
   
   Tutorial generation complete! Files are in: output/microbit
   
   ________________________________________________________
   Executed in   62.90 secs      fish           external
      usr time  575.98 millis  998.00 micros  574.99 millis
      sys time   57.69 millis  256.00 micros   57.43 millis

You can view all of the generated docs here:

* `Index <https://github.com/technicalwriting/dev/blob/main/ml/pocketflow/microbit/01_microbit__crate__.md>`_
* `Chapter 2 <https://github.com/technicalwriting/dev/blob/main/ml/pocketflow/microbit/02_board_.md>`_
* `Chapter 3 <https://github.com/technicalwriting/dev/blob/main/ml/pocketflow/microbit/03_display_.md>`_
* `Chapter 4 <https://github.com/technicalwriting/dev/blob/main/ml/pocketflow/microbit/04_gpio__general_purpose_input_output__pins_.md>`_
* `Chapter <https://github.com/technicalwriting/dev/blob/main/ml/pocketflow/microbit/05_hal__hardware_abstraction_layer__.md>`_

(TCK did not generate a first chapter. It goes straight from the index to the second chapter.)

The next few sections are my notes about each generated chapter.

Index
=====

.. _RTOS: https://en.wikipedia.org/wiki/Real-time_operating_system
.. _examples: https://github.com/nrf-rs/microbit/tree/main/examples

Pros:

* I like that the page is concise.
* The Mermaid diagram is attractive.
* The components of the diagram seem to be in the correct places.

Cons:

* The first paragraph claims that the crate provides an "operating system"
  for the micro:bit. Considering that this is supposed to be a tutorial for
  codebase contributors, that sounds very misleading. I'm pretty sure this
  crate gives you bare metal control of the micro:bit. I don't even see any
  `RTOS`_ usage in the codebase.
* The diagram seems incomplete. The crate provides `examples`_ of interfacing
  with the micro:bit's ADC, magnetometer, random number generator, serial,
  servo, microphone, and speaker. I would expect those to be covered in the
  diagram.
* Usually, tutorials start by declaring what you'll learn. After reading this
  page I have a sense of what the codebase does, but I'm still not sure about
  what I'll accomplish by the end of the tutorial.

Chapter 2
=========

Pros:

* The fact that it calls out the 2 versions of the micro:bit upfront is great.
* It generated a timing diagram! Very cool and promising.

Cons:

* The writing is geared towards extreme beginners. This writing style does not
  seem appropriate for codebase contributors.
* The first code example is incomplete. There should be more indication that
  this code won't work.
* Where is chapter 1? It goes straight from index to chapter 2.

Chapter 3
=========

Pros:

* The key concepts section seems like a good overview.

Cons:

* The "main character in a video game" analogy is strange.
* One of the diagrams does not render. Given the fact that GitHub
  was able to render the other Mermaid diagrams, I presume that TCK
  itself generated incorrect Mermaid code.
* The simplified internal implementation seems pretty far removed from
  the actualy real implementation. I get the desire to start from a simple
  foundation, but as a new codebase contributor I wonder if this would do
  more harm than good.
* At this point I'm pretty sure that none of the code examples are actually
  going to work. The lack of ``#![no_main]`` and ``#![no_std]`` is a giveaway
  that none of the code is complete.

Chapter 4
=========

Pros:

* The code examples are starting to look more fleshed out.
* If I were brand new to GPIO, this seems like a decent introduction.

Cons:

* The content is definitely not geared towards codebase contributors.

Chapter 5
=========

Pros:

* The conceptual explanation of HALs looks solid.
* The level of technical depth is starting to look more aligned
  with what new codebase contributors would need.

Cons:

* The page ends by saying ``In the next chapter, we'll explore further concepts.``
  but there is no next chapter. This is the last chapter.

-----------------
Second evaluation
-----------------

.. _nodes.py: https://github.com/The-Pocket/Tutorial-Codebase-Knowledge/blob/main/nodes.py

An exciting thing about this project is that it's all open source and
the TCK repo itself is quite simple. Let's try to customize TCK to
fix the issues that we encountered in the first evaluation. The only
file that we need to touch is `nodes.py`_.

Here's a diff of the prompts that I changed:

.. literalinclude:: microbit/diff.txt
   :language: text
