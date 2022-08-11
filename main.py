import random

import prosodic as p
import csv

from pyrhyme import rhyming_list

from parody.generation.ParodyGenerator import generate_parody

from genius_client.genius import fetch_lyrics

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

original_lyrics = ""

with open("input.txt", 'r') as input_file:
    lines = input_file.readlines()
    for line in lines:
        original_lyrics += line

# TODO: Remove metadata e.g. singer name from genius version of lyrics
original_lyrics = fetch_lyrics("Hey Jude", "the beatles")

parody = generate_parody(original_lyrics)

output_file = open("output.txt", "a")
output_file.truncate(0)

for line in parody:
    output_file.write(line)
    output_file.write("\n")

output_file.close()
