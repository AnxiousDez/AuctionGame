import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Bidder:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def random_bid(self):
        return random.randint(1, self.value)

    def strategic_bid(self, reserve):
        # Implement a bidding strategy (e.g., value-based bidding)
        return min(self.value, reserve + random.randint(1, 10))

class AuctionGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Auction Game")
        self.root.geometry("600x400")  # Set initial window size
        self.root.resizable(True, True)  # Allow window resizing
        self.root.configure(bg="#f0f0f0")  # Set background color

        # Load player images
        self.alice_image = Image.open("football-player.png").resize((100, 100))
        self.alice_photo = ImageTk.PhotoImage(self.alice_image)

        self.bob_image = Image.open("baseball-player.png").resize((100, 100))
        self.bob_photo = ImageTk.PhotoImage(self.bob_image)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Labels and entries for player 1
        tk.Label(self.root, text="Player 1", font=("Arial", 16, "bold"), bg="#f0f0f0").place(x=50, y=50)
        tk.Label(self.root, image=self.alice_photo, bg="#f0f0f0").place(x=50, y=100)
        tk.Label(self.root, text="Name:", font=("Arial", 12), bg="#f0f0f0").place(x=50, y=220)
        self.alice_name_entry = tk.Entry(self.root, font=("Arial", 12), width=15)
        self.alice_name_entry.place(x=110, y=220)
        tk.Label(self.root, text="Value:", font=("Arial", 12), bg="#f0f0f0").place(x=50, y=260)
        self.alice_value_entry = tk.Entry(self.root, font=("Arial", 12), width=15)
        self.alice_value_entry.place(x=110, y=260)

        # Labels and entries for player 2
        tk.Label(self.root, text="Player 2", font=("Arial", 16, "bold"), bg="#f0f0f0").place(x=350, y=50)
        tk.Label(self.root, image=self.bob_photo, bg="#f0f0f0").place(x=350, y=100)
        tk.Label(self.root, text="Name:", font=("Arial", 12), bg="#f0f0f0").place(x=350, y=220)
        self.bob_name_entry = tk.Entry(self.root, font=("Arial", 12), width=15)
        self.bob_name_entry.place(x=410, y=220)
        tk.Label(self.root, text="Value:", font=("Arial", 12), bg="#f0f0f0").place(x=350, y=260)
        self.bob_value_entry = tk.Entry(self.root, font=("Arial", 12), width=15)
        self.bob_value_entry.place(x=410, y=260)

        # Reserve and rounds entries
        tk.Label(self.root, text="Reserve Price:", font=("Arial", 12), bg="#f0f0f0").place(x=50, y=300)
        self.reserve_entry = tk.Entry(self.root, font=("Arial", 12), width=15)
        self.reserve_entry.place(x=160, y=300)
        tk.Label(self.root, text="Number of Rounds:", font=("Arial", 12), bg="#f0f0f0").place(x=350, y=300)
        self.num_rounds_entry = tk.Entry(self.root, font=("Arial", 12), width=15)
        self.num_rounds_entry.place(x=490, y=300)

        # Bidding strategy option menu
        self.strategy_var = tk.StringVar(self.root)
        self.strategy_var.set("Random")
        tk.Label(self.root, text="Select Bidding Strategy:", font=("Arial", 12), bg="#f0f0f0").place(x=50, y=350)
        tk.OptionMenu(self.root, self.strategy_var, "Random", "Value-Based").place(x=200, y=345)

        # Start button
        start_button = tk.Button(self.root, text="Start Game", font=("Arial", 14), command=self.start_game, bg="#4CAF50", fg="white")
        start_button.place(x=250, y=380)

    def start_game(self):
        alice_name = self.alice_name_entry.get()
        bob_name = self.bob_name_entry.get()
        alice_value = int(self.alice_value_entry.get())
        bob_value = int(self.bob_value_entry.get())
        reserve = int(self.reserve_entry.get())
        num_simulations = int(self.num_rounds_entry.get())
        strategy = self.strategy_var.get()

        alice = Bidder(alice_name, alice_value)
        bob = Bidder(bob_name, bob_value)

        total_alice_payoff = total_bob_payoff = total_auctioneer_payoff = 0
        winners = {alice.name: 0, bob.name: 0, "None": 0}

        for round_num in range(1, num_simulations + 1):
            if strategy == "Random":
                alice_bid = alice.random_bid()
                bob_bid = bob.random_bid()
            elif strategy == "Value-Based":
                alice_bid = alice.strategic_bid(reserve)
                bob_bid = bob.strategic_bid(reserve)

            if alice_bid > bob_bid and alice_bid >= reserve:
                winner = alice
                winner_bid = alice_bid
            elif bob_bid > alice_bid and bob_bid >= reserve:
                winner = bob
                winner_bid = bob_bid
            else:
                winner = None
                winner_bid = 0

            alice_payoff = payoff_bidder(alice.value, alice_bid, reserve, winner_bid)
            bob_payoff = payoff_bidder(bob.value, bob_bid, reserve, winner_bid)
            auctioneer_payoff = payoff_auctioneer(reserve, winner_bid)

            total_alice_payoff += alice_payoff
            total_bob_payoff += bob_payoff
            total_auctioneer_payoff += auctioneer_payoff

            if winner:
                winners[winner.name] += 1
            else:
                winners["None"] += 1

        average_alice_payoff = total_alice_payoff / num_simulations
        average_bob_payoff = total_bob_payoff / num_simulations
        average_auctioneer_payoff = total_auctioneer_payoff / num_simulations

        messagebox.showinfo("Results", 
                            f"{alice.name}: ${average_alice_payoff:.2f}\n"
                            f"{bob.name}: ${average_bob_payoff:.2f}\n"
                            f"Auctioneer: ${average_auctioneer_payoff:.2f}\n"
                            f"Overall Winners:\n{alice.name}: {winners[alice.name]} wins\n"
                            f"{bob.name}: {winners[bob.name]} wins\n"
                            f"None: {winners['None']}")

def payoff_bidder(value, bid, reserve, winner_bid):
    if bid > winner_bid and bid >= reserve:
        return value - bid
    else:
        return 0

def payoff_auctioneer(reserve, winner_bid):
    if winner_bid >= reserve:
        return winner_bid - reserve
    else:
        return 0

if __name__ == "__main__":
    root = tk.Tk()
    app = AuctionGame(root)
    root.mainloop()
