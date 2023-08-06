import dataclasses
from collections.abc import Sequence

@dataclasses.dataclass(kw_only=True)
class Note:
    clues: Sequence[str] = None
    attempted_decipher: Sequence[int] = None
    attempted_interception: Sequence[int] = None
    correct_code: Sequence[int] = None


@dataclasses.dataclass(kw_only=True)
class Game:
    keywords: Sequence[Sequence[str]]
    notesheets: Sequence[list[Note]] = dataclasses.field(default_factory=lambda: [[], []])
     
    def __post_init__(self):
        self.rounds_played = len(self.notesheets[0])
        self.miscommunications = [0, 0]
        self.interceptions = [0, 0]

        for team, notesheet in enumerate(self.notesheets): # may make sense to abstract this to separate method later
            opponent = not team
            for note in notesheet:
                if note.attempted_decipher != note.correct_code:
                    self.miscommunications[team] += 1
                if note.attempted_interception == note.correct_code:
                    self.interceptions[opponent] += 1

