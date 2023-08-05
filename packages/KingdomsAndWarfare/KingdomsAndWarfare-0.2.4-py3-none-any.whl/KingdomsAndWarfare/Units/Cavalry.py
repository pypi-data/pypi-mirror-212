from .Unit import Unit


class Cavalry(Unit):
    def __init__(self, name: str, description: str):
        self.type = Unit.Type.CAVALRY
        super().__init__(name, description)

    def level_up(self) -> None:
        self.attack = self.attack + 1
        self.defense = self.defense + 1
        self.morale = self.morale + 1
        self.command = self.command + 2
        if self.experience == Unit.Experience.VETERAN:
            self.attacks = self.attacks + 1
        super().level_up()

    def level_down(self) -> None:
        self.attack = self.attack - 1
        self.defense = self.defense - 1
        self.morale = self.morale - 1
        self.command = self.command - 2
        if self.experience == Unit.Experience.ELITE:
            self.attacks = self.attacks - 1
        super().level_down()

    def upgrade(self) -> None:
        """Upgrade a unit's equipment bonuses. This is usually done by spending gold.
        Throws a CannotUpgradeError if trying to upgrade past Super Heavy equipment."""
        self.power = self.power + 1
        self.toughness = self.toughness + 1
        if self.equipment == Unit.Equipment.HEAVY:
            self.damage = self.damage + 1
        super().upgrade()

    def downgrade(self) -> None:
        """Downgrade a unit's equipment bonuses. This is usualy the 'undo' function for upgrading.
        Throws a CannotUpgradeError if trying to downgrade past Light equipment."""
        self.power = self.power - 1
        self.toughness = self.toughness - 1
        if self.equipment == Unit.Equipment.SUPER_HEAVY:
            self.damage = self.damage - 1
        super().downgrade()
