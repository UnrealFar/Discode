class GatewayEvent:
    r"""
    This class has all available gateway events, and information on how to register a listener for each of the events. An event maybe registered like this:

    .. code-block:: py

        @client.event(GatewayEvent.{EVENT_NAME})
        async def example_listener(*args, **kwargs):
            ...
    """

    DISPATCH = "dispatch"
    r"Dispatch is called whenever the websocket receives an event. Listeners waiting for dispatch must have 1 parameter- 'payload'"
    READY = "ready"
    r"Dispatched when the client is completely ready. Listeners waiting for this event must not have any parameters."
    GUILD_CREATE = "guild_create"
    r"Dispatched when the client joins a new guild, or the client receives data on a guild it is already in. This event takes 1 parameter- 'guild'"
    GUILD_UPDATE = "guild_update"
    r"Dispatched when a guild that the client is already in gets updated. This event takes two parameters- 'before' and 'after'"
    GUILD_DELETE = "guild_delete"
    r"Dispatched when the client gets removed from a guild, or the guild itself gets deleted by the owner. This event takes 1 parameter- 'guild'"
    MESSAGE_CREATE = "message_create"
    r"Dispatched when a user / bot sends a message. This event takes 1 parameter- 'message'"

class ButtonStyle:
    r"""Buttons come in a variety of styles to convey different types of actions. These styles also define what fields are valid for a button.

    .. image:: docs/media/button_styles.png

    """

    primary: int = 1
    secondary: int = 2
    success: int = 3
    danger: int = 4
    link: int = 5
    blurple: int = primary
    grey: int = secondary
    green: int = success
    red: int = danger
    url: int = link
