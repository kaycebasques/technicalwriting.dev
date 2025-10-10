.. _gn:

==========================================================
Automating code deletion with Gemini (and a little Python)
==========================================================

.. _Gemini 2.0 Flash: https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-0-flash

Today I used `Gemini 2.0 Flash`_ and a little Python to automate the process of
removing code from over 200 GN build files. Here's how it went.

----------
Background
----------

.. _migrated pigweed.dev: https://pigweed.dev/docs/blog/08-bazel-docgen.html

Back in Q1 2025 we `migrated pigweed.dev`_ from GN to Bazel. I.e. previously we
built the site with GN and now we build it with Bazel. We kept the old GN build
around in case some unforeseen issues with the Bazel build came up and we
needed to quickly revert to the "known good" GN build. Fast forward to today,
no such issues have popped up. The Bazel build has been running smoothly in
production for a few months now. Keeping the old GN docs build is slowing down
Pigweed contributors, because they have to keep both the GN and Bazel docs
builds happy. It's time to turndown the GN build.

The actual process of turning down the GN docs build is fairly simple. I just
needed to remove the documentation generation (docgen) features from all of the
``BUILD.gn`` files. It's easy to detect the existence of docgen features; you
just search for a few certain keywords (e.g. ``pw_docgen`` or ``pw_doc_group``)
within each ``BUILD.gn`` file's contents. It's probably feasible to automate
this through regex-based automation but I wanted to find out if Gemini could
handle this task. Also, if this approach works, there are lots of other
problems that aren't reducible to regex automation where this approach may come
in handy.

--------
Approach
--------

My general approach was to:

* Grab all source files in the repo.
* Filter out everything except the ``BUILD.gn`` files.
* Filter out the ``BUILD.gn`` files that do not use the
  docgen features.
* Use Gemini to remove the docgen features from each ``BUILD.gn``
  file, one-by-one. I.e. one Gemini API invocation for each file.

.. _Meggin Kearney: https://www.linkedin.com/in/meggin-kearney-553b3373

My former boss `Meggin Kearney`_ calls this the hybrid approach to GenAI.
For some tasks, such as listing out all files and determining relevant
files, you're sometimes better off just using "classical automation" e.g.
a Python script. Only use GenAI for the things that can't be handled by
classical automation.

Implementation
==============

#. Create and activate a virtual environment in the root directory
   of the repository:

   .. code-block:: console

      python3 -m venv venv
      . venv/bin/activate.fish

#. Install the Gemini Python library:

   .. code-block:: console

      python3 -m pip install google-genai

#. Save the following script as ``edit.py``:

   .. code-block:: py

      from json import dump, load
      from os import environ, walk
      from pathlib import Path
      from subprocess import run
      from typing import Dict

      from google.genai import Client


      def _is_ignored(root: Path, target: Path, ignored: list[Path]) -> bool:
          """Check if Git is ignoring the path."""
          # Ignore Git's directory itself.
          if str(target).lower().endswith(".git"):
              return True
          # Check if this path matches something in ``.gitignore``.
          command = ["git", "-C", str(root), "check-ignore", str(target)]
          result = run(command, capture_output=True, text=True)
          return str(target) in result.stdout


      def _is_in_ignored_dir(target: Path, ignored: list[Path]):
          """Check if this path is in an ignored directory."""
          for maybe_parent_dir in ignored:
              if str(maybe_parent_dir) in str(target):
                  return True
          return False


      def collect_paths(root: Path) -> list[Path]:
          """Collect all paths in the repository."""
          paths: list[Path] = []
          ignored: list[Path] = []
          for current_working_dir, _, files in walk(root):
              cwd = Path(current_working_dir)
              if _is_in_ignored_dir(cwd, ignored):
                  continue
              if _is_ignored(Path(root), cwd, ignored):
                  ignored.append(cwd)
                  continue
              for file in files:
                  path = cwd / Path(file)
                  if _is_ignored(Path(root), path, ignored):
                      ignored.append(path)
                      continue
                  paths.append(path)
          return paths


      def _is_gn_build_file(path: Path) -> bool:
          """Check if the path is a GN build file."""
          return str(path).endswith("BUILD.gn")


      def _uses_docgen(path: Path) -> bool:
          """Check if the GN build file has any of the docgen keywords."""
          with open(path, "r") as f:
              content = f.read()
          keywords = ["pw_docgen", "pw_doc_group", "pw_size_diff", "pw_doc_gen"]
          for keyword in keywords:
              if keyword in content:
                  return True
          return False


      def filter_paths(root: Path, paths: list[Path]) -> list[Path]:
          targets = []
          for path in paths:
              if not _is_gn_build_file(path):
                  continue
              if not _uses_docgen(path):
                  continue
              targets.append(path)
          return targets


      def _remove_backticks(edits: str) -> str:
          """Remove the backticks that Gemini adds at the start and end of the output."""
          lines = edits.splitlines()
          if lines[0].startswith("```"):
              lines.pop(0)
          last = len(lines) - 1
          if lines[last].startswith("```"):
              lines.pop(last)
          return "\n".join(lines)


      def remove_docgen_code(prompt: str, target: Path, gemini: Client) -> None:
          print(f"[info] Editing {str(target)}")
          with open(target, "r") as f:
              src = f.read()
          contents = prompt + src
          response = gemini.models.generate_content(
              model="gemini-2.0-flash",
              contents=contents,
          )
          if response.text is None:
              return
          edits = _remove_backticks(response.text)
          with open(target, "w") as f:
              f.write(edits)


      def main():
          root = Path(".")
          paths = collect_paths(root)
          targets = filter_paths(root, paths)
          print(f"[info] {len(targets)} files will be edited")
          with open("prompt.md", "r") as f:
              prompt = f.read()
          gemini = Client(api_key=environ["GEMINI_API_KEY"])
          for target in targets:
              remove_docgen_code(prompt, target, gemini)


      if __name__ == "__main__":
          main()

   (This script assumes that ``git`` is a globally available command.)

