import curses
from curses.ascii import isdigit
import json
import nltk
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize
import random
from random import randint
import math

d = cmudict.dict()
d["forsooth"] = [u'FOR0',u'SOOTH2']
tagDict = {}

"""
Load and parse sonnets from a file and return the structure
@param {string} file_name The file location (complete path)
@return {dictionary[]}
"""
def load_sonnets(file_name):
    sonnets = None
    with open(file_name, "r") as sonnetFile:
        sonnets = json.load(sonnetFile)

        def get_tags_from_sonnet(sonnet):
            return map(lambda line: nltk.pos_tag(word_tokenize(line)), sonnet)

        def add_tags_to_sonnet(sonnet_info):
            sonnet_info["tags"] = get_tags_from_sonnet(sonnet_info["sonnet"])
            return sonnet_info

        return map(add_tags_to_sonnet, sonnets)


sonnets = load_sonnets("./sonnets.json")

"""
Return the rank of a CMUdict word part.
Returns -1 if the word part does not have a rank
"""
def toRank(part):
    if part[-1].isdigit():
        return int(part[-1])
    return -1
    
"""
Convert a word into a list of syllable stress ranks
"""
def wordToSylRanks(word):
    return [toRank(part) for part in (d[word.lower()][0]) if toRank(part) != -1]

"""
Convert a list of words into a monolithic list of syllable stress ranks
"""
def stanzaToSylRanks(stanza):
    ranks = []
    for word in stanza:
        ranks = ranks + wordToSylRanks(word)
    return ranks

"""
Check to see if a list of words follows iambic pentameter
"""
def isIP(stanza):
    ranks = stanzaToSylRanks(stanza)
    if len(ranks) != 10:
        return False
    for r in [ranks[i] for i in [1,3,5,7,9]]:
        if r <= 0:
            return False
    return True
        

def buildTagDict(sonnets):
    #gets a sonnet line
    for sonnet in sonnets:
        for taglist in sonnet["tags"]:
            addTagsToDict(taglist)
        
#assuming one line and its tag list is passed as arrays
def addTagsToDict(tagList):
    for word,tag in tagList:
        word = word.lower()
        if tagList == {}:
            tagList[tag] = word
        elif tag in tagDict:
            if tagDict[tag] is None:
                tagDict[tag] = [word]
            elif word not in tagDict[tag]:
                tagDict[tag].append(word)
        else:
            tagDict[tag] = [word]


def replaceWordTags(tags):
    #Assuming each word in words is an nltk tag as a string. ie. ['UU','WC','CC']
    newLine = []
    for tag in tags:
        replacement = random.choice(tagDict[tag])
        newLine.append(replacement)
    return newLine

"""
Convert a list of words to a list of tags
"""
def toTags(line):
    return [x[1] for x in nltk.pos_tag(line)]

"""
Grab a random sonnet's tag set from the .json
"""
def getRandSonnetTags():
    return sonnets[randint(0, len(sonnets) - 1)]["tags"]

"""
Grab a random line from a sonnet
"""
def getRandSonnetLine(sonnet):
    return sonnet[randint(0, len(sonnet) - 1)]

"""
Generate a random sonnet structure of word tags
"""
def makeRandomSonnetStructure():
    sonnetStruct = []

    # For the first 13 lines, pick a random line from a random sonnet
    for i in range(0,13):
        randSonnet = getRandSonnetTags()
        randLine = getRandSonnetLine(randSonnet)
        sonnetStruct.append([x[1] for x in randLine])
    
    # For the last line, choose the last line from a random sonnet
    lastSonnet = getRandSonnetTags()
    sonnetStruct.append([x[1] for x in lastSonnet[-1]])
            
    return sonnetStruct

"""
Takes a list of words and punctuation and returns a nicely formatted English sentence
"""
def wordListToSentence(wordList):
    sentence = ""
    for i in range(0,len(wordList) - 1):
        sentence = sentence + wordList[i]
        if wordList[i+1] not in [',','.','?','\'',':',';']:
            sentence = sentence + " "
    sentence = sentence + wordList[-1]
    return sentence


