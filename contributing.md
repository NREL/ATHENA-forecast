Contributing 
============

## Issue Tracking

New feature requests, changes, enhancements, non-methodology features, and bug reports can be filed as new issues in the
[Github.com issue tracker](https://github.com/NREL/ATHENA-twin/issues) at any time. Please be sure to fully describe the
issue.

## Repository

The ATHENA-twin repository is hosted on Github, and located here: http://github.com/NREL/ATHENA-twin

To work on a feature, please make a new feature branch based on the master branch. If you're working externally
to NREL, please fork OpenOA first and then create a feature branch in your own copy of the repository.
Work out of the feature branch before submitting a pull request. Be sure to periodically merge the target release
branch into your feature branch to avoid conflicts in the pull request.

When the feature branch is ready, make a pull request through the Github.com UI.

## Pull Request

Pull requests must be made for any changes to be merged into release branches.
They must include updated documentation and pass all unit tests and integration tests.
In addition, code coverage should not be negatively affected by the pull request.

## Coding Style

This code follows the PEP 8 style guide and uses the ``pycodestyle`` linter to check for compliance.
The only exception is the line length limit of 120 characters.

```
pylint --max-line-length=120 operational_analysis
```

## Documentation Style

Documentation is written using RST.


