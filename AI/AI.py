import json
import sqlite3
from typing import Union

import numpy

from AI.Song import Song

def get_db_connection():
    conn=sqlite3.connect('database.db')
    conn.row_factory=sqlite3.Row
    return conn

def voteBass(bassVal):
    prob = makeFreqTable("bass")[bassVal]
    if prob >= .5:
        return True
    else:
        return False


def voteFeat(featVal):
    prob = makeFreqTable("feat")[featVal]
    if prob >= .5:
        return True
    else:
        return False


def voteVocal(vocalVal):
    prob = makeFreqTable("vocal")[vocalVal]
    if prob >= .5:
        return True
    else:
        return False


def voteInstrument(instrumentVal):
    prob = makeFreqTable("instrument")[instrumentVal]
    if prob >= .5:
        return True
    else:
        return False


def voteOriginality(originalityVal):
    prob = makeFreqTable("originality")[originalityVal]
    if prob >= .5:
        return True
    else:
        return False


def main(song: Song):
    print(song.bass)
    bassVote = voteBass(song.bass)
    featVote = voteFeat(song.feat)
    vocalVote = voteVocal(song.vocal)
    instrumentVote = voteInstrument(song.instrument)
    originalityVote = voteOriginality(song.originality)
    voteList = [bassVote, featVote, vocalVote, instrumentVote, originalityVote]
    voteCount = voteList.count(True)
    if voteCount >= 3:
        return True
    else:
        return False


def makeFreqTable(param: str):
    # TODO: make it read from json so that you just have to input a parameter and it reads training data to make list for you
    conn=get_db_connection()
    rows=conn.execute('SELECT * FROM songs').fetchall()
    list=[Song(i['name'],i['bass'],i['feat'],i['vocal'],i['instrument'],i['originality'],i['isBop']) for i in rows]
    paramArray = []
    for song in list:
        paramArray.extend([song.__getattribute__(param)])
    numpyInput = numpy.array(paramArray)
    uniqueValList = numpy.unique(numpyInput)
    freqTable = {}
    for val in uniqueValList:
        bopNum = 0
        totalNum = 0
        for song in list:
            if song.__getattribute__(param) == val:
                totalNum += 1
                if song.isBop:
                    bopNum += 1
        freqTable[val] = bopNum / totalNum
    return freqTable
