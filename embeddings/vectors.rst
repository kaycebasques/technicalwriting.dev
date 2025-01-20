.. _vectors:

=======
Vectors
=======

I want to understand the math behind :ref:`embeddings <underrated>`
more deeply. Vectors seem like a good place to start. 

---------------------
Why focus on vectors?
---------------------

Vectors seem to be the mathematical foundation of embeddings.
All embeddings are vectors (but not all vectors are embeddings).
Maybe I should say "most embeddings are vectors", not "all embeddings
are vectors". Maybe there are some niche types of embeddings that
are not represented as vectors. It seems safe to assume that
the great majority (over 90%) of embeddings are vectors.

------------------------------------------
Why are embeddings represented as vectors?
------------------------------------------

Because machine learning (ML) researchers decided to use vectors.
That may sound like a superficial answer, but I think it's important
to remember the deeply academic foundation of ML. This academic
foundation makes my quest to understand vectors easier. I can probably trace back the
first usage of the term "embeddings" to a specific research paper.
And that research paper probably makes a clear case for why embeddings
need to be vectors.

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
