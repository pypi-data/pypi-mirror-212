import pytest

from ..KingdomsAndWarfare.Traits.Trait import Trait


def test_trait():
    name = "traitName"
    description = "This is the trait description."
    new_trait = Trait(name, description)

    assert name == new_trait.name
    assert description == new_trait.description
    assert new_trait.homebrew


def test_trait_from_dict():
    trait_name = "traitName"
    trait_description = "This is the trait description."
    example_dict = {
        "name": trait_name,
        "description": trait_description,
        "homebrew": False,
        "created": "14/10/2009:01:01:01",
    }

    test_trait = Trait.from_dict(example_dict)

    assert test_trait.name == trait_name
    assert test_trait.description == trait_description
    assert not test_trait.homebrew


def test_to_dict():
    test_trait = Trait("Water Breathing", "This unit's breath smells wet.")
    test_trait_dictionary = test_trait.to_dict()
    assert test_trait_dictionary["name"] == "Water Breathing"
    assert test_trait_dictionary["description"] == "This unit's breath smells wet."
    assert test_trait_dictionary["homebrew"] == True


def test_trait_eq():
    trait_a = Trait("A", "A Description")
    trait_b = Trait("A", "A Description")
    assert trait_a == trait_b
    trait_c = Trait("C", "C Description")
    assert trait_a != trait_c
