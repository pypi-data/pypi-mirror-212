from abc import ABC


class Utils(ABC):
    __error__: Exception | None = None

    @property
    def Error(self) -> Exception | None:
        return self.__error__

    def is_error(self, err: Exception | None) -> None:
        self.__error__ = err