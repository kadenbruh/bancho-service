from __future__ import annotations

from common.redis import generalPubSubHandler
from common.ripple import userUtils
from objects import osuToken
from objects import tokenList


class handler(generalPubSubHandler.generalPubSubHandler):
    def __init__(self):
        super().__init__()
        self.type = "int"

    def handle(self, userID):
        if (userID := super().parseData(userID)) is None:
            return

        userID = int(userID)

        userUtils.removeFirstPlaces(userID)

        if not (targetToken := tokenList.getTokenFromUserID(userID)):
            return

        targetToken["privileges"] = userUtils.getPrivileges(userID)
        osuToken.checkBanned(targetToken["token_id"])
        osuToken.checkRestricted(targetToken["token_id"])
