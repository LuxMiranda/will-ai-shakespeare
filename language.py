import curses
from curses.ascii import isdigit
import nltk
from nltk.corpus import cmudict


d = cmudict.dict()

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

"""
Check to see if a list of words follows iambic pentameter
"""
def isIP(stanza):
    sylCount = 0;
    for word in stanza:
        sylCount = sylCount + numSyls(word)[0]
    return (sylCount == 10)
        
