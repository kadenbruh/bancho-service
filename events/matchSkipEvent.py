from __future__ import annotations

from objects import match
from objects.osuToken import Token

from redlock import RedLock


def handle(userToken: Token, _):
    # Make sure we are in a match
    if userToken["match_id"] is None:
        return

    # Make sure the match exists
    multiplayer_match = match.get_match(userToken["match_id"])
    if multiplayer_match is None:
        return

    # Skip
    with RedLock(
        f"{match.make_key(userToken['match_id'])}:lock",
        retry_delay=50,
        retry_times=20,
    ):
        match.playerSkip(multiplayer_match["match_id"], userToken["user_id"])
