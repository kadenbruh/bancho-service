from common.ripple import userUtils
from constants import clientPackets
from objects.osuToken import token


def handle(userToken: token, rawPacketData: bytes):  # Friend add packet
    userUtils.addFriend(
        userToken.userID, clientPackets.addRemoveFriend(rawPacketData)["friendID"]
    )
