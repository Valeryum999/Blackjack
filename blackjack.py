import random
import time
from math import floor,ceil
not_tens = [str(a) for a in range(2,10)]


class Blackjack:
    def __init__(self,balance=0,automatic=False):
        self.balance = balance
        self.original_balance = self.balance
        self.hand = []
        self.second_hand = []
        self.dealers_hand = []
        self.current_count = 0
        self.true_count = 0
        self.sum_of_counts = 0
        self.number_of_games = 0
        self.number_of_wins = 0
        self.deck = []
        self.deck_limit = 156
        self.automatic = automatic
        self.auto_bet = automatic

        self.initialize_deck()

    def deposit(self):
        if self.automatic:
            self.balance = 100
            return
        while(True):
            amount = input("How much do you want to deposit? $")
            if amount.isdigit():
                amount = int(amount)
                if amount <= 0:
                    print("Please enter a valid amount.")
                else:
                    self.balance = amount
            else:
                print("Please enter a number.")

    def control_bet(self,balance,auto_bet,true_count):
        if auto_bet:
            bet = max(5,5*true_count)
            return bet
        while(True):
            bet = input("How much do you want to bet? $")
            if bet.isdigit():
                bet = int(bet)
                if bet > self.balance:
                    print("The amount you're trying to bet exceeds your current balance.")
                elif bet<=0:
                    print("Please enter a positive amount.")
                else:    
                    return bet
            else:
                print("Please enter a number.")
        
    def initialize_deck(self):
        for _ in range(6):
            self.add_suit('♥')
            self.add_suit('♦')
            self.add_suit('♧')
            self.add_suit('♤')
        random.shuffle(self.deck)
        
    def add_suit(self,char):
        self.deck.append('A'+char)
        for i in range(2,11):
            self.deck.append(str(i)+char)
        self.deck.append('J'+char)
        self.deck.append('Q'+char)
        self.deck.append('K'+char)

    def print_table(self,dealers_hand,my_hand):
        if not self.automatic:
            print(f"Dealer's hand:\t{dealers_hand}({self.sum_of_hand(dealers_hand)})")
            print()
            print(f"Your hand:\t{my_hand}({self.sum_of_hand(my_hand)})")
            print("---------------------")

    def add_card(self,hand):
        hand.append(self.deck.pop())

    def sum_of_hand(self,hand):
        sum = 0
        numberOfAces = 0
        for card in hand:
            if card[0] in not_tens and not "10" in card[0:2]:
                sum += int(card[0])
            elif card[0]=='A':
                numberOfAces += 1
            else:
                sum += 10
        while numberOfAces>0:
            if sum + 11 <= 21:
                sum += 11
            else:
                sum+=1
            numberOfAces-=1
        return sum

    def count(self,hand):
        count = 0
        for card in hand:
            if card[0] in ['2','3','4','5','6']:
                count += 1
            if card[0] in ['J','Q','K','A'] or "10" in card[0:2]:
                count -= 1
        return count

    def control_blackjack(self,hand):
        if self.sum_of_hand(hand)==21 and len(hand)==2:
            return True
        else:
            return False

    def check_double(self,hand):
        tmp = '0'
        if len(hand) == 2:
            for card in hand:
                if tmp != '0':
                    if tmp == card[0]:
                        return True
                    else:
                        return False
                else:
                    tmp = card[0]


    def correct_move(self,dealers_hand,my_hand):
        sum_of_dealers_hand = self.sum_of_hand(dealers_hand)
        sum_of_my_hand = self.sum_of_hand(my_hand)
        # da implementare gli assi e gli split
        if self.check_double(my_hand):
            if "A" in my_hand[0] or "8" in my_hand[0] or "9" in my_hand[0]:
                return 'split'

        if "A" in my_hand[0] or "A" in my_hand[1]:
            if sum_of_my_hand >= 19:
                return 'stay'
            elif sum_of_my_hand == 18:
                if sum_of_dealers_hand < 7:
                    return 'double'
                elif sum_of_dealers_hand < 9:
                    return 'stay'
                else:
                    return 'hit'
            elif sum_of_my_hand == 17:
                if sum_of_dealers_hand == 2:
                    return 'hit'
                elif sum_of_dealers_hand < 7:
                    return 'double'
                else:
                    return 'hit'
            elif sum_of_my_hand == 16 or sum_of_my_hand == 15:
                if sum_of_dealers_hand < 4:
                    return 'hit'
                elif sum_of_dealers_hand < 7:
                    return 'double'
                else:
                    return 'hit'
            elif sum_of_my_hand == 14 or sum_of_my_hand == 13:
                if sum_of_dealers_hand < 5:
                    return 'hit'
                elif sum_of_dealers_hand < 7:
                    return 'double'
                else:
                    return 'hit'
        if sum_of_my_hand>=17:
            return 'stay'
        elif sum_of_my_hand<17 and sum_of_my_hand>=13:
            if sum_of_dealers_hand >= 6:
                return 'hit'
            else:
                return 'stay'
        elif sum_of_my_hand == 12:
            if sum_of_dealers_hand < 4 or sum_of_dealers_hand>6:
                return 'hit'
            else:
                return 'stay'
        elif sum_of_my_hand == 11:
            return 'double' 
        elif sum_of_my_hand == 10:
            if sum_of_dealers_hand<10:
                return 'double'
            else:
                return 'hit'
        elif sum_of_my_hand == 9:
            if sum_of_dealers_hand >=3 and sum_of_dealers_hand <=6:
                return 'double'
            else:
                return 'hit'
        elif sum_of_my_hand <= 8:
            return 'hit'

    def your_turn(self,dealers_hand,your_hand,bet):
        #Decisione Automatica
        second_hand = []
        while(True):
            decision = self.correct_move(dealers_hand,your_hand)
            if len(second_hand) > 0:
                self.your_turn(dealers_hand,second_hand,bet)
            if decision == 'stay':
                break
            if decision == 'hit':
                self.add_card(your_hand)
                continue
            if decision == 'double':
                self.add_card(your_hand)
                self.balance -= bet #bug da risolvere sometime
                bet*=2
                break
            if decision == 'split':
                second_hand = [your_hand.pop()]
                self.add_card(second_hand)
                self.add_card(your_hand)
        return bet,second_hand

    def dealers_turn(self,dealers_hand,your_hand):
        while self.sum_of_hand(dealers_hand)<17:
            if not self.automatic:
                time.sleep(1)
            self.add_card(dealers_hand)
            self.print_table(dealers_hand,your_hand)
            if not self.automatic:
                time.sleep(1)

    def control_who_won(self,dealers_hand,your_hand,bet):
        if self.control_blackjack(your_hand):
            self.dealers_turn(dealers_hand,your_hand)
            self.print_table(dealers_hand,your_hand)
            if not self.automatic:
                print("Blackjack babeee")
            self.number_of_wins += 1
            self.number_of_games += 1
            self.balance += bet*2 + bet/2
        elif self.sum_of_hand(your_hand) > 21:
            self.print_table(dealers_hand,your_hand)
            if not self.automatic:
                print("You lost.")
            self.number_of_games += 1
        else:
            if self.sum_of_hand(dealers_hand)<self.sum_of_hand(your_hand) or self.sum_of_hand(dealers_hand) > 21:
                if not self.automatic:
                    print("You won!")
                self.balance += 2*bet
                self.number_of_wins += 1
                self.number_of_games += 1
            elif self.sum_of_hand(dealers_hand) == self.sum_of_hand(your_hand):
                if not self.automatic:    
                    print("Tie.")
                self.balance += bet
            else:
                if not self.automatic:    
                    print("You lost.")
                self.number_of_games += 1

    def stats(self):
            if not self.automatic:
                print("Statistics about this run:")
                print(f"Current count is: {self.current_count} and current length of deck is: {len(self.deck)}\nTrue count is: {self.true_count}")
                print(f"Average count along the game: {(self.sum_of_counts/self.number_of_games):.2f}")
                print(f"You have won {self.number_of_wins} out of {self.number_of_games} games, for a {(self.number_of_wins/self.number_of_games * 100):.2f}% winrate and a net gain of {self.balance - self.original_balance}")
            return (self.sum_of_counts/self.number_of_games),self.number_of_wins,self.number_of_games,(self.balance - self.original_balance)

    def main(self):
        self.deposit()
        self.original_balance = self.balance
        if not self.automatic:
            self.automatic = True if str(input("Want to auto-play? (y/n)")) == "y" else False
            self.auto_bet = True if self.automatic else False 

        while(True):
            if len(self.deck ) <= self.deck_limit:
                return self.stats()
            
            bet = self.control_bet(self.balance,self.auto_bet,self.true_count)
            self.balance -= bet
            dealers_hand = [self.deck.pop()]
            your_hand = [self.deck.pop(),self.deck.pop()]

            self.print_table(dealers_hand,your_hand)

            bet,second_hand = self.your_turn(dealers_hand,your_hand,bet)
            self.dealers_turn(dealers_hand,your_hand)
            self.control_who_won(dealers_hand,your_hand,bet)
            if len(second_hand) > 0:
                self.print_table(dealers_hand,second_hand)
                self.control_who_won(dealers_hand,second_hand,bet)
                self.current_count += self.count(second_hand)
                self.sum_of_counts += self.current_count
            
            self.current_count += self.count(dealers_hand) + self.count(your_hand)
            self.sum_of_counts += self.current_count
            self.true_count = round(self.current_count/(round(len(self.deck)/52)))
            if not self.automatic:
                print(f"Your current balance is: {self.balance}")
                print(f"Current count is: {self.current_count} and current length of deck is: {len(self.deck)}\nTrue count is: {self.true_count}")
                print(f"You have won {self.number_of_wins} out of {self.number_of_games} games, for a {(self.number_of_wins/self.number_of_games * 100):.2f}% winrate and a net gain of {self.balance - self.original_balance}")

def mean(list):
    sum = 0
    for element in list:
        sum += element
    return round(sum/len(list),2)

avg_of_counts_in_games = []
avg_of_wins = []
avg_of_games = []
avg_of_net_gains = []

for _ in range(1000):
    b = Blackjack(100,True)
    avg_count, wins, games, net_gain = b.main()
    avg_count = round(avg_count,2)
    avg_of_counts_in_games.append(avg_count)
    avg_of_wins.append(wins)
    avg_of_games.append(games)
    avg_of_net_gains.append(net_gain)

print("Statistics about this simulation:")
print(f"Avg of running count in games:{mean(avg_of_counts_in_games)}")
print(f"Avg of games:{mean(avg_of_games)}")
print(f"Avg of wins:{mean(avg_of_wins)}")
print(f"Avg of net_gains:{mean(avg_of_net_gains)}")
