Contributors Guide
==================

Coding Style
------------

``PEP8`` is the coding style used in this project with one exception:
lines can be up to 100 characters long.
Please make sure to follow it.

Releasing
---------

Releases are published automatically when a tag is pushed to GitHub.

.. code-block:: bash

  # Set next version number
  export RELEASE=x.x.x
  export RELEASE=export RELEASE=$(python -c "import command_creator._info as _info; print(_info.__version__)")

  # Ensure committing everything (optional)
  git add -A

  # Create tags
  git commit --allow-empty -m "Release $RELEASE"
  git tag -a $RELEASE -m "Version $RELEASE"

  # Push
  git push --follow-tags
