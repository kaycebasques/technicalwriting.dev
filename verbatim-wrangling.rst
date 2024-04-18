.. _verbatim-wrangling:

=================================================
Wrangling verbatim text in Doxygen+Breathe+Sphinx
=================================================

.. _small CLs: https://google.github.io/eng-practices/review/developer/small-cls.html
.. _verbatim: https://www.doxygen.nl/manual/commands.html#cmdverbatim
.. _Handling Leading Slashes: https://www.doxygen.nl/manual/commands.html#cmdverbatim

2023 Jun 9

The Pigweed docs (powered by Sphinx) are using Doxygen and Breathe to
single-source their API reference documenation. Last night I was having
trouble getting a plaintext diagram to render correctly. This is how I
fixed it.

I am taking a `small CLs`_ approach to converting the Pigweed docs to use Doxygen.
I am converting one section/function at a time. Last night I was trying to convert
this section:

.. code-block:: none

   // The "Block" type is intended to be a building block component for
   // allocators. In the this design, there is an explicit pointer to next and
   // prev from the block header; the size is not encoded. The below diagram shows
   // what this would look like for two blocks.
   //
   //   .------+---------------------------------.-----------------------------
   //   |            Block A (first)             |       Block B (second)
   //
   //   +------+------+--------------------------+------+------+---------------
   //   | Next | Prev |   usable space           | Next | Prev | usable space..
   //   +------+------+--------------------------+------+--+---+---------------
   //   ^  |                                     ^         |
   //   |  '-------------------------------------'         |
   //   |                                                  |
   //   '----------- Block B's prev points to Block A -----'
   //
   // One use for these blocks is to use them as allocations, where each block
   // represents an allocation handed out by malloc(). These blocks could also be
   // used as part of a slab or buddy allocator.
   //
   // Each block also contains flags for whether it is the last block (i.e. whether
   // the "next" pointer points to a valid block, or just denotes the end of this
   // block), and whether the block is in use. These are encoded into the last two
   // bits of the "next" pointer, as follows:
   //
   //  .-----------------------------------------------------------------------.
   //  |                            Block                                      |
   //  +-----------------------------------------------------------------------+
   //  |              Next            | Prev |         usable space            |
   //  +----------------+------+------+      +                                 |
   //  |   Ptr[N..2]    | Last | Used |      |                                 |
   //  +----------------+------+------+------+---------------------------------+
   //  ^
   //  |
   //  '----------- Next() = Next & ~0x3 --------------------------------->
   //
   // The first block in a chain is denoted by a nullptr "prev" field, and the last
   // block is denoted by the "Last" bit being set.
   //
   // Note, This block class requires that the given block is aligned to a
   // alignof(Block*) boundary. Because of this alignment requirement, each
   // returned block will also be aligned to a alignof(Block*) boundary, and the
   // size will always be rounded up to a multiple of alignof(Block*).
   //
   // This class must be constructed using the static Init call.

The full text isn't relevant here so from now on let's just represent the
source code like this:

.. code-block:: none

   // The "Block" type is intended to ...
   //
   //   .------+---------------------------------.-----------------------------
   //   |            Block A (first)             |       Block B (second)
   //
   //   +------+------+--------------------------+------+------+---------------
   //   | Next | Prev |   usable space           | Next | Prev | usable space..
   //   +------+------+--------------------------+------+--+---+---------------
   //   ^  |                                     ^         |
   //   |  '-------------------------------------'         |
   //   |                                                  |
   //   '----------- Block B's prev points to Block A -----'
   //
   // One use for these blocks is ...
   //
   // Each block also contains flags for ...
   //
   //  .-----------------------------------------------------------------------.
   //  |                            Block                                      |
   //  +-----------------------------------------------------------------------+
   //  |              Next            | Prev |         usable space            |
   //  +----------------+------+------+      +                                 |
   //  |   Ptr[N..2]    | Last | Used |      |                                 |
   //  +----------------+------+------+------+---------------------------------+
   //  ^
   //  |
   //  '----------- Next() = Next & ~0x3 --------------------------------->
   //
   // The first block in a chain is ...
   //
   // Note, This block class requires ...
   //
   // This class must be ...

