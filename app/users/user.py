from typing import override
import attrs


@attrs.define(slots=True, eq=False)
class User:
    id: int
    first_name: str
    last_name: str
    email: str = attrs.field(
        validator=attrs.validators.matches_re(r"^[^@]+@[^@]+\.[^@]+$"),
    )

    @override
    def __eq__(self, other: object):
        if isinstance(other, User):
            return self.id == other.id

        return NotImplemented

    def sortable_name(self):
        return f"{self.last_name}, {self.first_name}"
