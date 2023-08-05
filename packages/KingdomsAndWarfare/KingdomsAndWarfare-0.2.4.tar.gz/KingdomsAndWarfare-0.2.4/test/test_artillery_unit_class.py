import pytest

from ..KingdomsAndWarfare.Units.Artillery import Artillery
from ..KingdomsAndWarfare.Units.Unit import Unit


def test_artillery():
    splonks_artillery = Artillery(
        "splonks_artillery artillery", "splonks_artillery with bottle rockets"
    )
    assert splonks_artillery.name == "splonks_artillery artillery"
    assert splonks_artillery.experience == Unit.Experience.REGULAR
    assert splonks_artillery.type == Unit.Type.ARTILLERY


def test_artillery_level_up():
    teddy_bear_artillery = Artillery("Teddy Bear artillery", "Teddy Bears with Toy Swords")
    teddy_bear_artillery.attack = 0
    teddy_bear_artillery.defense = 10
    teddy_bear_artillery.morale = 0
    teddy_bear_artillery.command = 0
    assert teddy_bear_artillery.experience == Unit.Experience.REGULAR
    teddy_bear_artillery.level_up()
    # assert stats were changed by level up correctly
    # magic numbers provided by table from MCDM K&W page 99
    assert teddy_bear_artillery.attacks == 2
    assert teddy_bear_artillery.attack == 2
    assert teddy_bear_artillery.defense == 11
    assert teddy_bear_artillery.morale == 1
    assert teddy_bear_artillery.command == 1
    assert teddy_bear_artillery.experience == Unit.Experience.VETERAN
    teddy_bear_artillery.level_up()
    assert teddy_bear_artillery.attacks == 2
    assert teddy_bear_artillery.attack == 4
    assert teddy_bear_artillery.defense == 12
    assert teddy_bear_artillery.morale == 2
    assert teddy_bear_artillery.command == 2
    assert teddy_bear_artillery.experience == Unit.Experience.ELITE
    teddy_bear_artillery.level_up()
    assert teddy_bear_artillery.attacks == 2
    assert teddy_bear_artillery.attack == 6
    assert teddy_bear_artillery.defense == 13
    assert teddy_bear_artillery.morale == 3
    assert teddy_bear_artillery.command == 3
    assert teddy_bear_artillery.experience == Unit.Experience.SUPER_ELITE


def test_artillery_upgrade():
    test_artillery = Artillery("Test", "Armed with personality tests.")
    test_artillery.power = 0
    test_artillery.toughness = 10
    assert test_artillery.equipment == Unit.Equipment.LIGHT
    test_artillery.upgrade()
    assert test_artillery.equipment == Unit.Equipment.MEDIUM
    assert test_artillery.power == 1
    assert test_artillery.toughness == 11
    test_artillery.upgrade()
    assert test_artillery.equipment == Unit.Equipment.HEAVY
    assert test_artillery.power == 2
    assert test_artillery.toughness == 12
    test_artillery.upgrade()
    assert test_artillery.equipment == Unit.Equipment.SUPER_HEAVY
    assert test_artillery.power == 3
    assert test_artillery.toughness == 13
