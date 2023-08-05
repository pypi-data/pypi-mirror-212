import pdb

from ..Traits.Trait import Trait
from .Aerial import Aerial
from .Artillery import Artillery
from .Cavalry import Cavalry
from .Infantry import Infantry
from .Unit import Unit


def unit_from_dict(new_unit_dict: dict) -> "Unit":
    new_unit = None
    new_type = parse_type(new_unit_dict["type"])
    new_name = new_unit_dict["name"]
    new_description = new_unit_dict["description"]
    if new_type == Unit.Type.INFANTRY:
        new_unit = Infantry(new_name, new_description)
    elif new_type == Unit.Type.CAVALRY:
        new_unit = Cavalry(new_name, new_description)
    elif new_type == Unit.Type.ARTILLERY:
        new_unit = Artillery(new_name, new_description)
    elif new_type == Unit.Type.AERIAL:
        new_unit = Aerial(new_name, new_description)
    else:
        raise NoSuchUnitTypeError(
            f"Could not instantiate unit type of {new_type}. \
                                       Expected one of [Infantry, Cavalry, Artillery, Aerial]."
        )
    new_unit.battles = int(new_unit_dict["battles"])
    new_unit.traits = []
    for trait_dict in new_unit_dict["traits"]:
        new_unit.traits.append(Trait.from_dict(trait_dict))
    new_unit.experience = parse_experience(new_unit_dict["experience"])
    new_unit.equipment = parse_equipment(new_unit_dict["equipment"])
    new_unit.tier = new_unit_dict["tier"]
    new_unit.attack = int(new_unit_dict["attack"])
    new_unit.defense = int(new_unit_dict["defense"])
    new_unit.power = int(new_unit_dict["power"])
    new_unit.toughness = int(new_unit_dict["toughness"])
    new_unit.morale = int(new_unit_dict["morale"])
    new_unit.command = int(new_unit_dict["command"])
    new_unit.damage = int(new_unit_dict["damage"])
    new_unit.attacks = int(new_unit_dict["attacks"])
    new_unit.ancestry = new_unit_dict["ancestry"]
    return new_unit


def parse_type(type_string: str) -> Unit.Type:
    if len(type_string) == 1:
        type_int = int(type_string)
        if type_int < 1 or type_int > 4:
            raise NoSuchUnitTypeError()
        return Unit.Type(type_int)
    type_name = type_string.upper().replace("TYPE.", "")
    if type_name not in ["INFANTRY", "ARTILLERY", "AERIAL", "CAVALRY"]:
        raise NoSuchUnitTypeError()
    return Unit.Type[type_name]


def parse_experience(experience_string: str) -> Unit.Experience:
    if len(experience_string) == 1:
        type_int = int(experience_string)
        if type_int < 1 or type_int > 5:
            raise NoSuchUnitExperienceError()
        return Unit.Experience(type_int)
    type_name = experience_string.upper().replace("EXPERIENCE.", "")
    if type_name not in ["LEVIES", "REGULAR", "VETERAN", "ELITE", "SUPER_ELITE"]:
        raise NoSuchUnitExperienceError()
    return Unit.Experience[type_name]


def parse_equipment(equipment_string: str) -> Unit.Equipment:
    if len(equipment_string) == 1:
        type_int = int(equipment_string)
        if type_int < 1 or type_int > 4:
            raise NoSuchUnitEquipmentError()
        return Unit.Equipment(type_int)
    type_name = equipment_string.upper().replace("EQUIPMENT.", "")
    if type_name not in ["LIGHT", "MEDIUM", "HEAVY", "SUPER_HEAVY"]:
        raise NoSuchUnitEquipmentError()
    return Unit.Equipment[type_name]


class UnitError(Exception):
    pass


class NoSuchUnitTypeError(UnitError):
    pass


class NoSuchUnitExperienceError(UnitError):
    pass


class NoSuchUnitEquipmentError(UnitError):
    pass
