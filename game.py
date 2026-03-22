# ============================================================
# game.py — Project 2: RPG Character Engine
# DO NOT modify the run_battle() function below.
# Add all of your class definitions and functions beneath it.
# ============================================================

import random

def run_battle(fighter1, fighter2):
    """
    Runs a turn-based battle between two character objects.
    The higher level character attacks first each round.
    Returns the winning character.

    Parameters:
        fighter1: a character object with attack(), is_alive(), and comparison methods
        fighter2: a character object with attack(), is_alive(), and comparison methods

    Returns:
        The character object that is still alive at the end of the battle.
    """
    print(f"\n{'='*40}")
    print(f"  BATTLE START")
    print(f"  {fighter1} vs {fighter2}")
    print(f"{'='*40}")

    round_num = 1
    while fighter1.is_alive() and fighter2.is_alive():
        print(f"\n--- Round {round_num} ---")

        # Higher level character attacks first
        if fighter1 > fighter2:
            first, second = fighter1, fighter2
        else:
            first, second = fighter2, fighter1

        first.attack(second)
        print(f"  {first.name} attacks {second.name}")
        print(f"  {second}")

        if second.is_alive():
            second.attack(first)
            print(f"  {second.name} attacks {first.name}")
            print(f"  {first}")

        round_num += 1

    winner = fighter1 if fighter1.is_alive() else fighter2
    print(f"\n{'='*40}")
    print(f"  {winner.name} wins!")
    print(f"{'='*40}\n")
    return winner


# ============================================================
# Write your classes and functions below this line.
# ============================================================
