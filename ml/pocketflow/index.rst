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
a very specific point A and end at a very specific point B. This definition is
practically universally accepted among technical writers, but software engineers
(for example) often have a different definition.

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

Spinning up TCK is easy:

.. code-block:: console

   $ fish  # The activate command below assumes a fish shell.
   $ mkdir pocketflow
   $ cd pocketflow
   $ git clone git@github.com:sphinx-doc/sphinx.git
   $ git clone https://github.com/The-Pocket/Tutorial-Codebase-Knowledge.git
   $ cd Tutorial-Codebase-Knowledge
   # Edit utils/call_llm.py to use your API key.
   # The model can also be configured from this file.
   $ python3 -m venv venv
   $ . venv/bin/activate.fish
   $ python3 -m pip install -r requirements.txt
   # Note that I'm including all files whereas the 
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

I'll give up on Sphinx for now and try the `microbit`_ Rust crate instead.

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
