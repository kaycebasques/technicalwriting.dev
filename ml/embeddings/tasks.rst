.. _tasks:

====================================================
Understanding task types in the Gemini Embedding API
====================================================

.. _models.embedContent: https://ai.google.dev/api/embeddings#method:-models.embedcontent

The `models.embedContent`_ endpoint of the Gemini Embedding API supports a
``taskType`` parameter.  This parameter lets you specify what kind of task the
embedding will be used for. I would like to understand this "task type" thing
at a deeper level. These are my notes.

----------
Motivation
----------

.. _Task types: https://ai.google.dev/gemini-api/docs/embeddings#task-types

`Task types`_ from the official docs describes the motivation like this:

  Task types enable you to generate optimized embeddings for specific tasks,
  saving you time and cost and improving performance.

That same section provides this example:

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

.. _TaskType: https://ai.google.dev/api/embeddings#v1beta.TaskType

The `TaskType`_ enum supports the following values. The descriptions are pulled
verbatim from the official docs.

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

.. _Gemini Embedding paper: https://arxiv.org/pdf/2503.07891
.. _Gecko paper: https://arxiv.org/pdf/2403.20327

Section 3.2. from the `Gemini Embedding paper`_ mentions that
each training example includes a task string:

  The Gemini Embedding model was trained with a noise-contrastive estimation (NCE)
  loss with inbatch negatives. The exact loss differs slightly depending on the
  stage of training. In general, a training example includes a query 𝑞\ :sub:`𝑖`,
  a positive target 𝑝\ :sup:`+`\ :sub:`𝑖` and (optionally) a hard negative target
  𝑝\ :sup:`−`\ :sub:`𝑖`. Each example also has a prescribed task string 𝑡, for
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

  We first prepend a dataset-specific task feature 𝑡 before each
  query, so each query is informed of which task is being optimized.

.. _unlabeled: https://en.wikipedia.org/wiki/Labeled_data

The Gecko paper also discusses a clever synthetic data generation technique
related to task types. They use a text generation model to generate a relevant
task and query for a given `unlabeled`_ passage from the web. Presumably, the
text generation model is told to pick from one of the options described in
:ref:`types`.

---------
Inference
---------

Suppose you invoke the Gemini Embedding API with a task type specified, like this:

.. code-block:: py

   result = client.models.embed_content(
       model="gemini-embedding-exp-03-07",
       contents="I’m outta here! I’m not gonna play second… banana-fiddle to some stupid old baby.",
       config=types.EmbedContentConfig(task_type="CLUSTERING")
   )

.. _NV-Embed-v2: https://huggingface.co/nvidia/NV-Embed-v2

How is the task type used at inference-time? I don't know. I couldn't find anything
in the official docs about this. However, when I look at the code example for
`NV-Embed-v2`_, I see the same instruction-prepending pattern, where the task type
is literally prepended as an instruction before the text that you want to embed:

.. code-block:: py

   task_name_to_instruct = {"example": "Given a question, retrieve passages that answer the question",}

   query_prefix = "Instruct: "+task_name_to_instruct["example"]+"\nQuery: "
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

   # normalize embeddings
   query_embeddings = F.normalize(query_embeddings, p=2, dim=1)
   passage_embeddings = F.normalize(passage_embeddings, p=2, dim=1)
