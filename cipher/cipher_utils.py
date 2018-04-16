import sys
import os.path
import re
from random import shuffle

DECK_ORDERING = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUIT_ORDERING = ["c", "d", "h", "s"]
CARDS_IN_DECK = 52
KEY_LENGTH = 108
ORDERED_DECK = "Ac2c3c4c5c6c7c8c9c10cJcQcKcAd2d3d4d5d6d7d8d9d10dJdQdKdAh2h3h4h5h6h7h8h9h10hJhQhKhAs2s3s4s5s6s7s8s9s10sJsQsKs"

# Private methods
# ---------------

def __parse_key(raw_key):
	index = 0
	cards_counted = 0
	key = []
	while cards_counted < CARDS_IN_DECK:
		for i in range(index, len(raw_key)):
			if raw_key[i] in SUIT_ORDERING:
				key.append(raw_key[index:(i + 1)])
				cards_counted += 1
				index = (i + 1)
				break
	return key

# assumes that incoming message only consists of lowercase letters
def __shift(message, key):
	shifted = ""

	index = 0
	for char in message:
		card_shift_value = DECK_ORDERING.index(key[index][0 : len(key[index]) - 1]) + 1

		shifted += chr(((ord(char) - ord('a') + card_shift_value) % 26) + ord('a'))
		index += 1

	return shifted

def __order(message, key):
	reordering = []

	for suit in SUIT_ORDERING:
		for val in DECK_ORDERING:
			place = val + suit
			if key.index(place) < len(message):
				reordering.append(message[key.index(place)])

	return ''.join(reordering)


# base method for enciphering message less than length of key
def __encipher_base(message, key):
	# two phases: shifting each character, and re-ordering them
	shifted = __shift(message, key)
	reordered = __order(shifted, key)
	return reordered

def __unshift(ciphertext, key):
	unshifted = ""

	index = 0
	for char in ciphertext:
		card_shift_value = DECK_ORDERING.index(key[index][0 : len(key[index]) - 1]) + 1

		unshifted += chr(((ord(char) - ord('a') - card_shift_value) % 26) + ord('a'))
		index += 1

	return unshifted

def __order_cards(cards):
	ordering = []

	for suit in SUIT_ORDERING:
		for val in DECK_ORDERING:
			if (val + suit) in cards:
				ordering.append(val + suit)

	return ordering

def __unorder(ciphertext, key):
	unordering = []
	key_ordering = __order_cards(key[0:len(ciphertext)])

	index = 0
	for card in key:
		if index < len(ciphertext):
			encipherment_position = key_ordering.index(card)
			unordering.append(ciphertext[encipherment_position])
			index += 1

	return ''.join(unordering)

def __decipher_base(ciphertext, key):
	# two plases: re-order the ciphertext in the order of the key, de-shift by the value of the key
	reordered = __unorder(ciphertext, key)
	unshifted = __unshift(reordered, key)
	return unshifted


# Public methods
# --------------

def generate_random_key():
	deck = []
	for val in DECK_ORDERING:
		for suit in SUIT_ORDERING:
			deck.append(val + suit)
	shuffle(deck)

	return ''.join(deck)

def encipher(message, key):
	key = __parse_key(key)
	ciphertext = ""

	# break the message up into 52 character chunks, and encode each. Then put them together at end
	for i in range(0, len(message), CARDS_IN_DECK):
		if len(message) - i >= CARDS_IN_DECK:
			chunk_end = i + CARDS_IN_DECK
		else:
			chunk_end = len(message)

		ciphertext += __encipher_base(message[i:chunk_end], key)

	return ciphertext

def decipher(ciphertext, key):
	key = __parse_key(key)
	# reorder the ciphertext to be in the order of the key
	# de-shift the ciphertext by the key to go back to plain
	plaintext = ""

	# break the message up into 52 character chunks, and decode each
	for i in range(0, len(ciphertext), CARDS_IN_DECK):
		if len(ciphertext) - i >= CARDS_IN_DECK:
			chunk_end = i + CARDS_IN_DECK
		else:
			chunk_end = len(ciphertext)

		plaintext += __decipher_base(ciphertext[i:chunk_end], key)

	return plaintext

def is_valid_key(key):
	if len(key) != KEY_LENGTH:
		return False

	return ''.join(__order_cards(__parse_key(key))) == ORDERED_DECK
