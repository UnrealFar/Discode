from typing import Optional

class InteractionData:
    __slots__ = [
        "custom_id",
        "component_type"
    ]
    def __init__(self, payload: dict):
        payload: dict = payload

        self.custom_id: int = int(payload.pop("id", int()))
        self.component_type: int = int(payload.pop("component_type"),)


class Interaction:
    r"""Represents a gateway interaction.
    """
    def __init__(
        self,
        interaction_id: Optional[int],
        application_id: Optional[int],
        interaction_type: int,
        data: dict
    ):
        self.id: int = int(interaction_id)
        self.application_id: int = int(application_id)
        self.type = interaction_type
        self.data = data


