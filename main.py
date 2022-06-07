import random

import prosodic as p
import csv

from pyrhyme import rhyming_list

words = []

# Overall design plan:

# Parse input lyrics
# (stretch goal) identify repeated phrases and ensure that we (a) make them funny somehow (b) repeat them in our parody
# (stretch goal) semantic consistency (this sounds v. hard!)
# choose appropriate places to rhyme with original
    # (stretch goal) - identify rhyming scheme and enforce parity
    # end of lines is a good MVP
    # maybe randomly pick a few other good rhyme places throughout (long words in particular)
# for each line, make a correctly-stressed alternative
    # mostly maintain original word lengths with some variations
    # high weighting towards long (3+ syllable) words remaining same length
    # introduce fallback logic for greedy algorithm - don't dig into un-finishable hole
    # maybe reverse algorithm to work from end of line tbh, as the rhyming will be there and therefore more constrained. We'll alwways be able to add some arbitrary syllables to the start of a line.
    # (v0) no language consideration
    # (v1) basic grammatical encoding to attempt to make sentences make some sense
    # (v2) markov chains?
    # (v3) full on machine learning (very stretch goal!)
# work out how to integrate with a karaoke program (e.g. Karafun)
# have fun karaoke night 😎


# TODO: This code is hideous, clean it up plz.

with open("data/english-word-list-total.csv", 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter=';')

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        words.append(row[1])

stressedWords = [{"word": word, "stress": p.Word(word).stress} for word in words]

# TODO: Handle punctuation properly so as not to confuse rhyme logic
text = p.Text("I never want to hear you say. I want it that way")

# TODO: Keep track of the original words, don't just extract stresses out of context - it would be nice to weight towards one to one mapping, though we shouldn't *ONLY* do one to one.
stresses = text.children[0].children[0].str_stress()

targetStresses = stresses


def is_valid_stress(w):
    return targetStresses.startswith(w["stress"])

parodyLine = []

while len(targetStresses) != 0:
    validWords = [w for w in stressedWords if is_valid_stress(w)]
    chosen = random.choice(validWords)
    stressLength = len(chosen["stress"])

    # hacky way of making last word rhyme
    if len(targetStresses) - stressLength == 0:
        toRhyme = text.children[0].children[0].children[-1].token
        # TODO: This is calling an API under the hood, so it's quite the bottleneck. Try: (i) evaluate all the rhymes we want up-front (ii) Fetch them in parallel (iii) Check that the API's ok with the rate
        rawRhymes = rhyming_list(toRhyme, lang="en")
        # perfect rhymes only for now - TODO: Fallback to half rhymes.
        # TODO: Weight towards more common words for rhymes
        rhymingWords = [w for w in rawRhymes if w.score == 300]
        stressedRhymingWords = [{"word": w2.word, "stress": p.Word(w2.word).stress} for w2 in rhymingWords]
        validRhymingWords = [w for w in stressedRhymingWords if is_valid_stress(w)]
        chosen = random.choice(validRhymingWords)

    parodyLine.append(chosen["word"])
    targetStresses = targetStresses[stressLength:]


print(parodyLine)
