.. currentmodule:: discode

API Reference
===============

The following section covers the API of DisCode.

Version Related Info
----------------------

.. data:: version_info

    A named tuple that gives detailed info on the current version.

.. data:: __version__

    Returns the current release / version

Clients
---------------
These are the clients, that the library provides.

Client
~~~~~~

.. autoclass:: Client
    :members:


Event Reference
-----------------
This section covers Discord gateway events and custom DisCode events. You can register an event liestener by using :meth:`Client.on_event`

Example:

.. code-block:: python

    @client.on_event("ready")
    async def ready_event():
       print(client.user, "is ready!")

Discord Objects
----------------
Discord Objects are objects, that the library provides you with to use. Some common examples of these are :class:`Message`, :class:`Channel`, etc. These classes are not to be initialised by users, except for a few, for example :class:`Embed` and :class:`Intents`. All the classes that are not supposed to be initialised by users are marked with a warning sign.

Message Object
~~~~~~~~~~~~~~

.. warning::
    This class should not be initialised by users.

.. autoclass:: Message
    :members:

Embed Object
~~~~~~~~~~~~~~

.. autoclass:: Embed
    :members:
