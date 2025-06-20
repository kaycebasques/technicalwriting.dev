=========================================
Docs for AI agents versus docs for humans
=========================================

Compare/Contrast: Writing Docs for AI Agents vs. Humans
-------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Aspect
     - Writing for Humans
     - Writing for AI Agents (LLMs)
   * - Purpose
     - Help users learn, evaluate, and use your product
     - Enable LLMs to surface, summarize, and answer queries about your product
   * - Structure
     - Clear, logical, easy to navigate for readers
     - Highly structured, with context in every section for independent understanding
   * - Headings/Links
     - Useful for navigation and skimming
     - Critical for LLMs to parse and relate content
   * - Context
     - Can rely on user reading previous sections
     - Each section should be self-contained with full context (product, version, component, goal)
   * - Content Types
     - Guides, FAQs, troubleshooting, reference, forums
     - Same, but FAQs and troubleshooting especially help LLMs answer common questions
   * - Updates
     - Important for accuracy and trust
     - Essential, as LLMs may ingest outdated info otherwise
   * - Accessibility
     - Fast, public, easy to find
     - Fast, public, and easy for bots to crawl and ingest
   * - Discovery
     - SEO, navigation, search
     - LLMs can replace search engines for discovery
   * - Building/Support
     - Step-by-step guides, examples, forums
     - LLMs can replace Stack Overflow for support, so docs should cover edge cases and long-tail content
   * - Technical Aids
     - Analytics, feedback forms
     - Access logs for LLM user agents, ``llms.txt`` files, copy-to-markdown buttons
   * - Success Metrics
     - Page views, user feedback, support tickets
     - LLM-driven traffic, accuracy of LLM answers, user reports of finding docs via LLMs
   * - Effort
     - Ongoing, requires maintenance and updates
     - Same, but even more important for LLMs to have up-to-date, well-structured docs

Key Contrasts
~~~~~~~~~~~~~

- **Context:** Humans can piece together information from multiple sections, but LLMs need each section to be self-contained and explicit.
- **Structure:** Good structure helps both, but is even more critical for LLMs to parse and relate information.
- **Discovery:** SEO and navigation help humans; LLMs may bypass these and go directly to relevant sections if docs are well-structured.
- **Technical Aids:** Humans benefit from traditional analytics; LLMs may require new tools like ``llms.txt`` and access log analysis.

Key Similarities
~~~~~~~~~~~~~~~~

- Quality, clarity, and completeness are foundational for both.
- Up-to-date, accurate docs benefit everyone.
- Well-structured docs with clear headings and links help both audiences.

Reference: `How to Make Your Developer Documentation Work with LLMs: Lessons from the Trenches – FusionAuth Blog <https://fusionauth.io/blog/llms-for-docs>`_

Compare/Contrast: Writing Docs for AI Agents vs. Humans (Kapa.ai)
-----------------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Aspect
     - Writing for Humans
     - Writing for AI Agents (LLMs)
   * - Content Structure
     - Can be narrative, assumes linear reading and context
     - Must be explicit, self-contained, and contextually complete; each section should stand alone
   * - Chunking
     - Not a concern; humans can follow references and context
     - AI systems process docs in chunks; implicit connections are lost unless made explicit
   * - Context
     - Can rely on prior sections or assumed knowledge
     - All necessary context must be included in each chunk; avoid references like "see above"
   * - Semantic Clarity
     - Helpful, but humans can infer meaning from context
     - Critical; use descriptive headings, meaningful URLs, and clear relationships between sections
   * - Visuals
     - Can rely on diagrams, tables, and layout for meaning
     - Must provide text equivalents for visuals; layout and images are not reliably parsed by AI
   * - Format
     - Flexible; can use PDFs, complex layouts, or custom UI
     - Prefer HTML or Markdown; avoid PDFs and complex layouts for better machine parsing
   * - Error Handling
     - General troubleshooting may suffice
     - Include exact error messages and solutions for direct matching with user queries
   * - Content Organization
     - Can be hierarchical, but humans can navigate non-linear structures
     - Hierarchical information architecture is essential; each section should carry enough context to be understood independently
   * - Procedural Content
     - Can assume prior setup or familiarity
     - Each procedure should include prerequisites and context, not assume prior knowledge
   * - Maintenance
     - Important for accuracy and user trust
     - Essential, as outdated or ambiguous content directly degrades AI answer quality

Key Contrasts (Kapa.ai)
~~~~~~~~~~~~~~~~~~~~~~~

- **Chunking & Context:** Humans can piece together information from scattered sections, but AI systems process content in isolated chunks. Each chunk must be self-contained and explicit, with all necessary context included.
- **Visuals & Layout:** Humans can interpret meaning from images, diagrams, and layout, but AI systems need text equivalents and simple, semantic structure.
- **References & Assumptions:** Humans can follow references like "see above" or "as mentioned earlier," but AI systems cannot. Avoid implicit knowledge and make all relationships explicit.

