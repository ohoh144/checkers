from core.actions.action import Action
from core.actions.burn import Burn
from core.actions.king_attack_move import KingAttackMove
from core.actions.king_move import KingMove
from core.actions.simple_attack_move import SimpleAttackMove
from core.actions.simple_move import SimpleMove
from core.exceptions.illegal_move_exception import IllegalMoveException
from core.enums.game_state import GameState
from core.dtos.board_cell import Cell
from core.enums.piece_type import PieceType
from core.enums.flags import Flags
from core.utils.register_actions import register_action


@register_action("simple_move", SimpleMove)
@register_action("simple_attack_move", SimpleAttackMove)
@register_action("king_move", KingMove)
@register_action("king_attack_move", KingAttackMove)
@register_action("burn", Burn, run_always=True)
class Game():
    _on_turn_actions: dict[str, Action]
    _on_move_actions: dict[str, Action]
    _flags: set[Flags]
    _game_state: GameState
    _board: list[list[PieceType]]

    def __init__(self, *flags: tuple[Flags]):
        self._flags = set(flags)

    def get_state(self):
        return self._game_state

    def move(self, action: str, from_cell: Cell, *target_cells: tuple[Cell]):
        self._assert_can_move(from_cell)
        self._dispatch(action, from_cell, target_cells)
        self._change_state()

    def _change_state(self):
        white_count = 0
        black_count = 0

        for row in self._board:
            for piece in row:
                if piece in (PieceType.WHITE, PieceType.WHITE_KING):
                    white_count += 1
                elif piece in (PieceType.BLACK, PieceType.BLACK_KING):
                    black_count += 1

        if white_count == 0:
            self._game_state = GameState.BLACK_WON

        if black_count == 0:
            self._game_state = GameState.WHITE_WON

        self._game_state = GameState.BLACK_TURN \
            if self._game_state == GameState.WHITE_TURN \
            else GameState.WHITE_TURN

    def _assert_can_move(self, from_cell: Cell):
        if self._game_state in (GameState.WHITE_WON, GameState.BLACK_WON):
            turn = 'white' if self._game_state == GameState.WHITE_WON else 'black'
            raise IllegalMoveException(f"""Game over, {turn} player won.""")

        if (self._game_state == GameState.WHITE_TURN) \
                and (self._board[from_cell.x][from_cell.y] not in (PieceType.WHITE, PieceType.WHITE_KING)):
            raise IllegalMoveException("white turn but black played")

        if (self._game_state == GameState.BLACK_TURN) \
                and (self._board[from_cell.x][from_cell.y] not in (PieceType.BLACK, PieceType.BLACK_KING)):
            raise IllegalMoveException("black turn but white played")

    def _dispatch(self, action: str, from_cell: Cell, target_cells: list[Cell]):
        for _, act in self._on_turn_actions.items():
            act.validate(self._board, from_cell, target_cells)
            self._board = act.mutate(self._board, from_cell, target_cells)

        if not (curr_act := self._on_move_actions.get(action, None)):
            raise IllegalMoveException("unsupported move")

        curr_act.validate(self._board, from_cell, target_cells)
        self._board = curr_act.mutate(self._board, from_cell, target_cells)
