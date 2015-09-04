Wikimo OpSec documentation
==========================

This repository stores all OpSec documentation for https://wiki.mozilla.org/Security/OpSec and related pages, except
for: https://wiki.mozilla.org/Security/Server_Side_TLS which is stored at https://github.com/mozilla/server-side-tls.

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
        <edit sync.jon!>
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
