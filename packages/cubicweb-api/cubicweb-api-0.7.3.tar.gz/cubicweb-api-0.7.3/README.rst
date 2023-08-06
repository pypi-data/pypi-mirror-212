Summary
================

.. Useful links
.. _RQLController cube: https://forge.extranet.logilab.fr/cubicweb/cubes/rqlcontroller
.. _CubicWebJS: https://forge.extranet.logilab.fr/cubicweb/cubicwebjs
.. _React Admin CubicWeb: https://forge.extranet.logilab.fr/cubicweb/react-admin
.. _OpenAPI: https://www.openapis.org
.. _JWT: https://jwt.io

This cube exposes the new api, replacing the `RQLController cube`_ with a simpler architecture.
We plan on integrating this new API directly into CubicWeb, without having to rely on this cube.

You can use the `CubicWebJS`_ client to communicate with this API in JavaScript.
See the project `React Admin CubicWeb`_ for an example on how to use `CubicWebJS`_.


**⚠️ Please note this cube will later be integrated into CubicWeb.
The installation instructions only applies for the API cube while it lives in its own repository.**

Setup
-----

Install this cube with pip by running:

``pip install cubicweb_api``

Then open the ``__pkginfo__.py`` of your CubicWeb instance
and add ``cubicweb-api`` in the ``__depends__`` dictionary.

The last step is to upgrade your instance by the following command
(replacing ``<YOUR_INSTANCE>`` with your instance name):

``cubicweb-ctl upgrade <YOUR_INSTANCE>``

The command will ask you to edit the ``all-in-one.conf`` file.
Accept the changes to write the default configuration options available for this cube.

Configuration options
~~~~~~~~~~~~~~~~~~~~~

There are 2 configuration options for this cube available in ``all-in-one.conf``:

* ``api-path-prefix``

Prefix used for the url path.The api version number will be added after this prefix (only v1 for now).

* ``api-server-name``

The base url to use for openapi validation. Set this to the CubicWeb base url if openapi cannot find the server.

Available Routes
----------------

This cube uses the `OpenAPI`_ specification to describe and validate data.
The complete specification is available in `openapi_template.yaml <cubicweb_api/openapi/openapi_template.yaml>`_,
but here is a short recap of all the available routes:

* ``/schema``

Returns this instance's Schema

* ``/rql``

Executes the given RQL query

* ``/login``

Tries to log in the user

* ``/transaction/<ACTION>``

Manages transactions. Replace ``<ACTION>`` with ``begin``, ``execute``, ``commit`` or ``rollback``.

The real path will depend on your configuration. When using the default configuration,
if your instance lives in ``https://example.com``, then the routes will live in ``https://example.com/api/v1/``.

Authentication
--------------

When sending valid credentials to the login route,
a `JWT`_ token will be generated and sent in the ``Set-Cookie`` header.
This token must be sent as a cookie for each request to be successful.

