#!/usr/bin/env python3

import sys
import collections
import functools
import operator

import requests

r = requests.get("https://arkhamdb.com/api/public/cards/")
cards = r.json()


def getDeck(deckID):
    r = requests.get(f"https://arkhamdb.com/api/public/deck/{deckID}.json")
    print(r.text)
    return r.json()


def getAllDecks(deckIDs):
    for deckID in deckIDs:
        nextDeck = deckID
        d = None
        while d is None or d["next_deck"] is not None:
            d = getDeck(nextDeck)
            nextDeck = d["next_deck"]
        yield d


def resolveCard(cardID):
    return [card['name'] for card in cards if card['code'] == cardID][0]


# deckIDs = sys.argv[1:]
# deckIDs = ['496803', '499642', '526251']
deckIDs = ['493723', '479501', '489153', '493047']
decks = list(getAllDecks(deckIDs))

cardCounts = dict(functools.reduce(
    operator.add, map(collections.Counter, [deck['slots'] for deck in decks])))

print("Cards > 2:")
print({resolveCard(k): v for k, v in cardCounts.items() if v > 2})
