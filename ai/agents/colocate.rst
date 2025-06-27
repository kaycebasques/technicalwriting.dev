.. _Guidelines for buildable and testable code examples: https://pigweed.dev/docs/contributing/docs/examples.html
.. _examples.rst: https://cs.opensource.google/pigweed/pigweed/+/c66eb854d321815eca1b0d4cbdfb893a43ab0b5d:docs/contributing/docs/examples.rst;bpv=1
.. _pwrev.dev/301461/1: https://pigweed-review.googlesource.com/c/pigweed/pigweed/+/301461/1

.. _colocate:

========================================================
(Experiment) Colocating agent instructions with eng docs
========================================================

In :ref:`my initial investigation of docs for AI agents <agents>`
I expressed skepticism over the current design of agent docs.
The agent providers (Claude Code, Gemini CLI, Cursor, etc.) are
steering us towards maintaining the agent docs as a new, separate
docs set. Yet agent docs seem to be very similar to internal eng docs.
I worry that we'll end up duplicating a lot of information across the
two docs sets. Inevitably, the duplicated information gets
out-of-sync with one another, and you end up in the confusing
situation where you're not sure whether the agent docs or the internal
eng docs are correct.

At the end of :ref:`agents` I propose various solutions to the synchronization
problem. In :ref:`agents-colocate`, I basically propose embedding the
agent instructions within the internal eng docs.
I tried out the colocate solution today, and it worked great!
Here are the details.

----------
Background
----------

Today on ``pigweed.dev``, we published `Guidelines for buildable and testable code examples`_.
At the top of the page, I embedded AI agent instructions:

.. code-block:: txt

   .. Instructions for AI agents (e.g. Gemini CLI):
   .. #. Follow the workflow described in :ref:`contributing-docs-quickstart-a`.
   ..    Do not use Option B.
   .. #. Inspect the files in ``//pw_string/examples``. This is a working example
   ..    of the kind of code that you need to create.
   .. #. Create the code example, unit test, and build targets. The first
   ..    iteration of the unit test should fail.
   .. #. Run ``bazelisk test //...`` to verify that your new unit test fails.
   .. #. Fix the unit test.
   .. #. Run ``bazelisk test //...`` again and verify that the new unit test now
   ..    passes.
   
   .. _contributing-docs-examples:
   
   ===================================================
   Guidelines for buildable and testable code examples
   ===================================================
   This guide shows :ref:`docs-glossary-upstream` maintainers how to write
   buildable and testable code examples for ``pigweed.dev``. It's focused on
   C++ but the general pattern is theoretically applicable to any language.

   …

(See `examples.rst`_ to view the full source code.)

All of those lines at the top of the file beginning with ``..`` are
comments. Humans viewing the page on a web browser don't see those comments.
These comments are the instructions for the agent. I embedded them within
the eng doc, rather than spinning up a separate agent doc like ``CLAUDE.md``,
``GEMINI.md``, ``AGENTS.md``, etc.

----------
Experiment
----------

I loaded up the code examples guidelines (``@docs/contributing/docs/examples.rst``)
and then instructed Gemini CLI to migrate a specific code example:

.. code-block:: text

   > @docs/contributing/docs/examples.rst use the instructions in examples.rst to
     convert the code example in the "Known size string" section of pw_string/guide.rst
     into a buildable and testable code example. Note that the examples.rst instructions
     has a mistake. When you update the sphinx_docs_library Bazel rules, you should
     update the `srcs` list, not the `deps` list.

-------
Results
-------

It worked really well. Gemini CLI followed the agent instructions
that I put at the top of the `examples.rst`_ file:

* Crucially, it created a failing test first, verified that the test fails,
  and then updated the test to pass.

* I got inadvertent confirmation that Gemini CLI was following my instructions
  closely. There's a mistake in ``examples.rst``. It instructs you to update
  the ``deps`` list in the ``sphinx_docs_library``. You actually need to update
  the ``srcs`` list. The first time I tried this workflow, Gemini CLI got
  confused because it could not find a ``deps`` list on the rule.

However, note that this is not a "pure" experiment. A pure experiment would
require me to run this workflow in a project that doesn't have any agent
docs. The Pigweed repo does have an agent doc, as you can tell after I run
the ``/memory show`` command. So, if anything, this experiment may be suggesting
that you get the best results when you have both agent docs and more targeted
instructions like `examples.rst`_ that you load in when you're trying to accomplish
a particular task.

Below is the full log. See `pwrev.dev/301461/1`_ to view the code that Gemini CLI
generated.

.. literalinclude:: ./colocate.txt
   :language: text