#. Save the instructions as ``prompt.md``:

   .. code-block:: md

      # GN DOCS BUILD TURNDOWN

      ## BACKGROUND

      Previously we built our docs with GN. Now, we build them with Bazel.
      We no longer need the GN document generation (docgen) features.

      ## GOAL

      Your task is to remove the GN docgen features from the GN file that
      I provide you. You must not modify any other lines in the GN files.
      You must output the edited GN file with no explanation. The keywords
      `docs`, `pw_docgen`, `pw_doc_group`, `pw_size_diff`, and `pw_doc_gen`
      indicate docgen features that need to be removed.

      ## EXAMPLE

      When provided a file like this:

      ```
      # Copyright 2024 The Pigweed Authors
      #
      # Licensed under the Apache License, Version 2.0 (the "License"); you may not
      # use this file except in compliance with the License. You may obtain a copy of
      # the License at
      #
      #     https://www.apache.org/licenses/LICENSE-2.0
      #
      # Unless required by applicable law or agreed to in writing, software
      # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      # License for the specific language governing permissions and limitations under
      # the License.
      import("//build_overrides/pigweed.gni")
      import("$dir_pw_docgen/docs.gni")
      import("$dir_pw_unit_test/test.gni")
      import("$dir_pw_build/target_types.gni")
      import("$dir_pw_unit_test/test.gni")

      config("public_include_path") {
        include_dirs = [ "public" ]
        visibility = [ ":*" ]
      }

      pw_source_set("my_library") {
        public = [ "public/my_library/foo.h" ]
        deps = [":an", ":unsorted", ":list"]
        public_configs = [ ":public_include_path",
        ]
      }

      pw_doc_group("docs") { sources = [ "docs.rst" ] }

      pw_test_group("tests") {
      }
      ```

      You should modify the file like this:

      ```
      # Copyright 2024 The Pigweed Authors
      #
      # Licensed under the Apache License, Version 2.0 (the "License"); you may not
      # use this file except in compliance with the License. You may obtain a copy of
      # the License at
      #
      #     https://www.apache.org/licenses/LICENSE-2.0
      #
      # Unless required by applicable law or agreed to in writing, software
      # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      # License for the specific language governing permissions and limitations under
      # the License.
      import("//build_overrides/pigweed.gni")
      import("$dir_pw_unit_test/test.gni")
      import("$dir_pw_build/target_types.gni")
      import("$dir_pw_unit_test/test.gni")

      config("public_include_path") {
        include_dirs = [ "public" ]
        visibility = [ ":*" ]
      }

      pw_source_set("my_library") {
        public = [ "public/my_library/foo.h" ]
        deps = [":an", ":unsorted", ":list"]
        public_configs = [ ":public_include_path",
        ]
      }

      pw_test_group("tests") {
      }
      ```

      ## INSTRUCTIONS

      Remove the GN docgen features from the following file. Remember that
      the keywords `docs`, `pw_docgen`, `pw_doc_group`, `pw_size_diff`, and
      `pw_doc_gen` represent the docgen features that should be deleted.
      You must output the edited GN file completely, without explanation.

   (In the Python script, the source code of a single ``BUILD.gn`` file
   is appended after these instructions.)

