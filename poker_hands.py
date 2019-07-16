from collections import defaultdict
import operator
import time

with open('/home/p-bpierson/notebooks/CSVs/p054_poker.txt') as file:
    data = [[card for card in row.split(' ')] for row in file.read().split('\n')]
data = data[0:-1] #drop last row if it's blank


def convert_value_to_num(value):
    '''
    value should be a string

    Converts T, J, Q, K, A to 10, 11, 12, 13, 14
    '''

    if value == 'T':
        return 10
    elif value == 'J':
        return 11
    elif value == 'Q':
        return 12
    elif value == 'K':
        return 13
    elif value == 'A':
        return 14
    else:
        return int(value)


def create_value_freq_dict(values):
    '''
    Pass in a list of string values for a
    hand and get back a dictionary with the
    frequency of each value
    '''

    d = defaultdict(int)
    for v in values:
        d[v] += 1
    return d


def hand_rank(hand):
    '''
    Given a hand (list of 5 cards as strings),
    returns a number 1-10 where 1 is a
    high card and 10 is a royal flush.

    Ex. hand = ['AS', 'KD', '3D', 'JD', '8H']

    Returns int between 1 and 10
    '''

    card_values = []
    card_suits = []

    for card in hand:
        card_values.append(card[0])
        card_suits.append(card[1])

    card_values_set = set(card_values)
    card_suits_set = set(card_suits)

    card_values_nums = [convert_value_to_num(value) for value in card_values]
    card_values_nums.sort()

    value_freq_dict = create_value_freq_dict(card_values)

    # royal flush - 10
    if card_values_set == {'T', 'J', 'Q', 'K', 'A'} and len(card_suits_set) == 1:
        return 10

    # straight flush - 9
    elif card_values_nums[-1] - card_values_nums[0] == 4 and len(card_suits_set) == 1:
        return 9

    # four of a kind - 8
    elif 4 in value_freq_dict.values():
        return 8

    # full house - 7
    elif 3 in value_freq_dict.values() and 2 in value_freq_dict.values():
        return 7

    # flush - 6
    elif len(card_suits_set) == 1:
        return 6

    # straight - 5
    elif card_values_nums[-1] - card_values_nums[0] == 4 and len(card_values_set) == 5:
        return 5

    # three of a kind - 4
    elif 3 in value_freq_dict.values():
        return 4

    # two pairs - 3
    elif len([c for c in value_freq_dict.values() if c == 2]) == 2:
        return 3

    # one pair - 2
    elif 2 in value_freq_dict.values():
        return 2

    # high card
    else:
        return 1


def high_card(hand, rank):
    '''
    Given a hand (list of 5 cards as strings)
    and the rank of the hand, returns a relevant
    list of high cards depending on the rank.

    Ex. hand = ['AS', 'KD', '3D', 'JD', '8H']

    Ex. royal flush high card is always A,
    two pair may come down to the value of the
    high pair or low pair, so would return both.

    Returns an integer for the high card or
    a list of high cards in order.
    '''

    card_values = []

    for card in hand:
        card_values.append(card[0])

    card_values_nums = [convert_value_to_num(value) for value in card_values]

    num_freq_dict = create_value_freq_dict(card_values_nums)

    # royal flush (no tiebreaker, does not occur in our 1000 hands)
    if rank == 10:
        return 0

    # straight flush, straight
    elif rank in [9,5]:
        return max(card_values_nums)

    # four of a kind, full house, three of a kind
    elif rank in [8,7,4]:
        return int(max(num_freq_dict.items(), key=operator.itemgetter(1))[0])

    # flush, high card
    elif rank in [6,1]:
        card_values_nums_desc = card_values_nums
        card_values_nums_desc.sort(reverse=True)
        return card_values_nums_desc

    # two pairs
    elif rank == 3:
        single_card = int(min(num_freq_dict.items(), key=operator.itemgetter(1))[0])
        list_of_pair_vals = [int(c) for c in num_freq_dict.keys() if int(c) != single_card]
        list_of_pair_vals.sort(reverse=True)
        list_of_pair_vals.append(single_card)
        return list_of_pair_vals

    # one pair
    elif rank == 2:
        single_pair_card = int(max(num_freq_dict.items(), key=operator.itemgetter(1))[0])
        list_of_high_cards = [single_pair_card]
        list_of_solos = [int(c) for c in num_freq_dict.keys() if int(c) != single_pair_card]
        list_of_solos.sort(reverse=True)
        list_of_high_cards += list_of_solos
        return list_of_high_cards


def evaluate_games(data):
    '''
    Run through N rows of data
    '''
    
    time_start = time.clock()
    p1w = 0
    p2w = 0
    for hand in data:
        p1h = hand[:5]
        p1r = hand_rank(p1h)
        p1hc = high_card(p1h, p1r)

        p2h = hand[5:]
        p2r = hand_rank(p2h)
        p2hc = high_card(p2h, p2r)

        if p1r > p2r:
            p1w += 1
        elif p1r < p2r:
            p2w += 1
        else:
            if type(p1hc) == int:
                if p1hc > p2hc:
                    p1w += 1
                elif p1hc < p2hc:
                    p2w += 1
            else:
                for n in range(0,len(p1hc)):
                    if p1hc[n] > p2hc[n]:
                        p1w += 1
                        break
                    elif p1hc[n] < p2hc[n]:
                        p2w += 1
                        break

    if p1w + p2w != 1000:
        print('Something horrible happened')

    print('P1 wins:', p1w, ' P2 wins:', p2w)
    time_elapsed = (time.clock() - time_start)
    print('Solution took',int(round(time_elapsed*1000,0)),'ms')


evaluate_games(data)
