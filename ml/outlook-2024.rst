.. _genai-outlook-2024:

==================
GenAI Outlook 2024
==================

2024 Dec 31

Back in March 2023 I published :ref:`genai-outlook-2023`.
With less than 12 hours remaining in 2024 I have managed to keep
my yearly streak going. Here's my 2024 outlook regarding the
impact of generative AI on my field, technical writing.

----------------------
Review of 2023 outlook
----------------------

Here's the current status of each of the ideas mentioned in
:ref:`genai-outlook-2023`.

Job loss
========

Back in March 2023 (when I wrote the outlook), a lot of technical writers
were worried that GenAI would automate our (very enjoyable!) jobs away. This
has not objectively happened at scale so far. I am aware of only one case
where a technical writer *maybe* lost their job because of GenAI.

Automation
==========

In the 2023 outlook I had GPT-4 brainstorm ways that LLMs might automate
aspects of technical writing. Here's a quick summary of how much each of
those ideas has been adopted up until now.

(If I say "no one is doing this" but you are in fact doing that thing,
aou're welcome to send me a message and I will update the post to
mention your work.)

Basic content generation
------------------------

  ChatGPT can generate paragraphs or sections based on given topics or
  outlines, providing a starting point for technical writers. This can speed
  up the content creation process and help maintain consistency in writing.

.. _automate release notes authoring: https://idratherbewriting.com/ai/automating-linking.html
.. _extensively automating all first draft work: https://aws.amazon.com/blogs/machine-learning/how-skyflow-creates-technical-content-in-days-using-amazon-bedrock/

There's a lot of this happening. Tom Johnson has been using a prompt
engineering approach to `automate release notes authoring`_. I have also
automated some of my changelog process with moderate success. Manny Silva
is `extensively automating all first draft work`_.

Data analysis and interpretation
--------------------------------

  AI can analyze large datasets and generate summaries, trends, or insights
  that can be incorporated into technical documents.

.. _context window: https://www.ibm.com/think/topics/context-window

Summarization is covered below.

Regarding trends, I'm not aware of anyone using LLMs for this task
and I actually don't even know what this would look like.

Regarding insights, I can recall some one-off instances of
technical writers using large `context window`_ models to help
think through some particular problems in their docs. E.g. they
would provide all of their docs as input and then ask the LLM
pointed questions related to those issues.

Formatting and template creation
--------------------------------

  AI can automatically apply formatting and styling rules to documents,
  ensuring they adhere to specific guidelines or templates.

.. _feature engineering: https://builtin.com/articles/feature-engineering

I personally worked on this a lot in 2023. My current opinion is that
it's feasible but requires a fine-tuned model, which means a lot of
`feature engineering`_, which means a lot of upfront toil and careful design.

Grammar and spell-checking
--------------------------

  ChatGPT can identify and correct grammatical errors, spelling mistakes, and
  other language inconsistencies, leading to higher-quality content.

I have heard of technical writers using LLMs for one-off editing tasks.
E.g. they were given the first draft of a new doc written by a software
engineer (or product manager, or whatever) and were told that the doc
must be published in a couple hours. The first draft had lots of grammatical
errors and typos. The technical writers just fed the first draft through an
LLM to quickly fix all the flagrant issues.

Terminology consistency
-----------------------

  AI can help maintain the use of consistent terminology and phrases throughout
  a document, reducing confusion for readers.

This still sounds feasible, but I haven't heard of anyone using LLMs for this task.

Content summarization
---------------------

  ChatGPT can create concise summaries or abstracts of longer, more complex
  documents, making them more accessible to a wider audience.

I'm surprised that there hasn't been more adoption here. LLMs reliably
generate high-quality summaries when given the content-to-summarize as input.
It's one of the few use cases where there's very little risk of hallucination
in my experience. Yet I don't see many docs sites offering
LLM-generated summaries and I'm not aware of many teams using LLMs to
systematically generate summary-like content behind-the-scenes, such as the
opening or closing paragraphs of docs.

Content translation
-------------------

  AI language models can translate technical content into multiple languages,
  helping to disseminate information globally.

I haven't seen a big uptick in more docs sites being translated into
multiple languages. I do think that LLMs have made it more feasible but I
imagine that the main constraint now is engineering resources. E.g. you need
to dedicate engineers to building out the automated translation pipeline for
your docs site.

FAQ generation
--------------

  AI can identify common questions related to a topic and generate clear,
  concise answers.

Not aware of anyone doing this.

Metadata generation
-------------------

  AI can automatically generate metadata for technical documents, such as
  keywords, tags, and descriptions, improving searchability and
  discoverability.

Ditto, haven't heard of anyone doing this.

Plagiarism detection
--------------------

  AI can identify potential plagiarism cases in technical
  writing and suggest alternative content to maintain originality.

Ditto again, not aware of anyone doing this.
