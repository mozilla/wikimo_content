Wikimo Git documentation
=========================

This repository stores  documentation for https://wiki.mozilla.org/ and in particular the https://wiki.mozilla.org/Security pages.
It is possible to both pull existing pages, or changes in made to pages directly back to Git as well as commit changes to Git first then push them to the wiki. In any case, the Git repository has authority and for pages tracked here, it is highly recommended to ensure that your changes are sent via a pull-request.

Please do not change the main repository directly (i.e always fork and send a pull-request, get at least one peer-review and merge).

All documentation is licensed under the MPL (see LICENSE).

Usage
=====

.. note::

        Recommended: Install/use virtual envs, see
        https://www.insecure.ws/linux/python_venv_wrapper.html for example.

.. code::

        <activate your venv>
        $ pip install -r requirements.txt
        $ cp sync.json.inc sync.json
        <edit sync.json>
        $ ./sync.py

To sync new changes from git to wikimo:

.. code::

        $ ./sync.py --push

To sync the wiki to git (for ex when someone forgot to use git... ;-):

.. code::

        $ ./sync.py --get


To see a full unified diff of any change (when ran without get or push, this will only display changes but not commit
them):

.. code::

        $ ./sync.py --diff
