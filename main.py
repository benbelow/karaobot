import random

import prosodic as p
import csv

words = []

with open("data/english-word-list-total.csv", 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile, delimiter=';')

    # extracting field names through first row
    fields = next(csvreader)

    # extracting each data row one by one
    for row in csvreader:
        words.append(row[1])

stressedWords = [{"word": word, "stress": p.Word(word).stress} for word in words]

text = p.Text("I never want to hear you say. I want it that way.")

stresses = text.children[0].children[0].str_stress()

targetStresses = stresses


def is_valid_stress(w):
    return targetStresses.startswith(w["stress"])

parodyLine = []

while len(targetStresses) != 0:
    validWords = [w for w in stressedWords if is_valid_stress(w)]
    chosen = random.choice(validWords)
    parodyLine.append(chosen["word"])
    stressLength = len(chosen["stress"])
    targetStresses = targetStresses[stressLength:]

print(parodyLine)
