from os import get_terminal_size
from time import sleep
from typing import Any

from noiftimer import Timer


def clear():
    """Erase the current line from the terminal."""
    print(" " * (get_terminal_size().columns - 1), flush=True, end="\r")


def print_in_place(string: str, animate: bool = False, animate_refresh: float = 0.01):
    """Calls to print_in_place will overwrite
    the previous line of text in the terminal
    with the 'string' param.

    :param animate: Will cause the string
    to be printed to the terminal
    one character at a time.

    :param animate_refresh: Number of seconds
    between the addition of characters
    when 'animate' is True."""
    clear()
    string = str(string)
    width = get_terminal_size().columns
    string = string[: width - 2]
    if animate:
        for i in range(len(string)):
            print(f"{string[:i+1]}", flush=True, end=" \r")
            sleep(animate_refresh)
    else:
        print(string, flush=True, end="\r")


def ticker(info: list[str]):
    """Prints info to terminal with
    top and bottom padding so that repeated
    calls print info without showing previous
    outputs from ticker calls.

    Similar visually to print_in_place,
    but for multiple lines."""
    width = get_terminal_size().columns
    info = [str(line)[: width - 1] for line in info]
    height = get_terminal_size().lines - len(info)
    print("\n" * (height * 2), end="")
    print(*info, sep="\n", end="")
    print("\n" * (int((height) / 2)), end="")


class ProgBar:
    """Self incrementing, dynamically sized progress bar.

    Includes an internal timer that starts when this object is created.
    It can be easily added to the progress bar display by adding
    the 'runtime' property to display's prefix or suffix param:

    >>> bar = ProgBar(total=100)
    >>> time.sleep(30)
    >>> bar.display(prefix=bar.runtime)
    >>> "runtime: 30s [_///////////////////]1.00%" """

    def __init__(
        self,
        total: float,
        update_frequency: int = 1,
        fill_ch: str = "_",
        unfill_ch: str = "/",
        width_ratio: float = 0.75,
        new_line_after_completion: bool = True,
        clear_after_completion: bool = False,
    ):
        """:param total: The number of calls to reach 100% completion.

        :param update_frequency: The progress bar will only update once every this number of calls to display().
        The larger the value, the less performance impact ProgBar has on the loop in which it is called.
        e.g.
        >>> bar = ProgBar(100, update_frequency=10)
        >>> for _ in range(100):
        >>>     bar.display()

        ^The progress bar in the terminal will only update once every ten calls, going from 0%->100% in 10% increments.
        Note: If 'total' is not a multiple of 'update_frequency', the display will not show 100% completion when the loop finishes.

        :param fill_ch: The character used to represent the completed part of the bar.

        :param unfill_ch: The character used to represent the uncompleted part of the bar.

        :param width_ratio: The width of the progress bar relative to the width of the terminal window.

        :param new_line_after_completion: Make a call to print() once self.counter >= self.total.

        :param clear_after_completion: Make a call to printbuddies.clear() once self.counter >= self.total.

        Note: if new_line_after_completion and clear_after_completion are both True, the line will be cleared
        then a call to print() will be made."""
        self.total = total
        self.update_frequency = update_frequency
        self.fill_ch = fill_ch[0]
        self.unfill_ch = unfill_ch[0]
        self.width_ratio = width_ratio
        self.new_line_after_completion = new_line_after_completion
        self.clear_after_completion = clear_after_completion
        self.reset()
        self.with_context = False

    def __enter__(self):
        self.with_context = True
        return self

    def __exit__(self, *args, **kwargs):
        if self.clear_after_completion:
            clear()
        else:
            print()

    def reset(self):
        self.counter = 1
        self.percent = ""
        self.prefix = ""
        self.suffix = ""
        self.filled = ""
        self.unfilled = ""
        self.bar = ""
        self.timer = Timer(subsecond_resolution=False).start()

    @property
    def runtime(self) -> str:
        return f"runtime:{self.timer.elapsed_str}"

    def get_percent(self) -> str:
        """Returns the percentage complete to two decimal places
        as a string without the %."""
        percent = str(round(100.0 * self.counter / self.total, 2))
        if len(percent.split(".")[1]) == 1:
            percent = percent + "0"
        if len(percent.split(".")[0]) == 1:
            percent = "0" + percent
        return percent

    def _prepare_bar(self):
        self.terminal_width = get_terminal_size().columns - 1
        bar_length = int(self.terminal_width * self.width_ratio)
        progress = int(bar_length * min(self.counter / self.total, 1.0))
        self.filled = self.fill_ch * progress
        self.unfilled = self.unfill_ch * (bar_length - progress)
        self.percent = self.get_percent()
        self.bar = self.get_bar()

    def _trim_bar(self):
        original_width = self.width_ratio
        while len(self.bar) > self.terminal_width and self.width_ratio > 0:
            self.width_ratio -= 0.01
            self._prepare_bar()
        self.width_ratio = original_width

    def get_bar(self):
        return f"{self.prefix}{' '*bool(self.prefix)}[{self.filled}{self.unfilled}]-{self.percent}% {self.suffix}"

    def display(
        self,
        prefix: str = "",
        suffix: str = "",
        counter_override: float | None = None,
        total_override: float | None = None,
        return_object: Any | None = None,
    ) -> Any:
        """Writes the progress bar to the terminal.

        :param prefix: String affixed to the front of the progress bar.

        :param suffix: String appended to the end of the progress bar.

        :param counter_override: When an externally incremented completion counter is needed.

        :param total_override: When an externally controlled bar total is needed.

        :param return_object: An object to be returned by display().

        Allows display() to be called within a comprehension:

        e.g.

        >>> bar = ProgBar(10)
        >>> def square(x: int | float)->int|float:
        >>>     return x * x
        >>> myList = [bar.display(return_object=square(i)) for i in range(10)]
        >>> <progress bar gets displayed>
        >>> myList
        >>> [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]"""
        if not self.timer.started:
            self.timer.start()
        if counter_override is not None:
            self.counter = counter_override
        if total_override:
            self.total = total_override
        # Don't wanna divide by 0 there, pal
        while self.total <= 0:
            self.total += 1
        if self.counter % self.update_frequency == 0:
            self.prefix = prefix
            self.suffix = suffix
            self._prepare_bar()
            self._trim_bar()
            pad = " " * (self.terminal_width - len(self.bar))
            width = get_terminal_size().columns
            print(f"{self.bar}{pad}"[: width - 2], flush=True, end="\r")
        if self.counter >= self.total:
            self.timer.stop()
            if not self.with_context:
                if self.clear_after_completion:
                    clear()
                if self.new_line_after_completion:
                    print()
        self.counter += 1
        return return_object


