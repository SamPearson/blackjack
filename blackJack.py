#!/usr/bin/python

import random


class StackOfCards(object):
    def __init__(self):
        self.contents = []

    def shuffle(self):
        random.shuffle(self.contents)


class BlackjackHand(StackOfCards):
    def __init__(self):
        self.contents = []
        self.ace_value = 11
        self.bust = False

    def draw_card(self, draw_from):
        transfer_card(draw_from, self, 0, 1)

    def point_value(self):
        self.points = 0
        for card in range(0, len(self.contents)):
            if self.contents[card] in ["K", "Q", "J"]:
                self.points += 10
            elif self.contents[card] == 'A':
                self.points += self.ace_value
            else:
                self.points += self.contents[card]

        if "A" in self.contents and self.points > 21 and self.ace_value == 11:
            self.ace_value = 1
            return self.point_value()
        return self.points

    def show_hand(self):
        pass


def transfer_card(fromStack, toStack, cardKey, transfers):
    #removes target card from one stack and puts it onto another stack
    # I need to do a safety check here:
    for i in range(0, transfers):
        toStack.contents.insert(0, fromStack.contents.pop(cardKey))

def draw_hands():
    deck.contents = []
    player_hand.contents = []
    dealer_hand.contents = []
    for x in range(2, 11):
        for i in range(0, 4):
            deck.contents.append(x)

    for card in ["J", "Q", "K", "A"]:
        for i in range(0, 4):
            deck.contents.append(card)

    deck.shuffle()
    # empty both dealer and player hands here
    transfer_card(deck, dealer_hand, 0, 2)
    transfer_card(deck, player_hand, 0, 2)

def display_game_state():
    print "\nThe dealer is showing " + str(dealer_hand.contents[0])
    print "You're holding " + str(player_hand.point_value()) + ": " + ", ".join(str(x) for x in player_hand.contents)

def request_input():
    while True:
        display_game_state()
        print "\nYou may enter:"
        print "Hit"
        print "Hold"
        print "Quit"
        player_input = raw_input("\nEnter an action: ")
        player_input = player_input.lower()

        if player_input in ["hit", "hold", "quit"]:
            player_action = player_input
            return player_action
        else:
            print "\n I'm sorry, I didn't understand that"

def take_dealers_turn():
    while dealer_hand.point_value() < 17:
        dealer_hand.draw_card(deck)
        if dealer_hand.point_value() > 21:
            dealer_hand.bust = True

def display_game_outcome(player_outcome):
    print "You held " + str(player_hand.point_value())
    print "The dealer held " + str(dealer_hand.point_value())
    if player_outcome == "win":
        print "\n***********"
        print "* You Win!*"
        print "***********"
    if player_outcome == "lose":
        print "\n***************"
        print "* You Lost :c *"
        print "***************"


# begin init sequence
dealer_hand = BlackjackHand()
player_hand = BlackjackHand()
deck = StackOfCards()

while True:
    draw_hands()
    dealer_hand.bust = False
    player_hand.bust = False

    player_action = request_input()
    if player_action == "quit":
        break

    while player_action == "hit":
        player_hand.draw_card(deck)
        print "\nYou drew: " + str(player_hand.contents[0])
        if player_hand.point_value() > 21:
            player_hand.bust = True
            display_game_outcome("lose")
            break
        player_action = request_input()
    if player_action == "quit":
        break

    if player_action == "hold":
        take_dealers_turn()
        if dealer_hand.bust == True or dealer_hand.point_value() < player_hand.point_value():
            display_game_outcome("win")
        else:
            display_game_outcome("lose")
