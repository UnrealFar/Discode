
.. meta::
    :title: Discode Documentation || API Reference
    :type: website
    :url: https://discode.readthedocs.io/api.html
    :description: API Documentation for Discode
    :keywords: docs, discode, discord

.. currentmodule:: discode

API Reference
===============

The following section covers the API of Discode.

Version Related Info
----------------------
.. data:: __version__

    Returns the current release / version

Clients
---------------
These are the clients, that the library provides.

Client
~~~~~~~
The base client to use to connect to the api and receive events.

.. attributetable:: Client

.. autoclass :: Client
    :members:
    :undoc-members:
    :inherited-members:
    :exclude-members: on_event

    .. autodecorator:: discode.Client.on_event(event)

Event Reference
----------------

Discode allows users to listen for dispatch events received thru the gateway. All events must be registered in the following format:

.. code-block:: python

    @client.on_event(discode.GatewayEvent.READY)
    async def on_ready():
        print(client.user, "is ready"!)

See :class:`GatewayEvent` for more information on dispatch events.

.. autoclass:: GatewayEvent
    :members:
    :undoc-members:

Enumerations
-------------
This section describes in detail all the available enumerations Discode Provides.

{% for object in dir(discode.enums) %}
    {% set cls = getattr(discode.enums, object, None) %}
    {% set cls_name = getattr(cls, "__name__", "") %}

    {% if cls is callable and cls_name in allowed_enums %}

{{ cls_name }}
{{ "~" * cls_name|length() }}

.. autoclass:: discode.{{ cls_name }}
    :members:
    :undoc-members:

    {% endif %}
{% endfor %}

Utilities
---------
Discode provides a wide range of utilities for making developing Discord bots, and Discord related projects for developers. These are some of the documented utilities.

.. automodule:: discode.utils
    :members:
    :exclude-members: async_function, deprecated

.. autodecorator:: discode.utils.async_function

.. autodecorator:: discode.utils.deprecated

Models
------

{% for object in dir(discode.models) %}
   {% set cls = getattr(discode.models, object, None) %}
   {% set cls_name = getattr(cls, "__name__", "") %}

   {% if cls is callable and cls_name not in disallow %}
{{ cls_name }}
{{ "~" * cls_name|length() }}

.. warning::
    This class is not to be instanized manually.

.. attributetable:: discode.{{ cls_name }}

.. autoclass:: discode.{{ cls_name }}
    :members:
    :inherited-members:

   {% endif %}
{% endfor %}

Dataclasses
-----------

{% for object in dir(discode.dataclasses) %}
   {% set cls = getattr(discode.dataclasses, object, None) %}
   {% set cls_name = getattr(cls, "__name__", "") %}

   {% if cls is callable and cls_name not in disallow %}
{{ cls_name }}
{{ "~" * cls_name|length() }}

.. attributetable:: discode.{{ cls_name }}

.. autoclass:: discode.{{ cls_name }}
    :members:
    :inherited-members:

   {% endif %}
{% endfor %}

Sharding
--------

One of the useful features of sharding is that Discode provides it by default.

Shard Object
~~~~~~~~~~~~

.. autoclass:: discode.gateway.Shard
    :members:
    :undoc-members:
