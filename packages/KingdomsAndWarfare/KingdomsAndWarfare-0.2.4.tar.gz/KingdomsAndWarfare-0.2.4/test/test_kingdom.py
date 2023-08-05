from ..KingdomsAndWarfare.Kingdoms.Kingdom import Kingdom


def test_kingdom():
    kingdom_name = "kingdomName"
    kingdom_description = "blah."
    kingdom = Kingdom(kingdom_name, kingdom_description)

    assert kingdom.name == kingdom_name
    assert kingdom.description == kingdom_description
