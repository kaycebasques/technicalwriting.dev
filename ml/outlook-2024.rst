.. _genai-outlook-2024:

================================================================
2024 Machine Learning Review & Forecasts (For Technical Writing)
================================================================

2024 Dec 31

Back in March 2023 I published :ref:`genai-outlook-2023`.
With less than 12 hours remaining in 2024 I have managed to keep
my yearly streak going. This post recaps how much (or little)
the ideas mentioned in :ref:`genai-outlook-2023` have panned
out, and then discusses future trends that I'm monitoring.

.. note::

   This year's post is called ``Machine Learning Review`` rather than
   ``GenAI Outlook`` to reflect the widening scope of discussion that
   I want to have. GenAI is a subset of machine learning (ML), and
   machine learning is a subset of artificial intelligence (AI). Over the
   past year as I've been doing various crash courses on ML, I've realized
   that there are lots of ways that ML and technical writing interact,
   outside of the narrow subfield of GenAI.

----------------------
Review of 2023 outlook
----------------------

First, status updates on the ideas mentioned in :ref:`genai-outlook-2023`.

Job loss
========

When I wrote the 2023 outlook, a lot of technical writers
were worried that GenAI would automate away our (very enjoyable!) jobs. This
has not objectively happened at scale so far. I am aware of only one case
where a technical writer *maybe* lost their job because of GenAI.

Automation
==========

.. _LLMs: https://en.wikipedia.org/wiki/Large_language_model

In the early days of the GenAI explosion, remember how seemingly every
blog post included verbatim Q&A discussion with ChatGPT? "Here's what
ChatGPT has to say on the matter." I did that in my 2023 outlook. I asked
GPT-4 to list out what parts of technical writing are potentially automatable
with `LLMs`_. Here's a quick summary of how much each of those ideas has
been adopted to date.

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
is `extensively automating all first draft work`_. I can think of many
more examples along these lines.

It's an open secret that writing is hard, even for technical writers.

Data analysis and interpretation
--------------------------------

  AI can analyze large datasets and generate summaries, trends, or insights
  that can be incorporated into technical documents.

.. _context window: https://www.ibm.com/think/topics/context-window

More on summarization later.

Regarding trends, I'm not aware of anyone using LLMs for this task
and I actually don't even know what "generating trends" would look like.

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
must be published in a couple hours. The first draft was riddled with grammatical
errors and typos. To meet the ridiculous deadline (pro tip: don't give your
technical writers ridiculous deadlines) the writers fed the first draft through
an LLM to quickly fix the most flagrant issues.

Terminology consistency
-----------------------

  AI can help maintain the use of consistent terminology and phrases throughout
  a document, reducing confusion for readers.

This still sounds feasible, but I haven't heard of anyone using LLMs for this task.
It may require a lot of upfront work around defining the preferred terms and
phrases. Simply identifying potential terminology inconsistency might be a lower
hanging fruit. E.g. the model produces a report telling you that you used
``foo`` on line 32 and ``bar`` on line 64 yet ``foo`` and ``bar`` seem to
relate to the same concept.

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

.. _Sphinx: https://www.sphinx-doc.org/en/master/

I haven't seen a big uptick in more docs sites being translated into
multiple languages. I do think that LLMs have made it more feasible but I
imagine that the main constraint now is engineering resources. E.g. you need
to dedicate engineers to building out the automated translation pipeline for
your docs site. Maybe the static site generators and content management systems
will start solving this for us. E.g. just give `Sphinx`_ an API key to your
favorite GenAI service, and it will take care of the end-to-end translation
pipeline: determining what docs need to be updated, using the GenAI service
to translate the doc, etc.

FAQ generation
--------------

  AI can identify common questions related to a topic and generate clear,
  concise answers.

Not aware of anyone doing this. I still think that Q&A will become
increasingly important over time. More on that below.

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

----------------------
Review of other trends
----------------------

My initial 2023 outlook left out some important stuff. I want to
provide status updates on those things now.

RAG chatbots have not taken over the docs world
===============================================

.. _retrieval-augmented generation: https://en.wikipedia.org/wiki/Retrieval-augmented_generation

Gather a list of 1000 docs sites from any domain (or a mix of domains). You will find
that a supermajority (+75%) of them have not shipped a companion `retrieval-augmented generation`_
(RAG) chatbot to supplement the traditional web-based docs experience. Even the
OpenAI docs don't have one.

I actually think that RAG chatbots can be very valuable, and I have heard
a few stories of companies enjoying significant productivity boosts thanks
to their internal RAG chatbots. But the objective fact remains: 
most docs sites have not shipped a RAG chatbot.

Policy is a nightmare
=====================

For the minority of technical writers that are interested in seriously adopting GenAI
into their workflows, confusing policy seems to be a significant
obstacle to adoption. Across many companies I have heard technical writers
say that their conversations revolve around these questions:

* "What GenAI services are we even approved to use?"
* "Can we really trust GenAI service XYZ with our non-public data?"
* "Are we setting our company up for copyright issues in the future?"

--------------
2025 forecasts
--------------

Technical writers will continue to ignore GenAI at their own peril
==================================================================

I will venture to say that a simple majority (+50%) of technical writers
are not interested in integrating GenAI into their work practices for
a variety of reasons: fear of accidentally automating themselves out of a
job, environmental concerns, copyright ethics, etc. So I expect adoption
of GenAI in technical writing to continue to be slow for that reason alone.

Technical writers ignore GenAI at their own peril, though. Here's a potential
playbook for a lot of unnecessary pain in the future:

#. Technical writing team at company XYZ hates anything that even smells of GenAI.
   As a consequence they do not pay any attention to the space and definitely do
   not do any experimentation.

#. Some desperate Y Combinator startup ABC has pivoted for the 3rd time into
   documentation automation.

#. Startup ABC's product is not anywhere close to being able to actually
   fully automate documentation work, but their sales team is very good.

#. The very persuasive sales team at startup ABC convinces company XYZ
   leadership that its product can replace the technical writing team. Company
   XYZ leadership duly lays off its technical writing team.

#. 9 months later, company XYZ can conclusively state that relying on
   startup ABC's "fully automated documentation solution" has been a
   disaster. Company XYZ also learned, however, that those introverted,
   non-unionized technical writers who never seem to be able to prove the
   exact ROI of their work can be hired back at much less cost as temps
   and contractors.

Don't let startup ABC determine your future. Make an earnest effort
to adopt GenAI where it brings true value, establishing yourself as a
forward-thinking expert in the eyes of your company leadership in the process.
As you do your own experimentation and see firsthand how inadequate or
cost-prohibitive GenAI is for a certain task, show your leaders. "Yes, I
tried that. Here's the demo. See for yourself; the results are pretty bad.
I estimate it will take a full-time SWE 3 months to make this bulletproof.
Is the ROI still worth it?"

Supervised learning
===================

There are *so many* areas in technical writing where a supervised
learning approach can provide significant improvement over the status
quo.

.. _fine-tuning: https://platform.openai.com/docs/guides/fine-tuning

If you're a technical writer and you don't know what I mean by
supervised learning, take this as a suggestion to do some self-study.
Hint: `fine-tuning`_ is a form of supervised learning.

FAQs, Q&A, etc.
===============

TBD

Translation pipelines solved for us
===================================

TBD
