import random


def chance(percentage):
    roll = random.randint(0, 100)
    return roll <= percentage
