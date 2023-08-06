========
idem-gcp
========

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-idem-teal
   :alt: Made with idem, a Python implementation of Plugin Oriented Programming
   :target: https://www.idemproject.io/

.. image:: https://img.shields.io/badge/docs%20on-docs.idemproject.io-blue
   :alt: Documentation is published with Sphinx on docs.idemproject.io
   :target: https://docs.idemproject.io/idem-gcp/en/latest/index.html

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

GCP Cloud Provider for Idem.

About
=====

``idem-gcp`` helps manage GCP with ``idem``.

* `idem-gcp source code <https://gitlab.com/vmware/idem/idem-gcp>`__
* `idem-gcp documentation <https://docs.idemproject.io/idem-gcp/en/latest/index.html>`__

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

What is Idem?
-------------

This project is built with `idem <https://www.idemproject.io/>`__, an idempotent,
imperatively executed, declarative programming language written in Python. This project extends
idem!

For more information:

* `Idem Project Website <https://www.idemproject.io/>`__
* `Idem Project docs portal <https://docs.idemproject.io/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.8+
* git *(if installing from source, or contributing to the project)*

Installation
------------

.. note::

   If wanting to contribute to the project, and setup your local development
   environment, see the ``CONTRIBUTING.rst`` document in the source repository
   for this project.

If wanting to use ``idem-gcp``, you can do so by either
installing from PyPI or from source.

Install from PyPI
+++++++++++++++++

.. code-block:: bash

  pip install idem-gcp

Install from source
+++++++++++++++++++

Clone the `idem_gcp` repository.

.. code:: bash

    git clone git@gitlab.com:vmware/idem/idem-gcp.git
    cd idem_gcp

Create a virtual environment, and then activate it:

.. code:: bash

    python3 -m venv venv
    source venv/bin/activate

Install idem-gcp and other base requirements:

.. code:: bash

    pip3 install -e .
    pip3 install -r requirements/base.txt


Install the following packages in order to run the tests:

.. code:: bash

    pip3 install -r requirements/py3.10/tests.txt

**NOTE:**  Change py3.10 if needed with your  Python version. There is support for py3.8, py3.9, py3.10 and py3.11.

Setup
=====

After installation GCP Idem Provider execution and state modules will be accessible to the pop `hub`.
In order to use them we need to set up our credentials.

Create a new file called `credentials.yaml` and populate it with your credential profiles.

To provide your GCP credentials in the file, use the "gcp" provider key.
Under that key, add different profiles as needed.
A profile specifies authentication parameters for GCP.
The `default` profile will be automatically used by `idem`,
but the other ones could be explicitly specified for each run or SLS file.
This is done through the `--acct-profile` `idem` cli flag or the
`acct_profile` SLS property.

There is currently one GCP authentication mechanism supported by idem-gcp -
providing service account keys.
The following example gives the overall structure of the authentication
parameters' expected format.

credentials.yaml

..  code:: sls

    gcp:
      default:
        type: service_account
        project_id: “<project>”
        private_key_id: “<key_id>”
        private_key: |
          -----BEGIN PRIVATE KEY-----
          <private_key>
          ——END PRIVATE KEY-----
        client_email: “<service_account_email>“
        client_id: “<client_id>”
        auth_uri: https://accounts.google.com/o/oauth2/auth
        token_uri: https://oauth2.googleapis.com/token
        auth_provider_x509_cert_url: https://www.googleapis.com/oauth2/v1/certs
        client_x509_cert_url: “<certificate_url>“
        universe_domain: googleapis.com
      <other_profile_name>:
        ...

The values of these parameters can be obtained through the GCP console after creating a service account and generating a service account key in JSON format.
Be sure to assign appropriate roles for the service account, such that it has the rights to access and manage the needed resources.
For a better security posture, follow the principal of least privilege and do not use service accounts with excessive rights.
For more information on the authentication parameters used, refer to the `Credentials <https://google-auth.readthedocs.io/en/master/reference/google.oauth2.service_account.html#google.oauth2.service_account.Credentials>`_ docs.

Encrypt the created credentials file:


.. code:: bash

    acct encrypt credentials.yaml


The output of this command is the ACCT_KEY which needs to be securely stored.
A `credentials.yaml.fernet` encrypted file is also created in the working directory, whose path should be used as ACCT_FILE.
These could be given to idem either through environment variables or directly as `idem` run parameters.

Setting environment variables
-----------------------------

.. code:: bash

    export ACCT_KEY="<ACCT_KEY>"
    export ACCT_FILE=$PWD/credentials.yaml.fernet

Providing acct parameters to the idem run
-----------------------------------------

.. code:: bash

    idem <subcommand> --acct-key "<ACCT_KEY>" --acct-file "$PWD/credentials.yaml.fernet" --acct-profile "<profile_name>"

Specifying account profile in SLS files
---------------------------------------

.. code:: sls

    ensure_resource:
      gcp.<service>.<resource>.present:
        - acct_profile: <profile_name>
        - name: resource_name
        - kwarg1: val1


For more information on the Idem ACCT authentication management subsystem, refer to the following resources:

* `Account credentials file doc <https://docs.idemproject.io/idem/en/latest/topics/tutorials/acct_file.html>`_
* `Multiple Account Management <https://docs.idemproject.io/idem/en/latest/topics/tutorials/acct.html>`_
* `ACCT advanced features <https://docs.idemproject.io/idem/en/latest/topics/sls_acct.html>`_
