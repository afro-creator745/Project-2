"""
COMP 163 - Introduction to Programming
Project: 2 RPG Character Engine
Name: Hakeem Cole
GitHub Username: afro-creator745
Date: 4/3/2026
Description: A use of classes, functions, and methods to create characters with different stats and
classes battle to the death.
"""




# ============================================================
# game.py — Project 2: RPG Character Engine
# DO NOT modify the run_battle() function below.
# Add all of your class definitions and functions beneath it.
# ============================================================

import random
import csv
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



class Serializable:
    def save(self, filepath):
        """
        Saves this object's data to a text file.

        Parameters:
            filepath: the file name to save to

        Returns:
            None
        """
        with open(filepath, "w") as file:
            file.write(f"name={self.name}\n")
            file.write(f"level={self.level}\n")
            file.write(f"health={self.health}\n")
            file.write(f"attack_power={self.attack_power}\n")
            file.write(f"defense={self.defense}\n")

    def load(self, filepath):
        """
        Loads this object's data from a text file.

        Parameters:
            filepath: the file name to load from

        Returns:
            None
        """
        with open(filepath, "r") as file:
            for line in file:
                key, value = line.strip().split("=")

                if key == "name":
                    self.name = value
                elif key == "level":
                    self.level = int(value)
                elif key == "health":
                    self.health = float(value)
                elif key == "attack_power":
                    self.attack_power = float(value)
                elif key == "defense":
                    self.defense = float(value)


class Character:

    def __init__(self, name, level = 1, health = 100, attack_power = 1.0, defense = 1.0):
        self.name = name
        self.level = level       #creating thr stats of the character
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.attack_move = "Hasn't attacked yet"

    def defend(self, damage):
        attack_damage = damage - ((self.defense / 150) * damage)
        self.health -= attack_damage     #damage is delt by making the defense stat a percentage
                                        # then multiple it to damage and subtract it from the original damag

    def attack(self, target):
        hit_points = self.attack_power * 15
        target.defend(hit_points)  #base method for attack though every class as their own attack method



# Methods under here are pretty self explanatory
    def __str__(self):
        return (f'\nCharacter: {self.name}\n'
                f'Attack Move: {self.attack_move}\n'
                f'Level: {self.level}\n'
                f'Health: {self.health}\n'
                f'Attack Power: {self.attack_power}\n'
                f'Defense: {self.defense}\n')

    def is_alive(self):
        return self.health > 0

    def __lt__(self, other):
       return self.level < other.level

    def __gt__(self, other):
       return self.level > other.level





# dictionary that has the set values for the different attack possibilities
attack_list = {'Warrior hit': 5,'Mage hit': 1, 'Rogue hit': 3, "Swing": 10, 'Barbarian Axe': 20, "Warrior's Rage": 30, 'Berserker': 45,
                       'Fireball': 15, 'Lighting Blast': 35, "Asteroid Storm": 50, "Divine Ray": 65,
                       'Dagger': 5, 'Stealth Slash': 10, 'Shadow Assault': 20, "Abyss": 45}





class Warrior(Character, Serializable):
    def __init__(self, name, level, health, attack_power, defense):


        super().__init__(name, level, health, attack_power, defense)

#Warrior class attack options based on level
    def attack(self, target):
        if self.level >= 15 and self.level < 35:
            attack_move = "Swing"
        elif self.level < 65 and self.level >= 35:
            attack_move = "Barbarian Axe"
        elif self.level < 90 and self.level >= 65:
            attack_move = "Warrior's Rage"
        elif self.level >= 90:
            attack_move = "Berserker"
        else:
            attack_move = 'Warrior hit'

        for i in attack_list:   #runs to the dictionary to find what attack is being used and itc corresponding value
            if i == attack_move:
                attack_points = attack_list[i]

         #Adds more attack power by making attack power stat a percentage then multiplying to
        # the attack points and then added it to attack points again to get total
        hit_points = attack_points + (self.attack_power / 100) * attack_points
        target.defend(hit_points)

        #tracks the attack move used
        self.attack_move = attack_move

        #Warrior class defend boost the percentage made will be higher sinces it's divided by 100 and not 150
    def defend(self, damage):
        attack_damage = damage - ((self.defense / 100) * damage)
        self.health -= attack_damage





class Mage(Character, Serializable):
    def __init__(self, name, level, health, attack_power, defense):


        super().__init__(name, level, health, attack_power, defense)

    # Mage class attack options based on level
    def attack(self, target):
        if self.level >= 15 and self.level < 35:
            attack_move = "Fireball"
        elif self.level < 65 and self.level >= 35:
            attack_move = "Lighting Blast"
        elif self.level < 90 and self.level >= 65:
            attack_move = "Asteroid Storm"
        elif self.level >= 90:
            attack_move = "Divine Ray"
        else:
            attack_move = 'Mage hit'

        for i in attack_list:
            if i == attack_move:    #runs to the dictionary to find what attack is being used and itc corresponding value
                attack_points = attack_list[i]


        # Adds more attack power by making attack power stat a percentage then multiplying to
        # the attack points and then added it to attack points again to get total
        hit_points = attack_points + (self.attack_power / 100) * attack_points
        target.defend(hit_points)

        # tracks the attack move used
        self.attack_move = attack_move





class Rogue(Character, Serializable):
    def __init__(self, name, level, health, attack_power, defense):

        super().__init__(name, level, health, attack_power, defense)

    # Rouge class attack options based on level
    def attack(self, target):
        if self.level >= 15 and self.level < 35:
            attack_move = "Dagger"
        elif self.level < 65 and self.level >= 35:
            attack_move = "Stealth Slash"
        elif self.level < 90 and self.level >= 65:
            attack_move = "Shadow Assault"
        elif self.level >= 90:
            attack_move = "Abyss"
        else:
            attack_move = 'Rogue hit'
        # set attacks moves with set values

        for i in attack_list:
            if i == attack_move:  #runs to the dictionary to find what attack is being used and itc corresponding value
                attack_points = attack_list[i]

        # Adds more attack power by making attack power stat a percentage then multiplying to
        # the attack points and then added it to attack points again to get total
        hit_points = attack_points + (self.attack_power / 100) * attack_points
        target.defend(hit_points)

        # tracks the attack move used
        self.attack_move = attack_move



def load_characters(filepath):
    """
    Loads characters from a CSV file and returns them in a list.

    Parameters:
        filepath: the CSV file name

    Returns:
        A list of character objects
    """
    characters = []

    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            name = row["name"]
            char_type = row["character_type"]
            level = int(row["level"])
            health = float(row["health"])
            attack_power = float(row["attack_power"])
            defense = float(row["defense"])

            if char_type == "Warrior":
                character = Warrior(name, level, health, attack_power, defense)
            elif char_type == "Mage":
                character = Mage(name, level, health, attack_power, defense)
            elif char_type == "Rogue":
                character = Rogue(name, level, health, attack_power, defense)
            characters.append(character)
    return characters

def main():
    """
    Main function that loads characters and runs battles

    """
    Hakeem = Warrior("Hakeem", 78, 100, 20, 65)
    Phill = Mage("Phill", 45, 100, 15, 45)

    run_battle(Phill, Hakeem)

    characters = load_characters("characters.csv")
    for character in characters:
        print(character)

    run_battle(characters[8], characters[1])



if __name__ == "__main__":
    main()