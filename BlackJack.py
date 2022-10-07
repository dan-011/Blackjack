import random
import sys

#need to add MULTIPLE ace implementation
#fix card-total bug
class Node:
    def __init__(self, _item, _next = None):
        self._item = _item
        self._next = _next
    
    def __str__(self):
        if self._next is not None:
            return "Node(item = {}, next._item = {})".format(self._item, self._next._item) #doesn't work for tail node (no next for teail node)
        return "Node(item = {}, next = None)".format(self._item)

class ModifiedLinkedList:
    def __init__(self):
        self.head = None
        self.len = 0

    def add_first(self, item):
        node = Node(item, self.head)
        self.head = node
        self.len += 1
    
    

    def remove_first(self):
        if self.len == 0:
            raise RuntimeError
        else:
            item = self.head._item
            self.head = self.head._next
            self.len -= 1
            return item

    def remove_last(self):
        if self.len == 0:
            raise RuntimeError
        elif self.len == 1:
            return self.remove_first()
        else:
            current_node = self.head
            while current_node._next._next is not None:
                current_node = current_node._next
            item = current_node._next._item
            current_node._next = None
            self.len -= 1
            return item

    def __len__(self):
        return self.len
class Card:
    def __init__(self, value, suite):
        self.value_dict = {'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10,'jack': 10, 'queen': 10, 'king': 10, 'ace': 11}
        self.value = self.value_dict[value]
        self.is_ace = False
        if value == 'ace':
            self.is_ace = True
        self.suite = suite
        self.title = value + " of " + suite
        self.name = value


    def __str__(self):
        return self.title
class Deck:
    def __init__(self):
        self.deck = ModifiedLinkedList()
        empty_deck = []
        suits = ['hearts', 'diamonds', 'clubs', 'spades']
        values = ['two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten','jack', 'queen', 'king', 'ace']
        for suit in suits:
            for value in values:
                empty_deck.append(Card(value, suit))
        random.shuffle(empty_deck)
        for i in empty_deck:
            self.deck.add_first(i)
        self.store = set()

    def remove_card1(self):
        return self.deck.remove_first()


class Player:
    def __init__(self, name = "", start_money = 0):
        self.name = name
        self.total_money = start_money
        self.potential_return = 0
        self.card_sum = 0
        self.hand = []
        self._dealer_hand = []
        self._dealer_sum = 0
        self._dealer_text = ""
        self.deck = Deck()
        self.hand_text = ""
        self.store = set()
        self.can_bid = True
        self.is_bidding = False
        self.enter_name = False
        self.enter_money = False
        self.difficulty = "Easy"
        self.ask_change_difficulty = False
        self.changing_difficulty = False
        self.player_aces = 0
        self._dealer_aces = 0
        self.deal_count = 0
        self.borrowing = False
        self.debt = 0
    
    def remove_card(self):
        if len(self.deck.deck) == 0:
            print("Reshuffling...")
            self.deck = Deck()
        card = self.deck.remove_card1()
        if card in self.store:
            self.store.add(card)
            self.remove_card() #potential issue
        else:
            self.deal_count += 1
            return card
    
    def bid(self, amount):
        if amount > self.total_money:
            print("You don't have enough money")
        else:
            self.total_money -= amount
            self.potential_return = (amount*2)
            self.can_bid = False
    def player_add_to_hand(self, card):
        self.hand.append(card)
        self.card_sum += card.value
        if card.is_ace:
            self.player_aces += 1
        
    def dealer_add_to_hand(self, card):
        self._dealer_hand.append(card)
        self._dealer_sum += card.value
        if card.is_ace:
            self._dealer_aces += 1

    def deal(self):
        card1 = self.remove_card()
        self.player_add_to_hand(card1)
        card2 = self.remove_card()
        self.player_add_to_hand(card2)
        self.hand_text = "Your hand is the "+ str(self.hand[0]) + " and the " + str(self.hand[1])
        print(self.hand_text)
        if self.card_sum == 21:
            print("BLACKJACK")
            print("You Win")
            self.total_money += self.potential_return
            self.potential_return = 0
            self.hand = []
            self.card_sum = 0
            self.hand_text = ""
            self.can_bid =True
            self.player_aces = 0

            self._dealer_hand = []
            self._dealer_sum = 0
            self._dealer_text = ""
            self._dealer_aces = 0
        elif self.card_sum > 21 and self.player_aces > 0:
            self.card_sum -= 10
            self.player_aces -= 1

        card = self.remove_card()
        self._dealer_hand.append(card)
        self._dealer_sum += card.value
        card = self.remove_card()
        self._dealer_hand.append(card)
        self._dealer_sum += card.value

    def hit(self):
        card = self.remove_card()
        self.player_add_to_hand(card)
        self.hand_text += (" and the " + str(card))
        print(self.hand_text)
        if self.card_sum > 21:
            if self.player_aces > 0:
                self.card_sum -= 10
                self.player_aces -= 1
                if self.card_sum == 21:
                    print()
                    print("BLACKJACK")
                    self.stay()
            else:
                print()
                print("Bust")
                print("You Lost")
                self.potential_return = 0
                self.store = set()
                self.can_bid = True
                self.card_sum = 0
                self.player_aces = 0
                self.hand = []
                self.hand_text = ""
                self.player_aces = 0
        elif self.card_sum == 21:
            print()
            print("BLACKJACK")
            self.stay()

    def stay(self): # bug with dealer not stoping as soon as they exceed 21
        print()
        random.seed()
        if self.difficulty == "Easy":
            top = random.randrange(17,22,1)
        elif self.difficulty == "Medium":
            top = random.randrange(15,22,1) # fix difficulty settings
        elif self.difficulty == "Hard":
            top = random.randrange(13,22,1)
        self._dealer_sum = 0 #look for where this needs to be where it belongs
        self._dealer_hand = []
        self._dealer_aces = 0
        self._dealer_text = ""
        while self._dealer_sum < top:
            card = self.remove_card()
            self.dealer_add_to_hand(card)
            if self._dealer_sum > 21 and self._dealer_aces > 0: # fix dealer response to aces
                self._dealer_sum -= 10
                self._dealer_aces -= 1
        self._dealer_text = "The dealer has the " + str(self._dealer_hand[0])
        for card in self._dealer_hand[1:]:
            self._dealer_text += " and the " + str(card)
        
        print(self._dealer_text)
        print("with a sum of " + str(self._dealer_sum))

        if self._dealer_sum > 21:
            print("Dealer Busts")
            print()
            print("You Win")
            self.total_money += self.potential_return
            self.potential_return = 0
            self.hand = []
            self.card_sum = 0
            self.hand_text = ""
            self.can_bid = True
            self.player_aces = 0

            self._dealer_hand = []
            self._dealer_sum = 0
            self._dealer_aces = 0
            self._dealer_text = ""
        elif self.card_sum < self._dealer_sum:
            print()
            print("You Lose")
            self.potential_return = 0
            self.hand = []
            self.card_sum = 0
            self.hand_text = ""
            self.can_bid = True
            self.player_aces = 0

            self._dealer_hand = []
            self._dealer_sum = 0
            self._dealer_text = ""
            self._dealer_aces = 0
        elif self.card_sum > self._dealer_sum:
            print()
            print("You Win")
            self.total_money += self.potential_return
            self.potential_return = 0
            self.hand = []
            self.card_sum = 0
            self.hand_text = ""
            self.can_bid = True
            self.player_aces = 0

            self._dealer_hand = []
            self._dealer_sum = 0
            self._dealer_aces = 0
            self._dealer_text = ""
        elif self.card_sum < self._dealer_sum:
            print()
            print("You Lose")
            self.potential_return = 0
            self.hand = []
            self.card_sum = 0
            self.hand_text = ""
            self.can_bid = True
            self.player_aces = 0

            self._dealer_hand = []
            self._dealer_sum = 0
            self._dealer_text = ""
            self._dealer_aces = 0
        elif self.card_sum == self._dealer_sum:
            print("Split")
            self.total_money += (self.potential_return/2)

            self.potential_return = 0
            self.hand = []
            self.card_sum = 0
            self.hand_text = ""
            self.can_bid = True
            self.player_aces = 0

            self._dealer_hand = []
            self._dealer_sum = 0
            self._dealer_aces = 0
            self._dealer_text = ""

    def get_card_sum(self):
        print(self.card_sum)
    
    def get_commands(self):
        print("\tCommands:")
        print("\t\t - New Player (enter a new player)"+ "\t\t\t\t - bid (enter a starting bid)")
        print("\t\t - deal (begin game)"+"\t\t\t\t\t\t - hit (deal a card from the deck)")
        print("\t\t - total? (get total value of hand)"+"\t\t\t\t - stay (keep hand)")
        print("\t\t - earnings (get earnings)"+"\t\t\t\t\t - done (finish game)")
        print("\t\t - difficulty (get/change difficulty)"+"\t\t\t\t - my money (get total money)")
        print("\t\t - commands (get game commands)"+ "\t\t\t\t\t - borrow money (borrow money to pay back later)")
        print("\t\t - pay debt (payback the money borrowed)"+"\t\t\t - instructions (get game instructions)")

if __name__ == '__main__':
    print((" -"*38) + " BLACKJACK " + ("- "*38))
    p1 = Player()
    start_money = 0
    for line in sys.stdin:
        if p1.deal_count == 52:
            p1.store = set()
            p1.deal_count = 0
        elif line.rstrip() == "done":
            if p1.debt > 0:
                print("You cannot leave, you have to pay your debt of ${}0".format(p1.debt))
            else:
                print(p1.name + " leaves with $" + str(p1.total_money) + "0")
                break
        elif line.rstrip() == "New Player":
            print("Name?")
            p1.enter_name = True
        elif p1.enter_name:
            p1.name = line.rstrip()
            p1.enter_name = False
            p1.enter_money = True
            print("Enter Money")
        elif p1.enter_money:
            string = line.rstrip()
            try:
                p1.total_money = float(string)
                start_money = float(string)
            except Exception:
                p1.total_money = float(string[1:])
                start_money = float(string[1:])
            p1.enter_money = False
            print("Let's Play")
        elif line.rstrip() == "bid":
            if p1.total_money == 0:
                print("You don't have any money (you may borrow money to pay back later)")
            else:
                print("How much?")
                p1.is_bidding = True
        elif line.rstrip() == "all in":
            if p1.is_bidding:
                amount = p1.total_money
                p1.bid(p1.total_money)
                print("You have bid $" + str(amount))
                p1.is_bidding = False
            else:
                print("You must type 'bid' command first")
        elif p1.is_bidding:
            try:
                string = line.rstrip()
                amount = float(string)
                p1.bid(amount)
                if p1.potential_return != 0:
                    print("You have bid $" + string)
                    p1.is_bidding = False
            except Exception:
                try:
                    string = line.rstrip()
                    amount = float(string[1:])
                    p1.bid(amount)
                    if p1.potential_return != 0:
                        print("You have bid " + string + "0")
                        p1.is_bidding = False
                except Exception:
                    print("You have to enter an amount")
        elif line.rstrip() == "deal":
            if p1.potential_return == 0:
                print("You haven't bid anything yet")
            else:
                p1.deal()
        elif line.rstrip() == "hit":
            p1.hit()
        elif line.rstrip() == "total?":
            p1.get_card_sum()
        elif line.rstrip() == "stay":
            p1.stay()
        elif line.rstrip() == "earnings":
            earnings = p1.total_money - start_money
            print("You've made $" + str(earnings) + "0")
        elif line.rstrip() == "difficulty":
            print(p1.difficulty)
            print("Change Difficulty? (yes or no)")
            p1.ask_change_difficulty = True
        elif p1.ask_change_difficulty:
            if line.rstrip() == "yes":
                print("Enter Difficulty")
                p1.changing_difficulty = True
            p1.ask_change_difficulty = False
        elif p1.changing_difficulty:
            p1.difficulty = line.rstrip()
            p1.changing_difficulty = False
        elif line.rstrip() == "my money":
            print("$"+str(p1.total_money)+"0")
        elif line.rstrip() == "commands":
            p1.get_commands()
        elif line.rstrip() == "borrow money":
            print("Enter Amount")
            p1.borrowing = True
        elif p1.borrowing:
            try:
                string = line.rstrip()
                amount = float(string)
                p1.debt += amount
                p1.total_money += p1.debt
                if p1.debt != 0:
                    print("You owe $" + string)
                    p1.borrowing = False
            except Exception:
                try:
                    string = line.rstrip()
                    amount = float(string[1:])
                    p1.debt += amount
                    p1.total_money += p1.debt
                    if p1.debt != 0:
                        print("You owe " + string)
                        p1.borrowing = False
                except Exception:
                    print("You have to enter an amount")
        elif line.rstrip() == "debt?":
            print("You owe $"+str(p1.debt)+"0")
        elif line.rstrip() == "pay debt":
            if p1.total_money <= 0:
                print("You haven't earned anything")
            elif p1.debt > p1.total_money:
                p1.debt = p1.debt - p1.total_money
                p1.total_money = 0
                print("You still owe ${}0".format(p1.debt))
            else:
                p1.total_money = p1.total_money - p1.debt
                p1.debt = 0
                print("You are no longer in debt")
                print("You now have ${}0".format(p1.total_money))
        elif line.rstrip() == "instructions":
            print("BLACKJACK is a game of math. The idea of the game is to collect a hand of cards that has a total value that gets as close to 21 without exceeding 21. Each numeric\n\ncard's value corresponds to its number, the face cards have a value of 10, and the ace cards have a value of 1 or 11. You begin the game by being dealt two\n\ncards. If the immediate sum of the cards is equal to 21, you get the BLACKJACK and you win. Otherwise, you may HIT until you are satisfied with your hand and you\n\nSTAY. If the sum of your cards ever exceeds 21, you immediately lose. The dealer then plays and hits their hand until they stay. If they exceed 21 or if the sum\n\nof your hand is greater than the sum of theirs, they lose and you win. If the sum of the hands are the same, you SPLIT (tie) and nobody wins. Otherwise, you lose.\n\nYou may BID money which, if you win the game, you gain back twice as much. If you split, you gain back the money you bid. If you lose, you lose the money you bid.\n\nType 'commands' for gameplay commands.")
        else:
            print("TYPO")
            p1.get_commands()