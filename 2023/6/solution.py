from functools import cmp_to_key
import numpy as np

with open('input.txt') as f:
    raw_data = [tuple(x.strip('\n').split(" ")) for x in f.readlines()]

cards = 'AKQJT98765432'

def get_hand_type(hand):
    card_counts = {a: hand.count(a) for a in set(hand)}
    if np.max(list(card_counts.values())) == 5:
        return 6
    elif np.max(list(card_counts.values())) == 4:
        return 5
    elif (3 in card_counts.values()) and (2 in card_counts.values()):
        return 4
    elif np.max(list(card_counts.values())) == 3:
        return 3
    elif list(card_counts.values()).count(2) == 2:
        return 2
    elif np.max(list(card_counts.values())) == 2:
        return 1
    else:
        return 0

def compare_hands(a, b):
    if get_hand_type(a[0]) > get_hand_type(b[0]):
        return 1
    elif get_hand_type(a[0]) < get_hand_type(b[0]):
        return -1
    else:
        for (c, d) in zip(a[0], b[0]):
            if cards.index(c) < cards.index(d):
                return 1
            elif cards.index(d) < cards.index(c):
                return -1
        return 0

sorted_hands = sorted(raw_data, key=cmp_to_key(compare_hands))
sorted_bids = [int(x) for x in list(zip(*sorted_hands))[1]]
ranks = [x+1 for x in range(len(sorted_bids))]
print(f"Solution a: {np.sum(np.array(ranks) * np.array(sorted_bids))}")