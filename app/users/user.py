import attrs


@attrs.define(slots=True)
class User:
    id: int = attrs.field(eq=True, hash=True)
    first_name: str = attrs.field(eq=False, hash=False)
    last_name: str = attrs.field(eq=False, hash=False)
    email: str = attrs.field(
        validator=attrs.validators.matches_re(r"^[^@]+@[^@]+\.[^@]+$"),
        eq=False,
        hash=False,
    )

    def sortable_name(self):
        return f"{self.last_name}, {self.first_name}"
