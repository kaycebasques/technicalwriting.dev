.. _agents:

.. _How to Make Your Developer Documentation Work with LLMs: https://fusionauth.io/blog/llms-for-docs
.. _Writing documentation for AI: https://docs.kapa.ai/improving/writing-best-practices
.. _llms.txt: https://llmstxt.org
.. _Rules: https://docs.cursor.com/context/rules
.. _Claude Code Best Practices: https://www.anthropic.com/engineering/claude-code-best-practices
.. _Software in the era of AI: https://youtu.be/LCEmiRjPEtQ
.. _Agents.md Guide for OpenAI Codex: https://agentsmd.net
.. _Every Page Is Page One: https://everypageispageone.com/the-book/
.. _Docs For Developers: https://docsfordevelopers.com/
.. _Diátaxis: https://diataxis.fr/
.. _Don't Make Me Think: https://en.wikipedia.org/wiki/Don%27t_Make_Me_Think
.. _Cursor 3-minute demo: https://youtu.be/LR04bU_yV5k
.. _Claude Code: https://docs.anthropic.com/en/docs/claude-code/overview
.. _Cursor: https://docs.cursor.com/welcome

==================
Docs for AI agents
==================

.. figure:: ./agents.png

How are docs for AI agents different than docs for humans? How are they
similar? Do we have to maintain them as separate docs sets or can they
be combined somehow?

This page contains my notes on questions like these.

----------
Hypothesis
----------

As the meme above suggests, my hunch is that "documentation for AI agents" will
end up looking largely the same as "documentation for (human) internal
(software) engineers". (In open source, these types of docs are often called
"contributor docs".) I could be wrong. I'm not trying to sell you on that idea.
The only purpose of this hypothesis is to disclose potential biases in my
research.

-----
Scope
-----

Technical writing is a big field that spans many industries. I'm focused on
the domain of developer docs i.e. docs for (human) software developers. I don't
know how relevant this "docs for AI agents" stuff is for technical writers in
other industries or domains.

I'm not talking about broadly about "writing documentation for AI". I think
that phrase is too broad. I suspect that the

Furthermore, "AI agents" is also a big field. I'm focused on "AI agents
for software developers". More on this in the next section.

.. _agents-overview:

--------
Overview
--------

As a software developer, your primary interface for interacting with an AI
agent is through a chat interface that's been bolted onto your CLI or IDE.
See `Claude Code`_ for a CLI example and `Cursor` for an IDE example. The
power of AI agents is their ability to use "tools" to act on your behalf.
For example, suppose that you need to understand the history of a file
in your codebase. With a single prompt like ``look through the git and
github history of this file and summarize the evolution of this file in
evolution.md`` the agent will:

* Do all the necessary pre-work: run ``git`` commands in your terminal,
  fetch the contents of all GitHub issues mentioned in the commits, etc.
  (`example <./searchtools.txt>`__)
* Synthesize the information and write it to the specified file
  (`example <./searchtools.md>`__)
  
See also `Cursor 3-minute demo`_.

How agents use docs
===================

TODO

--------------
Juxtapositions
--------------

The next few sections compare and contrast "docs for AI agents" versus "docs for humans".
The sections are ordered alphabetically, not by importance.

Capitalization
==============

TODO

Goals
=====

TODO

