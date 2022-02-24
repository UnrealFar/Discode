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

.. autoclass :: Client
    :members:

Models
--------

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
