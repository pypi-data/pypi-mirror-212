from .Unit import Unit


class Artillery(Unit):
    def __init__(self, name: str, description: str):
        self.type = Unit.Type.ARTILLERY
        super().__init__(name, description)

    def level_up(self) -> None:
        self.attack = self.attack + 2
        self.defense = self.defense + 1
        self.morale = self.morale + 1
        self.command = self.command + 1
        if self.experience == Unit.Experience.REGULAR:
            self.attacks = self.attacks + 1
        super().level_up()

    def level_down(self) -> None:
        self.attack = self.attack - 2
        self.defense = self.defense - 1
        self.morale = self.morale - 1
        self.command = self.command - 1
        if self.experience == Unit.Experience.VETERAN:
            self.attacks = self.attacks - 1
        super().level_down()

    def upgrade(self) -> None:
        """Upgrade a unit's equipment bonuses. This is usually done by spending gold.
        Throws a CannotUpgradeError if trying to upgrade past Super Heavy equipment."""
        self.power = self.power + 1
        self.toughness = self.toughness + 1
        super().upgrade()

    def downgrade(self) -> None:
        """Downgrade a unit's equipment bonuses. This is usualy the 'undo' function for upgrading.
        Throws a CannotUpgradeError if trying to downgrade past Light equipment."""
        self.power = self.power - 1
        self.toughness = self.toughness - 1
        super().downgrade()
