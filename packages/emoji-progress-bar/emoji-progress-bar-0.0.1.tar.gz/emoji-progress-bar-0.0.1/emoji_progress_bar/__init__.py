from __future__ import annotations


class SlackBusySpinner:
    def __init__(self, timeout: int | None = None):
        self.__progress_bar_index = 0
        self.timeout = timeout

    def __iter__(self):
        return self

    def __next__(self) -> str:
        if self.timeout is not None and self.__progress_bar_index > self.timeout:
            raise StopIteration
        minutes = "30" if self.__progress_bar_index % 2 else ""
        clock_number = (self.__progress_bar_index % 24 // 2) + 1
        emoji = f"clock{clock_number}{minutes}"
        self.__progress_bar_index += 1
        return emoji
