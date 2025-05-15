.. _tasks:

====================================================
Understanding task types in the Gemini Embedding API
====================================================

.. _models.embedContent: https://ai.google.dev/api/embeddings#method:-models.embedcontent
.. _official docs: https://ai.google.dev/api/embeddings
.. _Gemini Embedding paper: https://arxiv.org/pdf/2503.07891
.. _Gecko paper: https://arxiv.org/pdf/2403.20327
.. _Task types: https://ai.google.dev/gemini-api/docs/embeddings#task-types
.. _TaskType: https://ai.google.dev/api/embeddings#v1beta.TaskType
.. _unlabeled: https://en.wikipedia.org/wiki/Labeled_data
.. _NV-Embed-v2: https://huggingface.co/nvidia/NV-Embed-v2
.. _python-genai: https://github.com/googleapis/python-genai
.. _Python client: https://github.com/googleapis/python-genai/blob/copybara/747683395/google/genai/models.py#L604
.. _discussion: https://news.ycombinator.com/item?id=43964392
.. _gut check: https://www.merriam-webster.com/dictionary/gut%20check
.. _Visualizing embeddings with t-SNE: https://github.com/google/generative-ai-docs/blob/main/site/en/gemini-api/tutorials/clustering_with_embeddings.ipynb
.. _Spruce Goose: https://en.wikipedia.org/wiki/Hughes_H-4_Hercules
.. _k-means: https://developers.google.com/machine-learning/glossary#k-means

The `models.embedContent`_ method of the Gemini Embedding API supports a
``taskType`` parameter.  This parameter lets you specify what kind of task the
embedding will be used for. Let's try to deduce how this "task type" thing
works by poring over the public information that's available to us, such as the
`official docs`_, the `Gemini Embedding paper`_, and the `python-genai`_ source code.

----------
Motivation
----------

The `Task types`_ section from the official docs describes the value proposition
like this:

  Task types enable you to generate optimized embeddings for specific tasks,
  saving you time and cost and improving performance.

And they provide this example:

  When building Retrieval Augmented Generation (RAG) systems, a common design is
  to use text embeddings to perform a similarity search. In some cases this can
  lead to degraded quality, because questions and their answers are not
  semantically similar. For example, a question like "Why is the sky blue?" and
  its answer "The scattering of sunlight causes the blue color," have distinctly
  different meanings as statements, which means that a RAG system won't
  automatically recognize their relation.

The "improve performance" argument makes sense to me, but I don't understand how
task types would save time or cost. If anything, it seems like time and cost increase,
because I might need to generate multiple embeddings for a given passage, one for each
task type that's relevant to my project.

.. _types:

--------------
Types of tasks
--------------

The `TaskType`_ enum supports the following values. (The descriptions are pulled
verbatim from the official docs, hence the quotes.)

* ``TASK_TYPE_UNSPECIFIED``: "Unset value, which will default to one of the other enum values."
* ``RETRIEVAL_QUERY``: "Specifies the given text is a query in a search/retrieval setting."
* ``RETRIEVAL_DOCUMENT``: "Specifies the given text is a document from the corpus being searched."
* ``SEMANTIC_SIMILARITY``: "Specifies the given text will be used for STS."
* ``CLASSIFICATION``: "Specifies that the given text will be classified."
* ``CLUSTERING``: "Specifies that the embeddings will be used for clustering."
* ``QUESTION_ANSWERING``: "Specifies that the given text will be used for question answering."
* ``FACT_VERIFICATION``: "Specifies that the given text will be used for fact verification."
* ``CODE_RETRIEVAL_QUERY``: "Specifies that the given text will be used for code retrieval."

--------
Training
--------

How is the Gemini Embedding model trained on task types?

Section 3.2. from the `Gemini Embedding paper`_ mentions that
each training example includes a task string:

  The Gemini Embedding model was trained with a noise-contrastive estimation (NCE)
  loss with inbatch negatives. The exact loss differs slightly depending on the
  stage of training. In general, a training example includes a query :math:`q_i`,
  a positive target :math:`p\ \overset{+}{_i}` and (optionally) a hard negative target
  :math:`p\ \overset{-}{_i}`. Each example also has a prescribed task string :math:`t`, for
  example "question answering" or "fact checking", describing the nature of the task.