Arguably, this info should be in a concepts doc, not the reference, but long story
short I have thought it through and we are better off keeping it in the reference.

Let's convert this to the triple slash syntax so that Doxygen picks it up:

.. code-block:: none

   /// The "Block" type is intended to ...
   ///
   ///   .------+---------------------------------.-----------------------------
   ///   |            Block A (first)             |       Block B (second)
   ///
   ///   +------+------+--------------------------+------+------+---------------
   ///   | Next | Prev |   usable space           | Next | Prev | usable space..
   ///   +------+------+--------------------------+------+--+---+---------------
   ///   ^  |                                     ^         |
   ///   |  '-------------------------------------'         |
   ///   |                                                  |
   ///   '----------- Block B's prev points to Block A -----'
   ///
   /// One use for these blocks is ...
   ///
   /// Each block also contains flags for ...
   ///
   ///  .-----------------------------------------------------------------------.
   ///  |                            Block                                      |
   ///  +-----------------------------------------------------------------------+
   ///  |              Next            | Prev |         usable space            |
   ///  +----------------+------+------+      +                                 |
   ///  |   Ptr[N..2]    | Last | Used |      |                                 |
   ///  +----------------+------+------+------+---------------------------------+
   ///  ^
   ///  |
   ///  '----------- Next() = Next & ~0x3 --------------------------------->
   ///
   /// The first block in a chain is ...
   ///
   /// Note, This block class requires ...
   ///
   /// This class must be ...

How does that look?

.. image:: /_static/verbatim-wrangling-1.png
   :alt: The rendered page after the first attempt. The visual representation of the text diagram is completely wrong.

Absolutely terrible, that's how. But that's OK. I expected that. Wrapping the diagrams
in Doxygen's [verbatim] command should do the trick...

.. code-block:: none

   /// The "Block" type is intended to ...
   ///
   /// @verbatim
   ///   .------+---------------------------------.-----------------------------
   ///   |            Block A (first)             |       Block B (second)
   ///
   ///   +------+------+--------------------------+------+------+---------------
   ///   | Next | Prev |   usable space           | Next | Prev | usable space..
   ///   +------+------+--------------------------+------+--+---+---------------
   ///   ^  |                                     ^         |
   ///   |  '-------------------------------------'         |
   ///   |                                                  |
   ///   '----------- Block B's prev points to Block A -----'
   /// @endverbatim
   ///
   /// One use for these blocks is ...
   ///
   /// Each block also contains flags for ...
   ///
   /// @verbatim
   ///  .-----------------------------------------------------------------------.
   ///  |                            Block                                      |
   ///  +-----------------------------------------------------------------------+
   ///  |              Next            | Prev |         usable space            |
   ///  +----------------+------+------+      +                                 |
   ///  |   Ptr[N..2]    | Last | Used |      |                                 |
   ///  +----------------+------+------+------+---------------------------------+
   ///  ^
   ///  |
   ///  '----------- Next() = Next & ~0x3 --------------------------------->
   /// @endverbatim
   ///
   /// The first block in a chain is ...
   ///
   /// Note, This block class requires ...
   ///
   /// This class must be ...

Let's check how it looks...

.. image:: /_static/verbatim-wrangling-2.png
   :alt: The rendered page after the second attempt. The first diagram is mostly rendering correctly but the rest of the text and the second diagram is still completely wrong.

Uh-oh. I was expecting that to work. This might get hairy.

The `Handling Leading Slashes`_ section in the Breathe docs seems to be relevant
to my problem. Let's try Breathe's solution:

