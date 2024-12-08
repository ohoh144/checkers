from core.actions.action import Action
from core.enums.flags import Flag


class Burn(Action):
    require_flags = set(Flag.CAN_BURN)
