"""
Created on Fri Jul  5 18:42:09 2019

Author: Andrej
"""

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight',
         'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
          'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    def __init__(self):      #Naredi seznam kart po vrsti
        self.deck = []
        for rank in ranks:
            for suit in suits:
                self.deck.append(Card(suit,rank))

    def __str__(self):      #Prikaže seznam
        deck_full = ''
        for card in self.deck:
            deck_full += '\n' + card.__str__()
        return 'Deck: ' + deck_full

    def shuffle(self):      #Naključno premeša karte
        random.shuffle(self.deck)
        print('Deck shuffled.')

    def deal_player(self):      #Spremenljivka z zadnjo karto iz seznama (jo odstrani)
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):      #Doda card v seznam trenutnih kart v roki in določi vrednost
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Budget:
    def __init__(self):
        self.balance = 100
        self.bet = 0

    def loss(self):
        self.balance -= self.bet

    def win(self):
        self.balance += self.bet

def bet(budget):
    while True:
        try:
            budget.bet = int(input('You have {budget} chips. Place your bet: '.format(budget=budget.balance)))
        except ValueError:
            print('Your bet must be a number')
        else:
            if budget.bet > budget.balance:
                print('Your bet exceeds your budget, bet lower amount.', budget.balance)
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal_player())
    hand.adjust_ace

def hit_or_stand(deck,hand):
    global playing
    while True:
        h_s = input("Do you want to hit or stand? Type 'h' or 's'.")
        if h_s.lower() == 'h':
            hit(deck,hand)
        elif h_s.lower() == 's':
            print('Player stands. Dealer is now playing')
            playing = False
        else:
            print('Type again...')
            continue
        break

def show_some(player,dealer):
    print("\nDealer's hand:")
    print("<hidden>")
    print("",dealer.cards[1])
    print("\nPlayer's hand:")
    print("",*player.cards, sep='\n')

def show_all(player,dealer):
    print("\nDealer has: ", *dealer.cards, sep = '\n')
    print("Dealer's value = ",dealer.value)
    print("\nPlayer has: ", *player.cards, sep = '\n')
    print("Player's value = ",player.value)

def player_busts(player,dealer,budget):
    print("Player busts.")
    budget.loss()

def player_wins(player,dealer,budget):
    print("Player won.")
    budget.win()

def dealer_busts(player,dealer,budget):
    print("Dealer busts.")
    budget.win()

def dealer_wins(player,dealer,budget):
    print("Dealer won.")
    budget.loss()

def push(player,dealer):
    print("It's a tie.")

# GAMEPLAY
player_chips = Budget()
print("Welcome to BlackJack game.")
while True:
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal_player())
    player_hand.add_card(deck.deal_player())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal_player())
    dealer_hand.add_card(deck.deal_player())
    
    bet(player_chips)

    show_some(player_hand,dealer_hand)

    while playing:
        hit_or_stand(deck,player_hand)
        show_some(player_hand,dealer_hand)
        player_hand.adjust_ace
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
            show_all(player_hand,dealer_hand)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
            show_all(player_hand,dealer_hand)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
            show_all(player_hand,dealer_hand)
        else:
            push(player_hand,dealer_hand)
            show_all(player_hand,dealer_hand)
    if player_chips.balance == 0:
        print('You lost all your chips. Game Over.')
        playing = False
        break
    else:
        print("Player's wins stand at: ",player_chips.balance)
        new_game = input("Would you like to play another hand? Enter 'y' or 'n'.")
        if new_game[0].lower() == 'y':
            playing = True
            continue
        else:
            print('Thank for playing')
            break