.. --------
.. Research
.. --------
.. 
.. .. list-table::
..    :header-rows: 1
.. 
..    * - Aspect
..      - Writing for Humans
..      - Writing for AI Agents (LLMs)
..      - Source(s)
..    * - Purpose
..      - Help users learn, evaluate, and use your product
..      - Enable LLMs to surface, summarize, and answer queries about your product
..      - FusionAuth, llms.txt
..    * - Structure
..      - Clear, logical, easy to navigate; can be narrative or reference-based
..      - Highly structured, with context in every section; each section should be self-contained and explicit
..      - FusionAuth, Kapa.ai, YCombinator
..    * - Headings/Links & Navigation
..      - Useful for navigation and skimming; menus, links, and search
..      - Critical for LLMs to parse and relate content; centralized, curated files or explicit linking
..      - FusionAuth, llms.txt, Kapa.ai
..    * - Context
..      - Can rely on user reading previous sections, memory, or intuition
..      - Each section must be self-contained with full context; avoid references like "see above"
..      - FusionAuth, Kapa.ai, YCombinator
..    * - Chunking
..      - Not a concern; humans can follow references and context
..      - AI systems process docs in chunks; implicit connections are lost unless made explicit
..      - Kapa.ai, YCombinator
..    * - Content Types
..      - Guides, FAQs, troubleshooting, reference, forums
..      - Same, but FAQs and troubleshooting especially help LLMs answer common questions
..      - FusionAuth
..    * - Visuals & Layout
..      - Can use diagrams, tables, and formatting for meaning
..      - Must provide text equivalents for visuals; avoid layout-dependent meaning
..      - Kapa.ai, YCombinator
..    * - Format
..      - Flexible: HTML, PDF, custom layouts, visual elements
..      - Prefer Markdown, plain text, and standardized formats for easy parsing and ingestion
..      - llms.txt, Kapa.ai, Claude Code
..    * - Jargon & Assumptions
..      - Can use domain-specific language, explained as needed
..      - Avoid unexplained jargon; make all assumptions explicit
..      - llms.txt, YCombinator
..    * - Error Handling
..      - General troubleshooting, may rely on user interpretation
..      - Include exact error messages and solutions for direct matching
..      - Kapa.ai, YCombinator
..    * - Content Organization
..      - Can be hierarchical, but humans can navigate non-linear structures
..      - Hierarchical information architecture is essential; each section should carry enough context to be understood independently
..      - Kapa.ai
..    * - Procedural Content
..      - Can assume prior setup or familiarity
..      - Each procedure should include prerequisites and context, not assume prior knowledge
..      - Kapa.ai
..    * - Level of Detail
..      - Can be broad, narrative, and exploratory
..      - Concise, focused, and explicit; avoids unnecessary detail and ambiguity
..      - llms.txt
..    * - Discoverability
..      - SEO, sitemaps, and navigation for humans
..      - LLMs can replace search engines for discovery; /llms.txt file at root path for LLMs to find easily
..      - FusionAuth, llms.txt
..    * - Technical Aids & Integration
..      - Analytics, feedback forms; human-focused, may not consider machine consumption
..      - Access logs for LLM user agents, llms.txt files, copy-to-markdown buttons; designed for programmatic access and integration with LLM tools and plugins
..      - FusionAuth, llms.txt, Cursor Rules
..    * - Guidance & Persistence
..      - Provided as documentation, guides, or internal docs; readers must remember or reference as needed
..      - Encoded as persistent, reusable rules (e.g., .cursor/rules, CLAUDE.md) for consistent model context; always included in model context
..      - Cursor Rules, Claude Code
..    * - Application & Automation
..      - Humans interpret and apply guidance as needed; interpret and execute workflows
..      - AI models automatically apply rules at the start of each context, guiding behavior and responses; agents can automate workflows, use checklists, and run commands as described
..      - Cursor Rules, Claude Code
..    * - Examples & Commands
..      - Provided in documentation, may be scattered
..      - Centralized in rules or command files for agent use
..      - Claude Code, Cursor Rules
..    * - Collaboration
..      - Shared via documentation, wikis, or internal docs
..      - Shared via version control, checked-in config, or team-wide files
..      - Cursor Rules, Claude Code
..    * - Updates & Maintenance
..      - Important for accuracy and user trust; updated as needed, but may lag behind usage
..      - Essential, as outdated or ambiguous content directly degrades AI answer quality; should be kept current, as LLMs may ingest outdated info
..      - FusionAuth, Kapa.ai, llms.txt, Claude Code, YCombinator
..    * - Best Practices
..      - Focused, actionable, and clear documentation is recommended
..      - Rules should be concise, composable, and provide concrete examples; avoid vague guidance
..      - Cursor Rules, Claude Code

-----------
Suggestions
-----------

Separate docs for agents smells like a bad idea
===============================================

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
