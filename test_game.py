import pytest
import os

import game
from game import Character, Warrior, Mage, Rogue, Serializable, load_characters


# ============================================================
# Shared test fixtures
# ============================================================

def make_character():
    """Returns a base Character with known attributes."""
    return Character("TestHero", 5, 100.0, 20.0, 10.0)

def make_warrior():
    return Warrior("TestWarrior", 5, 100.0, 20.0, 10.0)

def make_mage():
    return Mage("TestMage", 5, 100.0, 20.0, 10.0)

def make_rogue():
    return Rogue("TestRogue", 5, 100.0, 20.0, 10.0)

TEST_CSV_CONTENT = """name,character_type,level,health,attack_power,defense
Aldric,Warrior,8,120.0,18.0,15.0
Lyssa,Mage,9,70.0,32.0,5.0
Nyx,Rogue,7,88.0,21.0,10.0
"""


# ============================================================
# Character constructor and attributes — 6 points
# ============================================================

class TestCharacterConstructor:

    def test_name_attribute(self):
        """Character should store the name attribute correctly."""
        c = make_character()
        assert c.name == "TestHero"

    def test_level_attribute(self):
        """Character should store level as an int."""
        c = make_character()
        assert c.level == 5
        assert isinstance(c.level, int)

    def test_health_attribute(self):
        """Character should store health as a float."""
        c = make_character()
        assert c.health == 100.0
        assert isinstance(c.health, float)

    def test_attack_power_attribute(self):
        """Character should store attack_power correctly."""
        c = make_character()
        assert c.attack_power == 20.0

    def test_defense_attribute(self):
        """Character should store defense correctly."""
        c = make_character()
        assert c.defense == 10.0

    def test_multiple_instances_independent(self):
        """Two Character instances should not share state."""
        c1 = Character("Hero", 5, 100.0, 20.0, 10.0)
        c2 = Character("Villain", 8, 150.0, 25.0, 12.0)
        assert c1.name != c2.name
        assert c1.health != c2.health


# ============================================================
# Character.__str__ — 4 points
# ============================================================

class TestCharacterStr:

    def test_returns_string(self):
        """__str__ should return a string."""
        c = make_character()
        assert isinstance(str(c), str)

    def test_contains_name(self):
        """__str__ output should include the character's name."""
        c = make_character()
        assert "TestHero" in str(c)

    def test_contains_level(self):
        """__str__ output should include the character's level."""
        c = make_character()
        assert "5" in str(c)

    def test_contains_health(self):
        """__str__ output should include the character's current health."""
        c = make_character()
        assert "100" in str(c)

    def test_str_reflects_updated_health(self):
        """__str__ output should reflect health after it has changed."""
        c = make_character()
        c.health = 55.0
        assert "55" in str(c)


# ============================================================
# Character.__lt__ and __gt__ — 4 points
# ============================================================

class TestCharacterComparison:

    def test_gt_higher_level(self):
        """Higher level character should be greater than lower level."""
        low = Character("Low", 3, 100.0, 20.0, 10.0)
        high = Character("High", 8, 100.0, 20.0, 10.0)
        assert high > low

    def test_lt_lower_level(self):
        """Lower level character should be less than higher level."""
        low = Character("Low", 3, 100.0, 20.0, 10.0)
        high = Character("High", 8, 100.0, 20.0, 10.0)
        assert low < high

    def test_gt_returns_bool(self):
        """__gt__ should return a boolean."""
        c1 = Character("A", 5, 100.0, 20.0, 10.0)
        c2 = Character("B", 3, 100.0, 20.0, 10.0)
        assert isinstance(c1 > c2, bool)

    def test_lt_returns_bool(self):
        """__lt__ should return a boolean."""
        c1 = Character("A", 3, 100.0, 20.0, 10.0)
        c2 = Character("B", 5, 100.0, 20.0, 10.0)
        assert isinstance(c1 < c2, bool)


# ============================================================
# Character.is_alive() — 4 points
# ============================================================

class TestIsAlive:

    def test_alive_with_full_health(self):
        """Character with full health should be alive."""
        c = make_character()
        assert c.is_alive() is True

    def test_alive_with_low_health(self):
        """Character with health above zero should be alive."""
        c = make_character()
        c.health = 0.1
        assert c.is_alive() is True

    def test_dead_at_zero_health(self):
        """Character with zero health should not be alive."""
        c = make_character()
        c.health = 0.0
        assert c.is_alive() is False

    def test_dead_below_zero_health(self):
        """Character with negative health should not be alive."""
        c = make_character()
        c.health = -10.0
        assert c.is_alive() is False


# ============================================================
# Character.defend() — 4 points
# ============================================================

