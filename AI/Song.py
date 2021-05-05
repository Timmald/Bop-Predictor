# TODO: make the class, with constructor and json serialize method(probably __dict__)
# name, bass,feat, vocal,instrument,originality,isBop
class Song:
    def __init__(self, name: str, bass: int, feat: bool, vocal: int, instrument: str, originality: int, isBop=None):
        assert 1 <= bass <= 5
        assert 1 <= vocal <= 5
        #assert 1 <= originality <= 5
        self.name = name
        self.bass = bass
        self.feat = feat
        self.vocal = vocal
        self.instrument = instrument
        self.originality = originality
        self.isBop = isBop

    def jsonSerialize(self):
        return {"name": self.name,
                "bass": self.bass,
                "feat": self.feat,
                "vocal": self.vocal,
                "instrument": self.instrument,
                "originality": self.originality,
                "isBop": self.isBop
                }

    @staticmethod
    def fromDict(dict):
        return Song(dict["name"], dict["bass"], dict["feat"], dict["vocal"], dict["instrument"], dict["originality"],
                    dict["isBop"])
