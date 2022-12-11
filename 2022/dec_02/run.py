from dataclasses import dataclass
from enum import Enum


class Outcome(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6

    @classmethod
    def from_str(cls, s: str):
        return {
            "x": cls.LOSS,
            "y": cls.DRAW,
            "z": cls.WIN,
        }.get(s.lower())


class GameMove(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @classmethod
    def from_str(cls, s: str):
        return {
            "a": cls.ROCK,
            "b": cls.PAPER,
            "c": cls.SCISSORS,
            "x": cls.ROCK,
            "y": cls.PAPER,
            "z": cls.SCISSORS,
        }.get(s.lower())


@dataclass
class Round:
    opponent: GameMove
    # move: GameMove
    outcome: Outcome

    @property
    def score(self) -> int:
        winning_play = {
            GameMove.ROCK: GameMove.SCISSORS,
            GameMove.PAPER: GameMove.ROCK,
            GameMove.SCISSORS: GameMove.PAPER,
        }

        if self.outcome == Outcome.DRAW:
            move = self.opponent
        elif self.outcome == Outcome.LOSS:
            move = winning_play.get(self.opponent)
        else:
            move = {v: k for k, v in winning_play.items()}.get(self.opponent)

        # if self.move == self.opponent:
        #     outcome = Outcome.DRAW
        # else:
        #     outcome = (
        #         Outcome.WIN
        #         if winning_play.get(self.move) == self.opponent
        #         else Outcome.LOSS
        #     )

        return int(move.value) + int(self.outcome.value)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        lines = f.readlines()

    rounds = [tuple(s.split()) for s in lines]
    rounds = [
        Round(
            opponent=GameMove.from_str(r[0]),
            outcome=Outcome.from_str(r[1]),
        )
        for r in rounds
    ]
    # print(rounds[:5])
    # print(rounds[0], rounds[0].score)
    print(sum([round.score for round in rounds]))