Key Similarities (Kapa.ai)
~~~~~~~~~~~~~~~~~~~~~~~~~~

- Clarity, structure, and completeness benefit both audiences.
- Well-organized, accessible documentation improves user experience for both humans and AI.
- Maintaining up-to-date, accurate docs is critical for both.

Reference: `Writing documentation for AI: best practices – Kapa.ai Docs <https://docs.kapa.ai/improving/writing-best-practices>`_

Compare/Contrast: Writing Docs for AI Agents vs. Humans (llms.txt)
------------------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Aspect
     - Writing for Humans
     - Writing for AI Agents (LLMs)
   * - Content Structure
     - Designed for readability, navigation, and engagement
     - Designed for concise, expert-level, and easily parseable information in a single location
   * - Format
     - Flexible: HTML, PDF, custom layouts, visual elements
     - Prefer Markdown, plain text, and standardized formats for easy parsing and ingestion
   * - Purpose
     - Help users understand, evaluate, and use the site
     - Help LLMs quickly access key information, background, and links to detailed resources
   * - Navigation
     - Menus, links, and search for user exploration
     - Centralized, curated file (e.g., /llms.txt) with direct links to LLM-friendly resources
   * - Context
     - Can be distributed across multiple pages and sections
     - Gathered in a single, accessible file with background, guidance, and links for LLMs
   * - Level of Detail
     - Can be broad, narrative, and exploratory
     - Concise, focused, and explicit; avoids unnecessary detail and ambiguity
   * - Jargon
     - Can use domain-specific language, explained in context
     - Avoids unexplained jargon; uses clear, unambiguous terms for machine understanding
   * - Updates
     - Updated as needed for human readers
     - Should be kept current, as LLMs may rely on the /llms.txt file for up-to-date info
   * - Integration
     - Human-focused, may not consider machine consumption
     - Designed for programmatic access and integration with LLM tools and plugins
   * - Discoverability
     - SEO, sitemaps, and navigation for humans
     - /llms.txt file at root path, similar to robots.txt or sitemap.xml, for LLMs to find easily

Key Contrasts (llms.txt)
~~~~~~~~~~~~~~~~~~~~~~~~

- **Centralization:** LLMs benefit from a single, curated file (like /llms.txt) that summarizes key information and provides direct links, while humans navigate through multiple pages and sections.
- **Format:** LLMs prefer Markdown and plain text for easy parsing, while humans can handle complex layouts and visual elements.
- **Explicitness:** LLMs require explicit, unambiguous information, while humans can infer meaning from context and narrative.

Key Similarities (llms.txt)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Clarity and accuracy are essential for both.
- Up-to-date, well-maintained documentation benefits all users.
- Both can benefit from concise summaries and clear organization.

Reference: `llms.txt: A proposal to standardise on using an /llms.txt file to provide information to help LLMs use a website at inference time <https://llmstxt.org/>`_

Compare/Contrast: Writing Docs for AI Agents vs. Humans (Cursor Rules)
---------------------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Aspect
     - Writing for Humans
     - Writing for AI Agents (LLMs)
   * - Guidance
     - Provided as documentation, guides, or internal docs
     - Encoded as persistent, reusable rules (e.g., in .cursor/rules) for consistent model context
   * - Persistence
     - Readers must remember or reference documentation as needed
     - Rules are always included in the model context, ensuring consistent behavior across sessions
   * - Scope
     - Documentation can be broad or specific, but is generally not scoped to code or workflow context
     - Rules can be project-wide, directory-specific, or user-specific, and are scoped to codebase or workflow
   * - Format
     - Written in prose, markdown, or other human-friendly formats
     - Written in MDC (Markdown with metadata) for project rules, or plain text for user rules
   * - Application
     - Humans interpret and apply guidance as needed
     - AI models automatically apply rules at the start of each context, guiding behavior and responses
   * - Organization
     - Documentation is organized by topic, section, or navigation structure
     - Rules are organized by directory, file, or workflow, and can be nested for specificity
   * - Examples
     - Provided as code snippets, templates, or best practices in docs
     - Included directly in rules or referenced files for model context
   * - Updates
     - Documentation is updated as needed, but may not be immediately reflected in user behavior
     - Rule changes are version-controlled and immediately affect model behavior
   * - Collaboration
     - Shared via documentation, wikis, or internal docs
     - Rules can be shared via version control, symlinks, or dedicated repositories
   * - Best Practices
     - Focused, actionable, and clear documentation is recommended
     - Rules should be concise, composable, and provide concrete examples; avoid vague guidance

