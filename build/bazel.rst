.. _bazel:

==============================
Migrating pigweed.dev to Bazel
==============================

I have been tasked with the fascinating and somewhat-overwhelming
project of migrating pigweed.dev's build system from GN to Bazel.
These are my notes on the project.

.. _bazel-20240924:

---------------
Tue Sep 24 2024
---------------

I wrote a design doc today summarizing the project and plan. Here's the
gist.

.. _Sphinx: https://www.sphinx-doc.org/en/master/

pigweed.dev is powered by `Sphinx`_. Sphinx expects your docs to be structured
under a root directory, like this:

.. code-block:: text

   .
   ├── a
   │   └── a.rst
   ├── b
   │   └── b.rst
   ├── c
   │   └── c.rst
   ├── conf.py
   └── index.rst

The directory containing ``conf.py`` and ``index.rst`` is the root directory.
``a/a.rst``, ``b/b.rst``, and ``c/c.rst`` are easy to integrate into the
Sphinx system because they're all in subdirectories relative to the root
directory.

pigweed.dev on the other hand is structured like this:

.. code-block:: text

   .
   ├── a
   │   └── a.rst
   ├── b
   │   └── b.rst
   ├── c
   │   └── c.rst
   └── docs
       ├── conf.py
       └── index.rst

Some of our docs are in sibling directories relative to the root directory.
Sphinx doesn't like this.

Our GN build system mainly just gathers up all the documentation-related
files that are spread across the Pigweed repo and packages them up into the
directory structure that Sphinx expects. Then we just ``cd`` into that new
directory and run Sphinx normally. This is the main functionality that I need
to recreate in Bazel.

.. _rules_python/sphinxdocs: https://github.com/bazelbuild/rules_python/tree/main/sphinxdocs

We're going to use `rules_python/sphinxdocs`_ as the foundation of our
Bazel-based build system. At first glance it seems to provide everything we
need.

.. _Sphinx Extensions: https://www.sphinx-doc.org/en/master/usage/extensions/index.html

The main challenge of this project is that pigweed.dev is a fairly big docs
site and it's not easy to migrate to Bazel incrementally. For example,
Sphinx has a wonderful cross-reference feature that guarantees that all internal
links are correct. If you try to link to a doc that doesn't exist, Sphinx treats
this as an error and stops the build. There's probably a way to downgrade this
particular error to just a warning where Sphinx complains about the problem
but continues building the site. My main point is that there are lots of things
like this that make incremental migration difficult.

.. _bazel-20240927:

---------------
Fri Sep 24 2027
---------------

Dependency Hell
===============

.. figure:: https://sourcegraphstatic.com/blog/nine-circles-of-dependency-hell.jpg

   Credit: `The Nine Circles of Dependency Hell <https://sourcegraph.com/blog/nine-circles-of-dependency-hell>`_

Yesterday I made an unexpected visit to `Dependency Hell <https://en.wikipedia.org/wiki/Dependency_hell>`_.

`rules_python/sphinxdocs`_ is going to be the foundation of our Bazel-based build
system. The Sphinx features in rules_python that I need are brand new. They were introduced
in the last release, v0.36.0. Upgrading the Pigweed repo to v0.36.0 was a simple
one-line change. But then all (dependency) hell broke loose. ``sphinx_build.py``
(the script in rules_python that starts the Sphinx build process) started having
fatal errors around unexpected arguments. Eventually I figured out that
rules_python v0.36.0 was developed against Sphinx v8, whereas we're on Sphinx v7. So I tried updating
the Pigweed repo to use Sphinx v8 and eventually hit a wall. Some of the Sphinx
Extensions that we use in turn have dependencies on other PyPI libraries, and
those dependencies don't support Sphinx v8 yet. Luckily I figured out that I
could just upgrade the Pigweed repo to the last v7 version that was released.
We were on Sphinx v7.1.2 (released over a year ago); I updated us to Sphinx
v7.4.7 (released two months ago). This unblocked me from using rules_python
v0.36.0 within the Pigweed repo.

Once rules_python v0.36.0 started working I hit another snag:

