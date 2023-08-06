import dataclasses
from collections.abc import Sequence


@dataclasses.dataclass(kw_only=True)
class Game:
    words: Sequence[Sequence[str]]
    winner: int = None # right now, player are represented as integers. It might make sense to use Enum later.
    rounds_played: int = 0
    miscommunications: list[int] = dataclasses.field(default_factory=lambda:[0,0])
    interceptions: list[int] = dataclasses.field(default_factory=lambda:[0,0])

