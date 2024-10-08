import attrs


@attrs.define(frozen=True)
class Gitmoji:
    """Class that represents a gitmoji."""

    type: str
    icon: str
    code: str
    desc: str

    @property
    def value(self) -> str:
        """The value property."""
        return f"{self.icon} {self.type}"

    @property
    def name(self) -> str:
        """The name property."""
        return f"{self.value}: {self.desc}"