.. code-block:: text

   kayce@kayce0 ~/p/pigweed (pw_docgen)> bazelisk build //pw_docgen/...
   WARNING: Option 'remote_default_platform_properties' is deprecated: --remote_default_platform_properties has been deprecated in favor of --remote_default_exec_properties.
   WARNING: Option 'remote_default_platform_properties' is deprecated: --remote_default_platform_properties has been deprecated in favor of --remote_default_exec_properties.
   ERROR: /home/kayce/.cache/bazel/_bazel_kayce/9659373b1552c281136de1c8eeb3080d/external/rules_python++pip+python_packages/sphinx/BUILD.bazel:10:6: in alias rule @@rules_python++pip+python_packages//sphinx:pkg: cycle in dependency graph:
       //pw_docgen:_docs_html (8bf5217cd2199c4037e0ca161ab823102dd08eb93eeb7d4325e1d09666f3d863)
       //pw_docgen:_docs_html (2ccb10a0925868f764725cd74e410c636f5bbc18edb2d446d5c2ff1eb85e7e25)
       //pw_docgen:docs (2ccb10a0925868f764725cd74e410c636f5bbc18edb2d446d5c2ff1eb85e7e25)
       //pw_docgen:sphinx-build (bef2812dd1082aa39f3bcaa89343101b37ad5ee2cf77f8448d2ef909b33c5108)
       @@rules_python++pip+python_packages//pydata_sphinx_theme:pydata_sphinx_theme (bef2812dd1082aa39f3bcaa89343101b37ad5ee2cf77f8448d2ef909b33c5108)
       @@rules_python++pip+python_packages//pydata_sphinx_theme:pkg (bef2812dd1082aa39f3bcaa89343101b37ad5ee2cf77f8448d2ef909b33c5108)
       @@rules_python++pip+python_packages_311_pydata_sphinx_theme//:pkg (bef2812dd1082aa39f3bcaa89343101b37ad5ee2cf77f8448d2ef909b33c5108)
   .-> @@rules_python++pip+python_packages//sphinx:pkg (bef2812dd1082aa39f3bcaa89343101b37ad5ee2cf77f8448d2ef909b33c5108)
   |   @@rules_python++pip+python_packages_311_sphinx//:pkg (bef2812dd1082aa39f3bcaa89343101b37ad5ee2cf77f8448d2ef909b33c5108)
   |   @@rules_python++pip+python_packages//sphinxcontrib_serializinghtml:pkg (bef2812dd1082aa39f3bcaa89343101b37ad5ee2cf77f8448d2ef909b33c5108)
   |   @@rules_python++pip+python_packages_311_sphinxcontrib_serializinghtml//:pkg (bef2812dd1082aa39f3bcaa89343101b37ad5ee2cf77f8448d2ef909b33c5108)
   `-- @@rules_python++pip+python_packages//sphinx:pkg (bef2812dd1082aa39f3bcaa89343101b37ad5ee2cf77f8448d2ef909b33c5108)
   Target //pw_docgen:_docs/_sources up-to-date:
     bazel-bin/pw_docgen/_docs/_sources/pw_docgen/conf.py
     bazel-bin/pw_docgen/_docs/_sources/pw_docgen/index.rst
   ERROR: Analysis of target '//pw_docgen:_docs_html' failed; build aborted
   INFO: Elapsed time: 0.124s, Critical Path: 0.01s
   INFO: 1 process: 1 internal.
   ERROR: Build did NOT complete successfully

This problem was beyond my pay grade so I asked my resident Bazel expert, Ted
Pudlik, for help. Ted pointed me to this issue:
`Circular dependencies between Sphinx and sphinxcontrib-* <https://github.com/sphinx-doc/sphinx/issues/11567>`_

And the rules_python docs on 
`circular dependencies <https://rules-python.readthedocs.io/en/latest/pypi-dependencies.html#circular-dependencies>`_.

The fixes here were also pretty easy. I mainly just needed to upgrade
``sphinxcontrib-serializinghtml`` to v1.1.10 to eliminate the circular
dependency. And then I had to bump the minor revisions on ``babel`` and
``pygments``.

After that, my unexpected tour of Dependency Hell was finished
(for now?) and I was able to proceed with my prototyping. Phew.

.. _bazel-20240930:

---------------
Mon Sep 30 2027
---------------

We have a custom Sphinx extension that pulls in data from a file in
a faraway directory. E.g. the script is at
``//pw_docgen/py/py_docgen/sphinx/modules_index.py`` and it needs data
from ``//docs/module_metadata.json``. In the GN build it's easy to access
the data file from ``modules_index.py``:

.. code-block:: py

   with open(f'{os.environ["PW_ROOT"]}/docs/module_metadata.json', 'r') as f:

``PW_ROOT`` gives you the absolute path to the Pigweed repo. Bazel on the
other hand uses `sandboxing <https://bazel.build/docs/sandboxing>`_ so you
can't access absolute paths like this. Well, maybe it's not related to
sandboxing; I'm not sure about those details. All I know is that the
simple approach that works in GN doesn't work in our Bazel system.

The Bazel solution is also not too bad, but I definitely would not have
figured it out without Ted's help again. You just add the data files to the
``data`` list in your ``py_library`` rule and depend on
`bazel-runfiles <https://github.com/bazelbuild/rules_python/tree/main/python/runfiles>`_:

.. code-block::

   py_library(
       # ...
       data = [
           "//:PIGWEED_MODULES",
           "//docs:module_metadata.json",
       ],
       # ...
       deps = [
           "@rules_python//python/runfiles",
       ],
   )

And then you tweak your Python script so that it changes the path
to the data files depending on whether the script is getting
executed from a Bazel build or a GN build:

.. code-block::

   try:  # Bazel location for the data
       from python.runfiles import runfiles  # type: ignore
       r = runfiles.Create()
       modules_file = r.Rlocation('pigweed/PIGWEED_MODULES')
       r = runfiles.Create()
       metadata_file = r.Rlocation('pigweed/docs/module_metadata.json')
   except ImportError:  # GN location for the data
       modules_file = f'{os.environ["PW_ROOT"]}/PIGWEED_MODULES'
       metadata_file = f'{os.environ["PW_ROOT"]}/docs/module_metadata.json'
   with open(modules_file, 'r') as f:
       # The complete, authoritative list of modules.
       complete_pigweed_modules_list = f.read().splitlines()
   with open(metadata_file, 'r') as f:
       # Module metadata such as supported languages and status.
       metadata = json.load(f)