class TestCharacterDefend:

    def test_health_reduced_after_defend(self):
        """Health should decrease after defend() is called."""
        c = make_character()
        initial_health = c.health
        c.defend(30.0)
        assert c.health < initial_health

    def test_defend_returns_none(self):
        """defend() should not return a value."""
        c = make_character()
        result = c.defend(10.0)
        assert result is None

    def test_health_not_negative_by_large_hit(self):
        """After a massive hit health may reach zero or below but defend should still run."""
        c = make_character()
        try:
            c.defend(9999.0)
        except Exception as e:
            pytest.fail(f"defend() raised an exception on large damage: {e}")

    def test_zero_damage_defend(self):
        """Defending against zero damage should not crash."""
        c = make_character()
        initial_health = c.health
        c.defend(0.0)
        assert c.health <= initial_health

    def test_defend_reduces_health_proportionally(self):
        """Larger damage should reduce health more than smaller damage."""
        c1 = make_character()
        c2 = make_character()
        c1.defend(10.0)
        c2.defend(40.0)
        assert c2.health < c1.health

    def test_defend_multiple_times_accumulates(self):
        """Multiple calls to defend() should keep reducing health."""
        c = make_character()
        c.defend(10.0)
        health_after_first = c.health
        c.defend(10.0)
        assert c.health < health_after_first


# ============================================================
# Warrior, Mage, Rogue constructors and is-a — 6 points
# ============================================================

class TestSubclassConstructors:

    def test_warrior_is_character(self):
        """Warrior should be an instance of Character."""
        w = make_warrior()
        assert isinstance(w, Character)

    def test_mage_is_character(self):
        """Mage should be an instance of Character."""
        m = make_mage()
        assert isinstance(m, Character)

    def test_rogue_is_character(self):
        """Rogue should be an instance of Character."""
        r = make_rogue()
        assert isinstance(r, Character)

    def test_warrior_is_serializable(self):
        """Warrior should inherit from Serializable."""
        w = make_warrior()
        assert isinstance(w, Serializable)

    def test_mage_is_serializable(self):
        """Mage should inherit from Serializable."""
        m = make_mage()
        assert isinstance(m, Serializable)

    def test_rogue_is_serializable(self):
        """Rogue should inherit from Serializable."""
        r = make_rogue()
        assert isinstance(r, Serializable)


# ============================================================
# Subclass method overrides — 9 points
# Tests that at least one method behaves differently per subclass
# compared to the base Character class.
# ============================================================

class TestSubclassOverrides:

    def _health_after_defend(self, char_factory, damage):
        """Helper: returns health after defending against given damage."""
        c = char_factory()
        c.defend(damage)
        return c.health

    def test_warrior_defend_differs_from_base(self):
        """Warrior defend() should produce a different result than base Character."""
        damages = [10.0, 20.0, 30.0]
        any_different = any(
            self._health_after_defend(make_warrior, d) !=
            self._health_after_defend(make_character, d)
            for d in damages
        )
        assert any_different, "Warrior.defend() produces identical results to base Character.defend()"

    def test_mage_attack_or_defend_differs_from_base(self):
        """Mage should override at least one combat method differently from base Character."""
        damages = [10.0, 20.0, 30.0]
        defend_differs = any(
            self._health_after_defend(make_mage, d) !=
            self._health_after_defend(make_character, d)
            for d in damages
        )
        # Also check attack produces different damage on target
        target_base = Character("Target", 1, 200.0, 5.0, 0.0)
        target_mage = Character("Target", 1, 200.0, 5.0, 0.0)
        make_character().attack(target_base)
        make_mage().attack(target_mage)
        attack_differs = target_base.health != target_mage.health

        assert defend_differs or attack_differs, "Mage does not override any combat method differently from base Character"

    def test_rogue_attack_or_defend_differs_from_base(self):
        """Rogue should override at least one combat method differently from base Character."""
        damages = [10.0, 20.0, 30.0]
        defend_differs = any(
            self._health_after_defend(make_rogue, d) !=
            self._health_after_defend(make_character, d)
            for d in damages
        )
        target_base = Character("Target", 1, 200.0, 5.0, 0.0)
        target_rogue = Character("Target", 1, 200.0, 5.0, 0.0)
        make_character().attack(target_base)
        make_rogue().attack(target_rogue)
        attack_differs = target_base.health != target_rogue.health

        assert defend_differs or attack_differs, "Rogue does not override any combat method differently from base Character"

    def test_all_three_subclasses_not_identical(self):
        """All three subclasses should not behave identically to each other."""
        target_w = Character("T", 1, 200.0, 5.0, 0.0)
        target_m = Character("T", 1, 200.0, 5.0, 0.0)
        target_r = Character("T", 1, 200.0, 5.0, 0.0)
        make_warrior().attack(target_w)
        make_mage().attack(target_m)
        make_rogue().attack(target_r)
        results = {target_w.health, target_m.health, target_r.health}
        assert len(results) > 1, "All three subclasses produce identical attack results"