Key Contrasts (Cursor Rules)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Persistence & Automation:** Rules provide persistent, automated guidance to AI models, while humans must remember or reference documentation.
- **Scoping & Organization:** Rules can be scoped to specific directories or workflows, ensuring relevant guidance is always applied, while human docs are generally broader.
- **Format & Application:** Rules use structured formats (MDC, plain text) for machine consumption, while human docs are written for readability and exploration.

Key Similarities (Cursor Rules)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Both benefit from clear, focused, and actionable guidance.
- Both use examples and templates to illustrate best practices.
- Both can be version-controlled and collaboratively maintained.

Reference: `Cursor Docs: Rules <https://docs.cursor.com/context/rules>`_

Compare/Contrast: Writing Docs for AI Agents vs. Humans (Claude Code Best Practices)
-----------------------------------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Aspect
     - Writing for Humans
     - Writing for AI Agents (LLMs)
   * - Contextual Guidance
     - Provided in README, guides, or internal docs
     - Provided in `CLAUDE.md` files, automatically pulled into context for agentic coding
   * - Format
     - Human-readable, flexible, often narrative
     - Concise, human-readable but optimized for LLM context; Markdown recommended
   * - Scope
     - Project-wide or section-specific, but not always surfaced at the right time
     - Can be repo-wide, directory-specific, or user-specific; contextually surfaced as needed
   * - Updates
     - Updated as needed, but may not be referenced by all users
     - Iteratively refined for prompt effectiveness; changes immediately affect agent behavior
   * - Examples & Commands
     - Provided in documentation, may be scattered
     - Centralized in `CLAUDE.md` or `.claude/commands` for agent use
   * - Tooling
     - Described in prose, may require manual setup
     - Explicitly listed and allowed for agentic automation and safety
   * - Collaboration
     - Shared via docs, wikis, or code comments
     - Shared via version control, checked-in config, or team-wide `CLAUDE.md`
   * - Automation
     - Humans interpret and execute workflows
     - Agents can automate workflows, use checklists, and run commands as described

Key Contrasts (Claude Code)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Contextual Automation:** LLMs use `CLAUDE.md` and command files for persistent, actionable context, while humans rely on scattered documentation.
- **Prompt Optimization:** LLM docs are iteratively refined for effectiveness in agentic workflows, while human docs may not be as tightly coupled to usage.
- **Tooling & Safety:** LLMs require explicit tool allowlists and command documentation for safe automation, while humans rely on judgment.

Key Similarities (Claude Code)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Both benefit from clear, concise, and actionable documentation.
- Both use examples and checklists to guide workflows.
- Both can share and version documentation for team-wide consistency.

Reference: `Claude Code: Best practices for agentic coding <https://www.anthropic.com/engineering/claude-code-best-practices>`_

Compare/Contrast: Writing Docs for AI Agents vs. Humans (YCombinator Discussion)
-------------------------------------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Aspect
     - Writing for Humans
     - Writing for AI Agents (LLMs)
   * - Audience
     - Assumes human reasoning, inference, and exploration
     - Assumes LLMs need explicit, context-rich, and unambiguous information
   * - Structure
     - Can be narrative, exploratory, or reference-based
     - Should be highly structured, with clear sections and explicit relationships
   * - Context
     - Can rely on user memory, prior reading, or intuition
     - Each section must be self-contained; avoid references like "see above"
   * - Visuals & Layout
     - Can use diagrams, tables, and formatting for meaning
     - Must provide text equivalents and avoid layout-dependent meaning
   * - Jargon & Assumptions
     - Can use domain-specific language, explained as needed
     - Should minimize jargon and make all assumptions explicit
   * - Discoverability
     - Relies on navigation, search, and user exploration
     - Relies on chunking, retrieval, and explicit linking for LLMs
   * - Error Handling
     - General troubleshooting, may rely on user interpretation
     - Include exact error messages and solutions for direct matching
   * - Updates
     - Updated for human readers, may lag behind usage
     - Should be kept current, as LLMs may ingest outdated info

Key Contrasts (YCombinator)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Explicitness:** LLMs require all context and relationships to be explicit, while humans can infer and explore.
- **Chunking & Retrieval:** LLMs process docs in chunks, so each must be self-contained; humans can piece together information from multiple sources.
- **Visuals:** LLMs need text-based alternatives for visuals, while humans can interpret diagrams and layout.

Key Similarities (YCombinator)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Both benefit from clarity, structure, and up-to-date information.
- Both require actionable, well-organized documentation for effective use.

Reference: `YCombinator: Writing docs for LLMs vs. humans (discussion) <https://news.ycombinator.com/item?id=44314423>`_ 