class ExceptionAsyncDB(Exception):

    def __init__(self, message) -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message

    def __repr__(self) -> str:
        return f"<{type(self)}>: {self.message}"
