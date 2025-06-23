.. _agents:

.. _How to Make Your Developer Documentation Work with LLMs: https://fusionauth.io/blog/llms-for-docs
.. _optimize docs for RAG-based chatbots: https://docs.kapa.ai/improving/writing-best-practices
.. _Writing documentation for AI: https://docs.kapa.ai/improving/writing-best-practices
.. _llms.txt: https://llmstxt.org
.. _Rules: https://docs.cursor.com/context/rules
.. _Claude Code Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices
.. _Software in the era of AI: https://youtu.be/LCEmiRjPEtQ
.. _Agents.md Guide for OpenAI Codex: https://agentsmd.net
.. _Cursor 3-minute demo: https://youtu.be/LR04bU_yV5k
.. _Claude Code: https://docs.anthropic.com/en/docs/claude-code/overview
.. _Cursor: https://docs.cursor.com/welcome
.. _searchtools.txt: ../../_static/searchtools.txt
.. _searchtools.md: ../../_static/searchtools.md
.. _partial autonomy: https://youtu.be/LCEmiRjPEtQ?t=1289
.. _burden of proof: https://en.wikipedia.org/wiki/Burden_of_proof_(law)
.. _Agents.md: https://agentsmd.net
.. _system prompt: https://help.flintk12.com/en/articles/9025167-what-is-a-system-prompt
.. _Manage Claude's memory: https://docs.anthropic.com/en/docs/claude-code/memory
.. _Prompt iteration strategies: https://developers.google.com/machine-learning/resources/prompt-eng#prompt_iteration_strategies

==================
Docs for AI agents
==================

.. figure:: ./agents.png

What are docs for AI agents? How are they different than docs for humans?
How are they similar? Do we have to maintain them as separate docs sets
or can they be combined somehow? This page contains my notes on these
questions. 

(This post is a work in progress.)

-----
Scope
-----

* I work on *developer* docs i.e. docs for software engineers. I don't know
  if AI agents are relevant for technical writers in other industries or
  domains.

* In this post I'm thinking specifically about docs for AI *agents*. I'm not
  sure that an all-encompassing "best practices when writing docs for AI" exists.
  The way that we `optimize docs for RAG-based chatbots`_ (for example) is
  probably different than the way we optimize docs for AI agents.

.. _agents-background:

---------
AI agents
---------

As a software developer, your primary interface for interacting with an AI
agent is through a chat interface that's been bolted onto your CLI or IDE.
See `Claude Code`_ for a CLI example and `Cursor`_ for an IDE example. The
power of AI agents is their ability to use "tools" to act on your behalf, in
addition to all the cool stuff that LLMs can do.

For example, suppose that you need to understand the history of a file
in your codebase. With a single prompt like ``look through the git and
github history of searchtools.js and summarize the evolution of the file``
the agent will:

* Run the relevant ``git`` commands in your terminal
* Fetch the contents of all GitHub issues mentioned in the commits
* Synthesize the information with an LLM
* Write the summary to a file

This really works! See `searchtools.txt`_ and `searchtools.md`_ for an
example.

----------
Agent docs
----------

Agent docs are a way to get better results from the agents. Agent docs
make the agent output more consistent, more aligned with your codebase
conventions, and more accurate.

For example, when first trying out Claude Code (CC) on this website's
repository, I instructed CC to build the site. CC searched through the
codebase and made a reasonable (but incorrect) guess:

