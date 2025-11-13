Coding Guidelines
=================

The lines should not exceed 120 characters.

Test comments
-------------

Each new test must have a short (1-3 sentences) description of the goal of the test. It should
be added as a sphinx docstring triple quote comment after the test function signature. Try to convey the
purpose of the test (why you felt it was important enough to dedicate time to write it) rather than
simply state what it does. Many tests don't have a description. We can address this problem
incrementally. If you edit an existing test that is missing a description, you should add it.

There are several formats of docstring and we decided to use `sphinx` variant. See
[Forge!219](https://gitlab.isc.org/isc-projects/forge/-/merge_requests/219#note_257686) for details.
Many modern editors support this syntax out of the box.

We also use [Python type hints](https://docs.python.org/3/library/typing.html).
If using more advanced types than primitives (str, bool, int, etc.), it may be necessary to do
`from typing import Tuple,Sequence,Literal` (or whatever type you're using).

An example comment looks like this:

```python
def test_some_function(class_cmd: str, dhcp6: bool) -> Tuple[int, str]:
    """This test checks if the specified API calls can handle negative (missing mandatory parameters,
       garbage, no parameters) scenarios.

    :param class_cmd: specific API command to be tested
    :param dhcp6: defines if DHCPv4 (false) or DHCPv6 (true) should be tested
    :return: a tuple with status code and error message (if status is non-zero)
    """
```

In _Visual Studio Code_, you can install _Python Docstring Generator_ extension that will generate
the template for you. Make sure you edit in the preferences (`autoDocstring.docstringFormat` set to
`sphinx`). The template will be generated for you as soon as you start typing `"""`.

In _PyCharm_, go to `Settings` => `Tools` => `Python integrated tools` => `Docstrings` and change
the format to `reStructuredText`. The template will be filled as soon as you type `"""` and press
Enter.

For _Emacs_, there is `sphinx-doc` package that adds minor mode that can be easily installed as
package from [MELPA](https://www.emacswiki.org/emacs/MELPA). After installing, enable `sphinx-doc-mode`,
then use `C-c M-d` to insert the comments. You may want to check the
[github docs](https://github.com/naiquevin/sphinx-doc.el).

pylint
------

The long term goal is to use pylint everywhere. However, we have a huge legacy code that didn't adhere
to pylint. When adding new code, make sure there are no new pylint warnings reported and the overall
score is not lower. Do not clutter your MRs that have substantial code changes with pylint fixes.
If you want to, open dedicated MRs for that, but please do that in moderation. This is a rabbit hole
that can easily suck a lot of time.

To check the code with pylint and other linters, use `lint.sh` script.

Changelog
---------

We do have a changelog. Please document changes that may be useful for others, such as adding new
tests, fixing problems in existing ones, refactoring functions that will be used by others etc.
Smaller changes (e.g. "I did fifth round of minor tweaks to something") should be skipped.

Writing new tests
-----------------

Since forge moved from lettuce to pytest, writing new tests is just python programming.
Functions available in `src/srv_control.py` are used to operate remote DHCP/DNS servers.
Functions available in `src/srv_msg.py` are used to generate and parse traffic. Don't forget
to write test description for new tests.

Additional info
---------------

- [Pytest homepage](https://docs.pytest.org/en/latest/)
- [Scapy homepage](http://www.secdev.org/projects/scapy/)
