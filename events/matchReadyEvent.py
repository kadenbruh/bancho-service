from __future__ import annotations

from objects import match
from objects.osuToken import Token

from redlock import RedLock

def handle(userToken: Token, _):
    if userToken["match_id"] is None:
        return

    multiplayer_match = match.get_match(userToken["match_id"])
    if multiplayer_match is None:
        return

    with RedLock(
        f"{match.make_key(userToken['match_id'])}:lock",
        retry_delay=50,
        retry_times=20,
    ):
        # Get our slotID and change ready status
        slot_id = match.getUserSlotID(multiplayer_match["match_id"], userToken["user_id"])
        if slot_id is not None:
            match.toggleSlotReady(multiplayer_match["match_id"], slot_id)

        # If this is a tournament match, we should send the current status of ready
        # players.
        if multiplayer_match["is_tourney"]:
            match.sendReadyStatus(multiplayer_match["match_id"])