class Spinner:
    """Prints one of a sequence of characters in order everytime display() is called.

    The display function writes the new character to the same line, overwriting the previous character.

    The sequence will be cycled through indefinitely.

    If used as a context manager, the last printed character will be cleared upon exiting.
    """

    def __init__(
        self, sequence: list[str] = ["/", "-", "\\"], width_ratio: float = 0.25
    ):
        """
        :param sequence: Override the built in spin sequence.

        :param width: The fractional amount of the terminal for characters to move across."""
        self._base_sequence = sequence
        self.width_ratio = width_ratio
        self.sequence = self._base_sequence

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        clear()

    @property
    def width_ratio(self) -> float:
        return self._width_ratio

    @width_ratio.setter
    def width_ratio(self, ratio: float):
        self._width_ratio = ratio
        self._update_width()

    def _update_width(self):
        self._current_terminal_width = get_terminal_size().columns
        self._width = int((self._current_terminal_width - 1) * self.width_ratio)

    @property
    def sequence(self) -> list[Any]:
        return self._sequence

    @sequence.setter
    def sequence(self, character_list: list[Any]):
        self._sequence = [
            ch.rjust(i + j)
            for i in range(1, self._width, len(character_list))
            for j, ch in enumerate(character_list)
        ]
        self._sequence += self._sequence[::-1]

    def _get_next(self) -> str:
        """Pop the first element of self._sequence, append it to the end, and return the element."""
        ch = self.sequence.pop(0)
        self.sequence.append(ch)
        return ch

    def display(self):
        """Print the next character in the sequence."""
        if get_terminal_size().columns != self._current_terminal_width:
            self._update_width()
            self.sequence = self._base_sequence
        print_in_place(self._get_next())
