import uuid

class UUIDTools(object):

    def __init__(self,node,clockSeq):
        self.node = node
        self.clockSeq = clockSeq

    @staticmethod
    def generateUUID():
        return uuid.uuid1()


# print UUIDTools.generateUUID()