.. code-block:: text

   > build the website

   ● I'll build the website for you. Let me first check what build system
     is being used and then run the build command.

   ● Read(package.json)
     ⎿  Error: File does not exist.

   ● List(.)
     ⎿  Listed 166 paths (ctrl+r to expand)

   ● This is a Sphinx documentation website using Bazel as the build system.
     Let me run the build command.

   ● Bash(bazel build //...)
     ⎿  Running…

CC correctly determined that this is a
:ref:`Sphinx site built with Bazel <sphazel-tutorial>`, but it got the
specific build command wrong. The correct command is
``./bazelisk build //:docs``. After adding that command to an agent doc,
CC now always builds the site correctly, even if my prompt is simply
``build``.

Mechanics
=========

How exactly do agents use docs?

`Agents.md`_ makes it sound like a sophisticated, anthropomorphic process
of analysis:

  When OpenAI Codex or another AI agent encounters an Agents.md file in
  your repository, it analyzes the information to guide its code generation
  process. The Agents.md file acts as a knowledge base that informs the AI
  about your project context, ensuring that AI-generated code follows your
  project's standards.

The reality seems to be much more mundane. Based off my reading of Claude Code
docs, Codex docs, Cursor docs, etc. it seems like the real mechanism is just
automated prompt engineering. The agent software looks for a file with a
specific name like ``AGENTS.md`` at a well-known location, such as the root
directory of your codebase. If found, then the full contents of that file are
prepended to any LLM API calls that the agent software makes.
For example, if my ``AGENTS.md`` file contains ``build the docs: ./bazelisk
build //:docs`` and the command that I just sent to the agent is ``build``,
then the underlying API call that the agent software makes to an LLM looks
like this:

.. code-block:: py

   from openai import OpenAI
   client = OpenAI()

   response = client.responses.create(
       model="gpt-4.1",
       input=[
           {
               "role": "developer",
               "content": "build the docs: ./bazelisk build //:docs"
           },
           {
               "role": "user",
               "content": "build"
           }
       ]
   )

   print(response.output_text)

-----------------------------------
Agent docs versus internal eng docs
-----------------------------------

As the meme at the start of the post suggests, my hunch is that "docs for AI
agents" are largely the same thing as "internal eng docs".  These are the docs
that engineering teams write for their own use. The goal is to share knowledge
and standardize workflows among the team. E.g. an RFC explaining a key
architectural decision in the codebase, a guide explaining how to build the
project, a tutorial explaining how to contribute your first patch, etc.  In
open source projects these types of docs are often called "contributor docs".

Problem
=======

The current design of agent docs is steering us towards maintaining the agent
docs as a separate docs set. E.g. your agent docs must have a specific name
like ``CLAUDE.md`` or ``AGENTS.md`` and the docs must be located at specific
locations. I think this might be a mistake.

Agent docs seem to be duplicating the information that already exists in the
internal eng docs. Duplicated information is the root of a lot of docs sins.
I worry that the agent docs will eventually get out-of-sync with the internal
eng docs, and the two docs sets will start saying contradictory things about
the same topics. E.g. the internal eng docs say that you must instantiate
objects via static factory methods, whereas the agent docs say that it's OK
to use constructors directly. This one would probably get caught at review time.
A discrepancy related to codebase design might be more insidious, though.

Maybe we can use AI agents themselves to keep the agent docs in-sync with the
internal eng docs? It sounds feasible, but I'm not sure how much it will
actually happen in practice. Time will tell.

But more importantly, if you think that `partial autonomy`_ is the right way to
build AI systems over the medium-term, then combining or colocating the agent
docs with the internal eng docs should be the default solution because it
increases the odds that humans are constantly verifying the instructions that are
provided to the agents. I explain these "combine" and "colocate" ideas in more
depth later, but the basic gist is that you don't want the agent docs tucked off
in a corner, where no humans actually read them. You want to set up your codebase
so that engineers are naturally reading and updating the agent docs all the
time, as a natural byproduct of their work.

-----------
Comparisons
-----------

To get closer to an answer regarding whether or not agent docs should be separate
from internal eng docs, I'm going to compare and contrast the two types of docs
across various dimensions. If there are huge differences, then they should be
separate docs sets. If there aren't, then we should find a way to combine or colocate
the agent docs with the internal eng docs.

The comparison sections are ordered alphabetically, not by importance.

All caps
========

In agent docs, all caps is an effective way to emphasize an important
instruction. In internal eng docs, this might seem rude or distracting.

I actually think that we should adapt internal eng docs to be more accepting of
all caps. It seems like a pretty effective, plaintext way to emphasize a point.
You see all caps used in code comments sometimes, but it's only used in extreme
situations.

Completeness
============

There's a finite amount of information that you can put into the agent docs
before you start overwhelming the LLM and reducing the quality of its outputs.

With internal eng docs, we aim for completeness. You ideally want documentation
for all APIs, important concepts, key workflows, etc.

File formats
============

Agent docs are strongly encouraged to be written in Markdown because LLMs
understand Markdown very well. Internal eng docs are also usually written
in Markdown.

Goals
=====

The goal of agent docs is to steer the agent towards correct workflows,
coding styles, architectures, API usage, etc. Internal eng docs have the same
goals. The only difference is that you're trying to steer an engineer towards
those successful outcomes, not a language model.

.. -----
.. Ideas
.. -----
.. 
.. Combine
.. =======
.. 
.. "Combining" means that the agent docs and internal eng docs are literally one
.. and the same. 
.. 
.. Colocate
.. ========
.. 
.. "Colocating" means that the agent docs are embedded within the
.. internal eng docs and you do some automated processing to transform the content
.. into the ``AGENTS.md`` files at well-known locations. I suspect that these are
.. better approaches, because engineers will be keeping the agent docs aligned with
.. the internal eng docs as a natural byproduct of their day-to-day work.
.. 
.. 
.. Build up the agent docs programmatically
.. ========================================
.. 
.. .. Claude Code ``#`` thing is cool
.. .. Analyze the whole codebase and build up the docs for us
.. 
.. Ditch the product-branded filenames
.. ===================================

.. _agents-references:

----------
References
----------

* `How to Make Your Developer Documentation Work with LLMs`_
* `Writing documentation for AI`_
* `llms.txt`_
* `Rules`_
* `Claude Code Best Practices`_
* `Software in the era of AI`_
* `Agents.md Guide for OpenAI Codex`_

.. _agents-changelog:

---------
Changelog
---------

TODO