Section 1. suggests that the `Gecko paper`_ has more information about task types:

  Building upon the success of Gecko (Lee et al., 2024), we incorporate task
  prompts and a pre-finetuning stage to enhance performance.

Looking through the Gecko paper, it seems like the task type is basically just
explicitly prepended as an instruction in the training input:

  Previously, Dai et al. (2022) demonstrated that there exist different
  intents for different retrieval tasks. For instance, given a search query, 
  users might want to find a similar query, or they might want to read a
  passage that directly answers the query. Recent work has explored implementing
  a retriever that changes the retrieval behavior for different intents. Asai
  et al. (2022) and Su et al. (2022) introduce “retrieval with instructions,”
  where a dense retriever is trained to follow an instruction that was given
  along with the query.

Another line from the Gecko paper suggesting that the task type is explicitly
prepended as an instruction:

  We first prepend a dataset-specific task feature :math:`t` before each
  query, so each query is informed of which task is being optimized.

The Gecko paper also discusses a clever synthetic data generation technique
related to task types. They use a text generation model to generate a relevant
task and query for a given `unlabeled`_ passage from the web. Presumably, the
text generation model is asked which of the task type options, as described in
:ref:`types`, is most appropriate for the passage.

---------
Inference
---------

Suppose you invoke the Gemini Embedding API with a task type specified, like this:

.. code-block:: py

   import os

   from google import genai
   from google.genai import types

   gemini = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
   result = gemini.models.embed_content(
       model="gemini-embedding-exp-03-07",
       contents="I’m outta here! I’m not gonna play second… banana-fiddle to some stupid old baby.",
       config=types.EmbedContentConfig(task_type="CLUSTERING")
   )

How is the task type used at inference-time? I don't know. I couldn't find anything
in the official docs about this. The `Python client`_ just passes on the task type
as part of the request. None of the prompt construction happens client-side.

However, when I look at the code example for `NV-Embed-v2`_, it uses an
instruction-prepending pattern that seems similar to what the Gecko paper mentions.
The task type is literally prependend as an instruction before the text that you want
to embed:

.. code-block:: py

   # …

   task_name_to_instruct = {"example": "Given a question, retrieve passages that answer the question"}

   query_prefix = "Instruct: " + task_name_to_instruct["example"] + "\nQuery: "
   queries = [
       'are judo throws allowed in wrestling?', 
       'how to become a radiology technician in michigan?'
   ]

   # No instruction needed for retrieval passages
   passage_prefix = ""
   passages = [
       "Yes, judo throws are allowed in freestyle and folkstyle wrestling.",
       "Below are the basic steps to becoming a radiologic technologist in Michigan."
   ]

   # load model with tokenizer
   model = AutoModel.from_pretrained('nvidia/NV-Embed-v2', trust_remote_code=True)

   # get the embeddings
   max_length = 32768
   query_embeddings = model.encode(queries, instruction=query_prefix, max_length=max_length)
   passage_embeddings = model.encode(passages, instruction=passage_prefix, max_length=max_length)

   # …

--------
Variance
--------

Suppose that we generate an embedding for eack task type. The target text
(``mango``) remains the same. The only difference between the embeddings is the
task type. How much do each of these embeddings vary from one another?

.. literalinclude:: variance.py
   :language: py

I was curious about two things:

* Element-wise changes. Think of each embedding as a list of floats. Do any of the elements
  at a given index ever remain the same between the two lists? E.g. is
  ``embedding_a[5] == embedding_b[5]`` ever true?
* Vector-wise comparison. It seems like dot product is a better measure here rather than
  cosine similarity because dot product measures both magnitude and direction whereas cosine
  similarity only measures direction. But I also read recently somewhere that the two
  calculations are equivalent when the embedding is normalized, i.e. each dimension is
  pinned between -1 and 1. I think that's what "normalized" means here, not sure about that either.

Here are the results:

