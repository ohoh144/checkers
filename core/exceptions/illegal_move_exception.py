
class IllegalMoveException(Exception):
    def __init__(self, message: str):
        super().__init__(self.message,
                         f"Illegal move - {message}")
