.. |.`~.replace_rst_images`| replace:: ``replace_rst_images()``
.. _.`~.replace_rst_images`: https://github.com/TDKorn/sphinx-readme/blob/master/sphinx_readme/parser.py#L191-L236
.. |.`~.read_rst`| replace:: ``read_rst()``
.. _.`~.read_rst`: https://github.com/TDKorn/sphinx-readme/blob/master/sphinx_readme/utils.py#L31-L56
.. |.`~.replace_autodoc_refs`| replace:: ``replace_autodoc_refs()``
.. _.`~.replace_autodoc_refs`: https://github.com/TDKorn/sphinx-readme/blob/master/sphinx_readme/parser.py#L278-L308
.. |attention| replace:: ⚠
.. |caution| replace:: ⚠
.. |danger| replace:: ☢
.. |error| replace:: ❌
.. |hint| replace:: 🧠
.. |important| replace:: ‼
.. |note| replace:: 📝
.. |tip| replace:: 💡
.. |warning| replace:: ❗
.. |default| replace:: ℹ
.. |client| replace:: 💻

..  Title: Sphinx README
..  Description: A Sphinx extension to generate reStructuredText files that render beautifully on platforms like GitHub, PyPi, and GitLab
..  Author: TDKorn (Adam Korn)


.. meta::
   :title: Sphinx README
   :description: A Sphinx extension to generate reStructuredText files that render beautifully on platforms like GitHub, PyPi, and GitLab
  
.. |RTD| replace:: **Explore the docs »**
.. _RTD: https://sphinx-readme.readthedocs.io/en/latest/


.. image:: docs/source/_static/logo.png
   :alt: Sphinx README: Generate reStructuredText files that render beautifully on platforms like GitHub, PyPi, and GitLab
   :align: center
   :width: 25%


Sphinx README
-----------------

Generate ``README.rst`` that renders beautifully on GitHub, PyPi, GitLab, etc.

|RTD|_


.. image:: https://img.shields.io/pypi/v/my-magento?color=eb5202
   :target: https://pypi.org/project/sphinx-readme/
   :alt: PyPI Version

.. image:: https://img.shields.io/badge/GitHub-my--magento-4f1abc
   :target: https://github.com/tdkorn/sphinx-readme
   :alt: GitHub Repository

.. image:: https://static.pepy.tech/personalized-badge/my-magento?period=total&units=none&left_color=grey&right_color=blue&left_text=Downloads
    :target: https://pepy.tech/project/my-magento

.. image:: https://readthedocs.org/projects/my-magento/badge/?version=latest
    :target: https://my-magento.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


About Sphinx README
~~~~~~~~~~~~~~~~~~~~~~~


.. csv-table::
   :header: |default| What's Sphinx README?

   "``sphinx_readme`` is a reStructuredText parser that uses Sphinx to generate ``rst`` files
   that render beautifully on platforms like GitHub, PyPi, and GitLab."

With ``sphinx_readme``, there's no need to rewrite your ``README.rst``
as a ``README.md`` file — parsed files have almost identical appearance and functionality as ``sphinx`` HTML builds,
including ``sphinx.ext.autodoc`` cross-references!

|

Features
=============

``sphinx_readme`` makes the following ``sphinx``/``docutils`` features functional:

* Autodoc cross-references
* Standard cross-references (ex. ``:doc:`` and ``:ref:``)
* Admonitions
* Image directives


Example
~~~~~~~~~~

.. image:: docs/source/_static/github_regular.png
   :width: 75%

|

.. image:: docs/source/_static/github_sphinx_readme.png
   :width: 75%

|

.. image:: docs/source/_static/pypi_sphinx_readme.png
   :width: 75%



Autodoc Cross-References
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. |replace_autodoc_refs| replace:: replace_autodoc_refs()
.. _replace_autodoc_refs: https://sphinx-readme.readthedocs.io/


Can link to source code or documentation stubs

Ex. |.`~.replace_autodoc_refs`|_ or |replace_autodoc_refs|_

Did you get the |.`~.read_rst`|_ method? Or was it the |.`~.replace_rst_images`|_ one?


Standard Cross-References
~~~~~~~~~~~~~~~~~~~~~~~~~~
The `The utils module <https://github.com/TDKorn/sphinx-readme/utils.html#utils>`_ module is helpful


Admonitions
~~~~~~~~~~~~~~~~~~~~~~~~~~
Admonitions are parsed to look the same as HTML admonitions

They can be parsed with the ``raw`` directive or ``csv-table`` directive

* GitHub supports the ``raw`` directive
* PyPi and GitLab must use the ``csv-table`` directive

Both generic and specific admonitions are supported


Generic Admonitions
=======================


.. csv-table::
   :header: |note| This is an admonition

   "Hello, this is a note admonition

   The admonition text is multiple lines long. If you |.`~.read_rst`|_ you will
   be able to read the ``rst`` files and convert them to **hot** versions

   .. admonition:: This is a nested admonition
      :class: warning

      Nested admonitions only work with the ``raw`` directive; please avoid them.

   This is back in the original admonition"


.. csv-table::
   :header: |client| The Client

   "This is an admonition with a custom class"


.. csv-table::
   :header: |default| Hello

   "This is an admonition with no class"

Specific Admonitions
=======================

Types: "attention", "caution", "danger", "error", "hint", "important", "note", "tip", "warning"



.. csv-table::
   :header: |attention| Attention

   "Attention!"


.. csv-table::
   :header: |caution| Caution

   "Caution!"


.. csv-table::
   :header: |danger| Danger

   "Danger!"


.. csv-table::
   :header: |error| Error

   "Error!"


.. csv-table::
   :header: |hint| Hint

   "Hint!"


.. csv-table::
   :header: |important| Important

   "Important!"


.. csv-table::
   :header: |note| Note

   "Note!"


.. csv-table::
   :header: |tip| Tip

   "Tip!"


.. csv-table::
   :header: |warning| Warning

   "Warning!"


.. csv-table::
   :header: |tip| Tip

   "This is a multi-line tip!

   Here's the second line."


.. csv-table::
   :header: |warning| Warning

   "This is a multi-line warning!
   There is no blank line before the second line!"


.. csv-table::
   :header: |note| Note

   "This is a note admonition, but it's on a separate line"


.. csv-table::
   :header: |attention| Attention

   "This is an attention admonition on a separate line,
   but there's no blank line before it!"


