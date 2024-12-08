from abc import ABC, abstractmethod
from core.dtos.board_cell import Cell
from core.enums.flags import Flags
from core.enums.piece_type import PieceType


class Action(ABC):
    @property
    def require_flags() -> set[Flags]:
        pass

    @property
    def _board() -> list[list[PieceType]]:
        pass

    def mutate(self, board: list[list[PieceType]], from_cell: Cell, target_cells: list[Cell]) -> list[list[PieceType]]:
        pass

    def validate(self, board: list[list[PieceType]], from_cell: Cell, target_cells: list[Cell]):
        pass