.. code-block:: output

   ---
   Comparing TASK_TYPE_UNSPECIFIED to SEMANTIC_SIMILARITY
   Identical dimensions: 0
   Dot product: 0.7835852194453554
   ---
   Comparing RETRIEVAL_QUERY to SEMANTIC_SIMILARITY
   Identical dimensions: 0
   Dot product: 0.7835852194453554
   ---
   Comparing RETRIEVAL_DOCUMENT to SEMANTIC_SIMILARITY
   Identical dimensions: 0
   Dot product: 0.8088390644721011
   ---
   Comparing CLASSIFICATION to SEMANTIC_SIMILARITY
   Identical dimensions: 0
   Dot product: 0.7930198656607292
   ---
   Comparing CLUSTERING to SEMANTIC_SIMILARITY
   Identical dimensions: 0
   Dot product: 0.7718854611562452
   ---
   Comparing QUESTION_ANSWERING to SEMANTIC_SIMILARITY
   Identical dimensions: 0
   Dot product: 0.8051469937783085
   ---
   Comparing FACT_VERIFICATION to SEMANTIC_SIMILARITY
   Identical dimensions: 0
   Dot product: 0.8126973065615051
   ---
   Comparing CODE_RETRIEVAL_QUERY to SEMANTIC_SIMILARITY
   Identical dimensions: 0
   Dot product: 0.7424771969498801

Insights:

* I think it's safe to assume that all dimensions always change
  depending on the task type. This is starting to make sense after what
  I recently learned from this `discussion`_.

* Given that the dot products for ``TASK_TYPE_UNSPECIFIED`` and
  ``RETRIEVAL_QUERY`` are identical, we can infer that ``TASK_TYPE_UNSPECIFIED``
  defaults to ``RETRIEVAL_QUERY``.

* ``CODE_RETRIEVAL_QUERY`` is the least similar task type to ``SEMANTIC_SIMILARITY``,
  which makes intuitive sense to me because code retrieval is a very different type
  of task.

----------
Clustering
----------

Let's wrap this up with a `gut check`_ of the ``CLUSTERING`` task type. See
`Visualizing embeddings with t-SNE`_ if you're not familiar with clustering.

For our experiment, we'll provide a list of related terms (fruit names) and one
unrelated term (`Spruce Goose`_). We'll use ``mango`` as the baseline again.
First, we'll generate an embedding for each term, with ``CLUSTERING`` specified
as the task type. When we calculate the dot product for ``mango`` against all
the other terms, the dot product should be high for the other fruit terms, and
much lower for ``Spruce Goose``. We'll run the calculation again, but this time
we'll use ``CODE_RETRIEVAL_QUERY``. All of the dot products should be much
lower, because this is not a relevant task type.

This is a very naive, simple experiment. `Visualizing embeddings with t-SNE`_ suggests
that other algorithms like `k-means`_ are required for clustering tasks, not dot product.
But nonetheless it seems valid to use dot product here for some very basic
intuition building.

Here's the experiment:

.. literalinclude:: clusters.py
   :language: py

And the results:

.. code-block:: output

   ==========
   CLUSTERING
   ---
   Comparing strawberry to mango
   Dot product: 0.9185685857057041
   ---
   Comparing watermelon to mango
   Dot product: 0.9190111016753526
   ---
   Comparing orange to mango
   Dot product: 0.890292211194551
   ---
   Comparing jabuticaba to mango
   Dot product: 0.8834979090318306
   ---
   Comparing feijoa to mango
   Dot product: 0.8872394629362534
   ---
   Comparing Spruce Goose to mango
   Dot product: 0.809432604102317
   ==========
   CODE_RETRIEVAL_QUERY
   ---
   Comparing strawberry to mango
   Dot product: 0.8113004271316064
   ---
   Comparing watermelon to mango
   Dot product: 0.8067946179014334
   ---
   Comparing orange to mango
   Dot product: 0.7946552697681786
   ---
   Comparing jabuticaba to mango
   Dot product: 0.8072596994606935
   ---
   Comparing feijoa to mango
   Dot product: 0.8202925440462843
   ---
   Comparing Spruce Goose to mango
   Dot product: 0.7863710189133477

Hypotheses confirmed. For the ``CLUSTERING`` embeddings, the dot products
between the fruit terms are between 0.88 and 0.91. Whereas the dot product
between ``mango`` and ``Spruce Goose`` is noticeably lower at 0.80. And
the dot products for all the ``CODE_RETRIEVAL_QUERY`` embeddings are all
noticeably lower than the ``CLUSTERING`` embeddings.
