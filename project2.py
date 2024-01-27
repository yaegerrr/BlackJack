import random
import time
import csv
import tkinter as tk


ace = [1, 11]
jacks = 10
kings = 10
queens = 10
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10]
balance_file = "money.csv"

class Blackjackgame:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x500")
        self.master.title("Yaeger's BlackJack")

        self.balance = self.read_balance()
        self.deck  = numbers + [jacks, kings, queens, random.choice(ace)]
        self.player_hand = [self.get_random_card(self.deck), self.get_random_card(self.deck)]
        self.dealer_hand = [self.get_random_card(self.deck)]

        self.stood = False

        self.balance_label = tk.Label(master, text=f"balance: {self.balance}", font=('Arial', 16))
        self.balance_label.pack()

        self.bet_label = tk.Label(master, text="Enter your bet: ", font=('Arial', 14))
        self.bet_label.pack()

        self.bet_entry = tk.Entry(master, font=('Arial',14))
        self.bet_entry.pack()

        self.play_round_button = tk.Button(master, text="play round", command=self.play_round, font=('Arial', 14))
        self.play_round_button.pack()

        self.quit_button = tk.Button(master, text="quit", command=self.master.destroy, font=('Arial', 14))
        self.quit_button.pack()

        self.another_round_button = tk.Button(master, text="another round", command=self.another_round, font=('Arial', 14))
        self.another_round_button.pack()

        self.hit_button = tk.Button(master, text="Hit", command=self.hit)
        self.hit_button.pack()

        self.stand_button = tk.Button(master, text="Stand", command=self.stand)
        self.stand_button.pack()

        self.info_label = tk.Label(master, text="", font=('Arial', 14))
        self.info_label.pack()

    def dealer_turn(self):
        while self.calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.get_random_card(self.deck))
            self.display_initial_hands()
    
    
    def play_round(self):
        try:
            bet = int(self.bet_entry.get())
            if bet > self.balance or bet <= 0:
                self.show_info("Invalid bet. Please enter a valid amount.")
                return
        except ValueError:
            self.show_info("Invalid bet. Please enter a valid amount.")
            return
       
        self.display_initial_hands()     
        self.player_turn()
        self.update_balance()
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.play_round_button.config(state=tk.DISABLED)
        self.another_round_button.config(state=tk.DISABLED)
        
    def another_round(self):
        if self.stood:
            self.stood = False
            self.player_hand = [self.get_random_card(self.deck), self.get_random_card(self.deck)]
            self.dealer_hand = [self.get_random_card(self.deck)]
            self.show_info("")
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)
            self.play_round_button.config(state=tk.NORMAL)
            self.another_round_button.config(state=tk.DISABLED)
            self.display_initial_hands()
        else:
            self.show_info("finish round before starting another")


    def player_turn(self):
        if self.stood:
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.winner(self.bet_entry.get())         
        else:
            self.hit_button.config(state=tk.NORMAL)
            self.stand_button.config(state=tk.NORMAL)



    def hit(self):
        self.player_hand.append(self.get_random_card(self.deck))
        self.display_player_hand()

        if self.calculate_hand_value(self.player_hand) >= 21:
            self.stood = True
            self.player_turn()


    def stand(self):
        self.stood = True
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.dealer_turn()
        self.winner(self.bet_entry.get())

    def display_player_hand(self):
        self.show_info(f"Players hand: {self.player_hand} Total = {self.calculate_hand_value(self.player_hand)}\nDealers Hand: {self.dealer_hand} Total = {self.calculate_hand_value(self.dealer_hand)}")
        

    def display_initial_hands(self):
        if not self.stood:
            self.show_info("place bet and play")
            return
        self.show_info(f"Players hand: {self.player_hand} Total = {self.calculate_hand_value(self.player_hand)}\nDealers Hand: {self.dealer_hand} Total = {self.calculate_hand_value(self.dealer_hand)}")
        self.another_round_button.config(state=tk.NORMAL)
        self.play_round_button.config(state=tk.DISABLED)

    def show_info(self, message):
        self.info_label.config(text=message)

    def read_balance(self):
        with open(balance_file, "r") as file:
            reader = csv.reader(file)
            balance = int(list(reader)[0][0])
        return balance
    
    def update_balance(self):
        with open(balance_file, "w") as file:
            file.write(f"{self.balance}")
        self.balance_label.config(text=f"Balance: {self.balance}")

    def get_random_card(self, deck):
        return random.choice(deck)

    def calculate_hand_value(self, hand):
        value = sum(hand)
        if 1 in hand and value + 10 <= 21:
            value +=10
        return value
    
    def winner(self, bet_str):
        bet = int(bet_str)
        player_hand_value = self.calculate_hand_value(self.player_hand)
        dealer_hand_value = self.calculate_hand_value(self.dealer_hand)

        final_message = f"Player's final hand: {self.player_hand} Total = {player_hand_value}\nDealer's final hand: {self.dealer_hand} Total = {dealer_hand_value}\n"

        if dealer_hand_value > 21 and player_hand_value > 21:
            return self.show_info (final_message + "TIE both bust")

        if player_hand_value > dealer_hand_value and player_hand_value <= 21:
            self.balance += bet
            time.sleep(1)
            return self.show_info(final_message + "PLAYER WINS!"), self.update_balance()

        elif dealer_hand_value > player_hand_value and dealer_hand_value <= 21:
            self.balance -= bet
            time.sleep(1)
            return self.show_info(final_message + "HOUSE WINS!"), self.update_balance()

        elif dealer_hand_value > 21:
            self.balance += bet
            time.sleep(1)
            return self.show_info(final_message + "HOUSE BUST,\nPLAYER WINS!"), self.update_balance()

        elif player_hand_value > 21:
            self.balance -= bet
            time.sleep(1)
            return self.show_info(final_message + "PLAYER BUST,\nHOUSE WINS!"), self.update_balance()

        elif dealer_hand_value == player_hand_value:
            return self.show_info(final_message + "TIE")
        
        




def main():
    root = tk.Tk()
    game = Blackjackgame(root)
    root.mainloop()

 
if __name__ == "__main__":
    main()