#. Run the script:

   .. code-block:: console

      python3 edit.py

-------
Results
-------

235 files were modified. Perhaps most miraculously, the build continued
to work after all of Gemini's removals, modulo a couple minor issues.

Here's the change: `https://pwrev.dev/286672 <https://pwrev.dev/286672>`_

Cost
====

I think my total Gemini API costs were between $30-40. I'm not sure at the
moment because Google Cloud seems to be having issues around not displaying
billing costs in realtime.

If I had been more careful with making sure the script worked completely before
ever invoking the Gemini API, I think the cost would have been between $10-20.
As I was developing the script, I would let Gemini run on a bunch of files and
then realize that something was wrong and would have to start all over again.

Time
====

The script took 20 minutes to run. There are some obvious ways to add more
parallelism, but I was already running into quota limit issues. It was simpler
for me to keep the script single-threaded, processing only one file at a time.

.. _Automation: https://xkcd.com/1319/

It took me about a day to get the setup working completely.
Right now, it feels a bit like I fell in xkcd's `Automation`_
trap. But if I am able to successfully adapt this setup for other
tasks with minimal further customization, then I do think I will
start to see some significant time savings.

Reviewing all 235 modified files took another 30 or 40 minutes.

Accuracy
========

Gemini 2.0 Flash was very good at only removing the code that I told
it to remove and leaving the rest untouched. I only saw one generation
error, where Gemini left off a quotation mark:

.. code-block:: text

   "extendhfsf2.c",
   extendsfdf2.c",

Extra backticks
---------------

Due to how the prompt is structured, Gemini assumed that it should start and
end its response with triple backtick characters. Writing a little
Python to remove the extra backticks was easier than coaxing Gemini to stop
doing this.

Going beyond the instructions
-----------------------------

In some of the files, Gemini went beyond the instructions that I gave it
by removing ``pw_size_diff`` code. This was interesting, because Gemini
was technically correct to remove this code. ``pw_size_diff`` is basically
a docgen feature. But I did not tell Gemini to remove this code. In this case,
it worked OK. In a team meeting we decided that the ``pw_size_diff`` code
should be removed. (I subsequently added ``pw_size_diff`` to the list of docgen
keywords to look for.) But in other situations it may be a problem if Gemini
does not follow my instructions closely.

There was one (and only one!) case where two extra dependencies were added
to a rule that creates a C++ library. I'm not sure why it happened only once
in the 235 files that were edited. Pretty weird and disconcerting.

Following the instructions too closely
--------------------------------------

In other cases, Gemini followed my instructions too closely. E.g. there was
an ``if`` block like this:

.. code-block:: py

   # We depend on emboss, so we can only compute size when emboss is in the build.
   if (dir_pw_third_party_emboss != "") {
     pw_size_diff("use_passthrough_proxy_size_report") {
       title = "pw_bluetooth_proxy Passthrough Size Report"
       base = "$dir_pw_bloat:bloat_base"
       binaries = [
         {
           target = "size_report:use_passthrough_proxy"
           label = "Create and use proxy as a simple passthrough"
         },
       ]
     }
   } else {
     pw_size_diff("use_passthrough_proxy_size_report") {
       title = "pw_bluetooth_proxy Passthrough Size Report"
       base = "$dir_pw_bloat:bloat_base"
       binaries = [
         {
           target = "$dir_pw_bloat:bloat_base"
           label = "Emboss not configured."
         },
       ]
     }
   }

Gemini correctly deleted the ``pw_size_diff`` code but left behind a now
empty and useless ``if`` block:

.. code-block:: py

   # We depend on emboss, so we can only compute size when emboss is in the build.
   if (dir_pw_third_party_emboss != "") {
   } else {
   }

Newline munging
---------------

A lot of newlines at the end of files got messed up. This was not a big
deal because Pigweed has a utility (``pw format``) for enforcing consistent
newline style at the end of all files. If we didn't have ``pw format`` this
would have been very annoying to fix.