.. code-block:: none

   /// The "Block" type is intended to ...
   ///
   /// @verbatim embed:rst:leading-slashes
   ///   .------+---------------------------------.-----------------------------
   ///   |            Block A (first)             |       Block B (second)
   ///
   ///   +------+------+--------------------------+------+------+---------------
   ///   | Next | Prev |   usable space           | Next | Prev | usable space..
   ///   +------+------+--------------------------+------+--+---+---------------
   ///   ^  |                                     ^         |
   ///   |  '-------------------------------------'         |
   ///   |                                                  |
   ///   '----------- Block B's prev points to Block A -----'
   /// @endverbatim
   ///
   /// One use for these blocks is ...
   ///
   /// Each block also contains flags for ...
   ///
   /// @verbatim embed:rst:leading-slashes
   ///  .-----------------------------------------------------------------------.
   ///  |                            Block                                      |
   ///  +-----------------------------------------------------------------------+
   ///  |              Next            | Prev |         usable space            |
   ///  +----------------+------+------+      +                                 |
   ///  |   Ptr[N..2]    | Last | Used |      |                                 |
   ///  +----------------+------+------+------+---------------------------------+
   ///  ^
   ///  |
   ///  '----------- Next() = Next & ~0x3 --------------------------------->
   /// @endverbatim
   ///
   /// The first block in a chain is ...
   ///
   /// Note, This block class requires ...
   ///
   /// This class must be ...

The third try is the charm, right?

.. image:: /_static/verbatim-wrangling-3.png
   :alt: The rendered page after the third attempt. Everything is completely messed up, again.

WRONG. In the words of the great Bender Bending Rodriguez: we're boned.

In an act of pure desperation, let's try ChatGPT (GPT-4). I asked:

.. code-block:: none

   I have a plaintext diagram. verbatim is not working for me. What should I do?

(This was part of a longstanding conversation about Doxygen.)

ChatGPT replied:

.. code-block:: none

   Doxygen has another command for preserving the preformatted text blocks:
   @code{.unparsed} ... @endcode. This command will prevent Doxygen from parsing
   the text inside the block and will preserve whitespace.

``@code{.unparsed}``, huh? Weird. Looks gross. But at this point I've got nothing
to lose. Let's try it:

.. code-block:: none

   /// The "Block" type is intended to ...
   ///
   /// @code{.unparsed}
   ///   .------+---------------------------------.-----------------------------
   ///   |            Block A (first)             |       Block B (second)
   ///
   ///   +------+------+--------------------------+------+------+---------------
   ///   | Next | Prev |   usable space           | Next | Prev | usable space..
   ///   +------+------+--------------------------+------+--+---+---------------
   ///   ^  |                                     ^         |
   ///   |  '-------------------------------------'         |
   ///   |                                                  |
   ///   '----------- Block B's prev points to Block A -----'
   /// @endcode
   ///
   /// One use for these blocks is ...
   ///
   /// Each block also contains flags for ...
   ///
   /// @code{.unparsed}
   ///  .-----------------------------------------------------------------------.
   ///  |                            Block                                      |
   ///  +-----------------------------------------------------------------------+
   ///  |              Next            | Prev |         usable space            |
   ///  +----------------+------+------+      +                                 |
   ///  |   Ptr[N..2]    | Last | Used |      |                                 |
   ///  +----------------+------+------+------+---------------------------------+
   ///  ^
   ///  |
   ///  '----------- Next() = Next & ~0x3 --------------------------------->
   /// @endcode
   ///
   /// The first block in a chain is ...
   ///
   /// Note, This block class requires ...
   ///
   /// This class must be ...

Surely it won't work but we might as well check...

.. image:: /_static/verbatim-wrangling-4.png
   :alt: It worked! Everything is rendering correctly.

The LLMs strike again. It worked. This is why I keep telling my fellow technical
writers that we really need to wake up and realize that LLMs can be a very powerful
tool with the potential to offer a much faster and easier experience for our users.
I spent hours digging through the Doxygen and Breathe docs (and Google Search and
Stack Overflow) to find a solution, and nothing worked. The LLM showed me a working
solution that I had not encountered anywhere else on the first go.

Edit: During some discussion in the Write The Docs Slack, someone pointed out
that Doxygen has documented the ``code`` command and the documentation does mention
``@code{.unparsed}``. I didn't mean to give the wrong impression and imply that Doxygen
has not documented this functionality.
