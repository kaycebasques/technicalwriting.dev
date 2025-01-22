.. _vectors:

=======
Vectors
=======

(This post is a work in progress.)

:ref:`Embeddings <underrated>` may be an important new tool for technical
writers. An embedding provides a numerical representation of a text's
semantics. We can mathematically compare the embedding of one text
against the embedding of another text and determine whether they're
semantically similar. This has many potential applications in technical
writing.

----------
Motivation
----------

But what does it mean to "represent a text's semantics as numbers"?
And how exactly does the mathematical comparison of one embedding
against another embedding work? If I'm going to seriously adopt
embeddings in my work as a technical writer, I should be able to
provide detailed answers to these questions. Also, having a deeper
understanding of the math behind embeddings is almost guaranteed
to help me use embeddings more effectively.

Where to begin my journey to understand the math behind embeddings?
Vectors seem like a good place to start.

---------------------
Why focus on vectors?
---------------------

Because embeddings typically\ :sup:`1` *are* vectors. Vectors are a math
(and physics) concept. Embeddings are an application of the concept.

:sup:`1` Non-vector embeddings are also possible, hence the
"typically". In practice it seems like embeddings are almost always
vector-based.

-----------------------------
What do embeddings look like?
-----------------------------

You input some text, and you get back a long array of numbers.
Here's how you generate an embedding with the Gemini API:

.. code-block:: pycon

   >>> import google.generativeai as gemini
   >>> gemini.configure(api_key='…')
   >>> text = 'Hello, world!'
   >>> response = gemini.embed_content(
   ...     model='models/text-embedding-004',
   ...     content=text,
   ...     task_type='SEMANTIC_SIMILARITY'
   ... )
   >>> embedding = response['embedding']
   >>> embedding
   [-0.029905086, 0.008915291, -0.07544613, …, 0.011311127]
   >>> len(embedding)
   768

No matter the size of your input text, you always get back an
array of the same length. E.g. in the previous code block, suppose that
the value of the ``text`` variable is the complete text of an entire
document rather than a short sentence (``Hello, world!``). The Gemini
embedding model will still return a list of 768 numbers.

Each particular number in the list will always be within a particular
range. E.g. the Gemini embedding model always returns a number between
-1 and +1.

Even if you still have no idea what an embedding is (see
:ref:`underrated-intuition`) you are hopefully starting to see
how embeddings make it possible to mathematically analyze docs.

-----------------
What is a vector?
-----------------

.. _Linear Algebra For Dummies: https://www.dummies.com/book/academics-the-arts/math/algebra/linear-algebra-for-dummies-282354/

According to `Linear Algebra For Dummies`_\ :sup:`2`, a vector
is just an ordered collection of numbers.

:sup:`2` I know that some people are turned off by the "Dummies"
name but this is the best book I've found on the topic yet. By
"best" I mean it provides a lot of context, gives a lot of examples,
and walks through each example in detail.

------------------------------------------
Why are embeddings represented as vectors?
------------------------------------------

.. _cop out: https://www.etymonline.com/word/cop%20out

Because machine learning (ML) researchers decided to use vectors.
That may sound like a `cop out`_, but I think it's useful 
to remember where all this stuff comes from. We can probably
trace the invention of vector-based embeddings back to specific
research papers. Those research papers probably provide rationale
for 

But why did ML researchers choose vectors?
==========================================

.. _neptune.ai blog post: https://neptune.ai/blog/understanding-vectors-from-a-machine-learning-perspective

This `neptune.ai blog post`_ suggests at least 3 different reasons:

First reason:

  Machines can’t read text or look at images like you and me. They need 
  input to be transformed or encoded into numbers.

Second reason: 

  The goal of most ML projects is to create a model that performs some
  function. It could be classifying text, or predicting house prices,
  or identifying sentiment. In deep learning models, this is achieved
  via a neural network where the neural network layers use linear
  algebra (like matrix and vector multiplication) to tune your parameters.

Third reason:

  The output of our ML model can be a range of different entities depending
  on our goal. If we’re predicting house prices, the output will be a
  number. If we’re classifying images, the output will be a category of
  image. The output, however, can be a vector as well. For example, NLP
  models like the Universal Sentence Encoder (USE) accept text and then
  output a vector (called an embedding) representing the sentence. You can
  then use this vector to perform a range of operations, or as an input into
  another model.

.. https://neptune.ai/blog/understanding-vectors-from-a-machine-learning-perspective
.. https://machinelearningmastery.com/gentle-introduction-vectors-machine-learning/
