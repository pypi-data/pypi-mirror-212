import pytest

from ..KingdomsAndWarfare.Units.Aerial import Aerial
from ..KingdomsAndWarfare.Units.Unit import Unit


def test_aerial():
    splonks_aerial = Aerial("splonks aerial", "splonks_aerial riding rockinghorses.")
    assert splonks_aerial.name == "splonks aerial"
    assert splonks_aerial.experience == Unit.Experience.REGULAR
    assert splonks_aerial.type == Unit.Type.AERIAL


def test_aerial_level_up():
    teddy_bear_aerial = Aerial("Teddy Bear aerial", "Teddy Bears riding rockinghorses.")
    teddy_bear_aerial.attack = 0
    teddy_bear_aerial.defense = 10
    teddy_bear_aerial.morale = 0
    teddy_bear_aerial.command = 0
    assert teddy_bear_aerial.experience == Unit.Experience.REGULAR
    teddy_bear_aerial.level_up()
    # assert stats were changed by level up correctly
    # magic numbers provided by table from MCDM K&W page 99
    assert teddy_bear_aerial.attacks == 1
    assert teddy_bear_aerial.attack == 1
    assert teddy_bear_aerial.defense == 11
    assert teddy_bear_aerial.morale == 1
    assert teddy_bear_aerial.command == 2
    assert teddy_bear_aerial.experience == Unit.Experience.VETERAN
    teddy_bear_aerial.level_up()
    assert teddy_bear_aerial.attacks == 2
    assert teddy_bear_aerial.attack == 2
    assert teddy_bear_aerial.defense == 12
    assert teddy_bear_aerial.morale == 2
    assert teddy_bear_aerial.command == 4
    assert teddy_bear_aerial.experience == Unit.Experience.ELITE
    teddy_bear_aerial.level_up()
    assert teddy_bear_aerial.attacks == 2
    assert teddy_bear_aerial.attack == 3
    assert teddy_bear_aerial.defense == 13
    assert teddy_bear_aerial.morale == 3
    assert teddy_bear_aerial.command == 6
    assert teddy_bear_aerial.experience == Unit.Experience.SUPER_ELITE


def test_aerial_upgrade():
    test_aerial = Aerial("Test", "Armed with personality tests.")
    test_aerial.power = 0
    test_aerial.toughness = 10
    assert test_aerial.equipment == Unit.Equipment.LIGHT
    test_aerial.upgrade()
    assert test_aerial.equipment == Unit.Equipment.MEDIUM
    assert test_aerial.power == 1
    assert test_aerial.toughness == 11
    assert test_aerial.damage == 1
    test_aerial.upgrade()
    assert test_aerial.equipment == Unit.Equipment.HEAVY
    assert test_aerial.power == 2
    assert test_aerial.toughness == 12
    assert test_aerial.damage == 1
    test_aerial.upgrade()
    assert test_aerial.equipment == Unit.Equipment.SUPER_HEAVY
    assert test_aerial.power == 3
    assert test_aerial.toughness == 13
    assert test_aerial.damage == 2