# ============================================================
# Serializable.save() and load() — 8 points
# ============================================================

class TestSerializable:

    def test_save_creates_file(self, tmp_path):
        """save() should create a file at the given filepath."""
        w = make_warrior()
        filepath = str(tmp_path / "warrior.txt")
        w.save(filepath)
        assert os.path.exists(filepath)

    def test_save_file_not_empty(self, tmp_path):
        """save() should write content to the file."""
        w = make_warrior()
        filepath = str(tmp_path / "warrior.txt")
        w.save(filepath)
        assert os.path.getsize(filepath) > 0

    def test_load_restores_name(self, tmp_path):
        """load() should restore the name attribute from file."""
        w = make_warrior()
        filepath = str(tmp_path / "warrior.txt")
        w.save(filepath)
        w.name = "Changed"
        w.load(filepath)
        assert w.name == "TestWarrior"

    def test_load_restores_health(self, tmp_path):
        """load() should restore the health attribute from file."""
        w = make_warrior()
        filepath = str(tmp_path / "warrior.txt")
        w.save(filepath)
        w.health = 1.0
        w.load(filepath)
        assert w.health == 100.0

    def test_load_restores_level(self, tmp_path):
        """load() should restore the level attribute from file."""
        w = make_warrior()
        filepath = str(tmp_path / "warrior.txt")
        w.save(filepath)
        w.level = 99
        w.load(filepath)
        assert w.level == 5

    def test_save_load_mage(self, tmp_path):
        """save() and load() should work on Mage as well as Warrior."""
        m = make_mage()
        filepath = str(tmp_path / "mage.txt")
        m.save(filepath)
        m.name = "Changed"
        m.load(filepath)
        assert m.name == "TestMage"


# ============================================================
# load_characters() — 10 points
# ============================================================

class TestLoadCharacters:

    def test_returns_list(self, tmp_path):
        """load_characters() should return a list."""
        csv_file = tmp_path / "test_chars.csv"
        csv_file.write_text(TEST_CSV_CONTENT)
        result = load_characters(str(csv_file))
        assert isinstance(result, list)

    def test_correct_number_of_characters(self, tmp_path):
        """load_characters() should return one object per data row."""
        csv_file = tmp_path / "test_chars.csv"
        csv_file.write_text(TEST_CSV_CONTENT)
        result = load_characters(str(csv_file))
        assert len(result) == 3

    def test_warrior_instantiated_correctly(self, tmp_path):
        """Warrior rows should be instantiated as Warrior objects."""
        csv_file = tmp_path / "test_chars.csv"
        csv_file.write_text(TEST_CSV_CONTENT)
        result = load_characters(str(csv_file))
        warriors = [c for c in result if isinstance(c, Warrior)]
        assert len(warriors) == 1
        assert warriors[0].name == "Aldric"

    def test_mage_instantiated_correctly(self, tmp_path):
        """Mage rows should be instantiated as Mage objects."""
        csv_file = tmp_path / "test_chars.csv"
        csv_file.write_text(TEST_CSV_CONTENT)
        result = load_characters(str(csv_file))
        mages = [c for c in result if isinstance(c, Mage)]
        assert len(mages) == 1
        assert mages[0].name == "Lyssa"

    def test_rogue_instantiated_correctly(self, tmp_path):
        """Rogue rows should be instantiated as Rogue objects."""
        csv_file = tmp_path / "test_chars.csv"
        csv_file.write_text(TEST_CSV_CONTENT)
        result = load_characters(str(csv_file))
        rogues = [c for c in result if isinstance(c, Rogue)]
        assert len(rogues) == 1
        assert rogues[0].name == "Nyx"

    def test_attributes_loaded_correctly(self, tmp_path):
        """Character attributes should match the CSV data."""
        csv_file = tmp_path / "test_chars.csv"
        csv_file.write_text(TEST_CSV_CONTENT)
        result = load_characters(str(csv_file))
        warrior = [c for c in result if isinstance(c, Warrior)][0]
        assert warrior.level == 8
        assert warrior.health == 120.0
        assert warrior.attack_power == 18.0
        assert warrior.defense == 15.0

    def test_all_objects_are_characters(self, tmp_path):
        """All returned objects should be instances of Character."""
        csv_file = tmp_path / "test_chars.csv"
        csv_file.write_text(TEST_CSV_CONTENT)
        result = load_characters(str(csv_file))
        for obj in result:
            assert isinstance(obj, Character)
