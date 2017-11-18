import curses
from curses.ascii import isdigit
import json
import nltk
from nltk.corpus import cmudict
from nltk.tokenize import word_tokenize

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

d = cmudict.dict()
d["forsooth"] = [u'FOR0',u'SOOTH2']
'''
"""
Count the number of sylables in a word.
Returns a list of integers with each integer the syllable
count for a certain pronunciation.
"""
def numSyls(word):   
    return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]

"""
Generate a list of rhymes for a given word.
"Level" is how good the rhymes should be. 
"""
def rhymeList(inp, level):
    entries = cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhymes += [word for word, pron in entries if pron[-level:] == syllable[-level:]]
    return set(rhymes)

"""
Check to see if two words rhyme
"""
def checkRhyme( word1, word2 ):
    # first, we don't want to report 'glue' and 'unglue' as rhyming words
    # those kind of rhymes are LAME
    if word1.find ( word2 ) == len(word1) - len ( word2 ):
        return False
    if word2.find ( word1 ) == len ( word2 ) - len ( word1 ): 
        return False
    return word1 in rhyme ( word2, 1 )
'''

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

"""
Convert a list of words to a list of tags
"""
def toTags(line):
    return [x[1] for x in nltk.pos_tag(line)]
