from typing import Protocol


class logger_type(Protocol):
    def debug(self, text: str) -> None:
        ...

    def info(self, text: str) -> None:
        ...

    def warning(self, text: str) -> None:
        ...

    def error(self, text: str) -> None:
        ...

    def critical(self, text: str) -> None:
        ...

    def traceback(self, text: str) -> None:
        ...

    def contextualise(self, text: str) -> None:
        ...
