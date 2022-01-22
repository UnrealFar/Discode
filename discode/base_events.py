from .message import Message

async def on_ready():
    """
    The on_ready event is called when the client successfully connects to the gateway and is completely ready.
    """
    pass

async def on_message(message: Message):
    """The on_message event is called when the client connects to the gateway. A minimum and maxiumum of one parameter may be passed.

    Parameters
    ----------
    message: :class:`Message`
    """
    print(message.author, "has sent", message.content)
