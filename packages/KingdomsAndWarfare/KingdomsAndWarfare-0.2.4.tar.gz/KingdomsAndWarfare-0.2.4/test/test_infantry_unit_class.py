import pytest

from ..KingdomsAndWarfare.Units.Infantry import Infantry
from ..KingdomsAndWarfare.Units.Unit import Unit


def test_infantry():
    splonks_infantry = Infantry("splonks_infantry Infantry", "splonks_infantry with butterknives")
    assert splonks_infantry.name == "splonks_infantry Infantry"
    assert splonks_infantry.experience == Unit.Experience.REGULAR
    assert splonks_infantry.type == Unit.Type.INFANTRY


def test_infantry_level_up():
    teddy_bear_infantry = Infantry("Teddy Bear Infantry", "Teddy Bears with Toy Swords")
    teddy_bear_infantry.attack = 0
    teddy_bear_infantry.defense = 10
    teddy_bear_infantry.morale = 0
    teddy_bear_infantry.command = 0
    assert teddy_bear_infantry.experience == Unit.Experience.REGULAR
    teddy_bear_infantry.level_up()
    # assert stats were changed by level up correctly
    # magic numbers provided by table from MCDM K&W page 99
    assert teddy_bear_infantry.attacks == 1
    assert teddy_bear_infantry.attack == 1
    assert teddy_bear_infantry.defense == 12
    assert teddy_bear_infantry.morale == 2
    assert teddy_bear_infantry.command == 1
    assert teddy_bear_infantry.experience == Unit.Experience.VETERAN
    teddy_bear_infantry.level_up()
    assert teddy_bear_infantry.attacks == 2
    assert teddy_bear_infantry.attack == 2
    assert teddy_bear_infantry.defense == 14
    assert teddy_bear_infantry.morale == 4
    assert teddy_bear_infantry.command == 1
    assert teddy_bear_infantry.experience == Unit.Experience.ELITE
    teddy_bear_infantry.level_up()
    assert teddy_bear_infantry.attacks == 2
    assert teddy_bear_infantry.attack == 3
    assert teddy_bear_infantry.defense == 16
    assert teddy_bear_infantry.morale == 6
    assert teddy_bear_infantry.command == 2
    assert teddy_bear_infantry.experience == Unit.Experience.SUPER_ELITE


def test_infantry_upgrade():
    test_infantry = Infantry("Test", "Armed with personality tests.")
    test_infantry.power = 0
    test_infantry.toughness = 10
    test_infantry.damage = 1
    assert test_infantry.equipment == Unit.Equipment.LIGHT
    test_infantry.upgrade()
    assert test_infantry.equipment == Unit.Equipment.MEDIUM
    assert test_infantry.power == 2
    assert test_infantry.toughness == 12
    assert test_infantry.damage == 1
    test_infantry.upgrade()
    assert test_infantry.equipment == Unit.Equipment.HEAVY
    assert test_infantry.power == 4
    assert test_infantry.toughness == 14
    assert test_infantry.damage == 1
    test_infantry.upgrade()
    assert test_infantry.equipment == Unit.Equipment.SUPER_HEAVY
    assert test_infantry.power == 6
    assert test_infantry.toughness == 16
    assert test_infantry.damage == 2
