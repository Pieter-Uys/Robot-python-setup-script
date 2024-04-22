import itertools
import threading
import time
import sys
from colorama import Fore, Style

class Loader:
    def __init__(self, desc="Loading...", end="Done!", timeout=0.1, color=Fore.YELLOW):
        self.desc = desc
        self.end = end
        self.timeout = timeout
        self.color = color

        self._thread = threading.Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in itertools.cycle(self.steps):
            if self.done:
                break
            sys.stdout.write(f"\r{self.color}{self.desc} {c}{Style.RESET_ALL}")
            sys.stdout.flush()
            time.sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = 80
        sys.stdout.write("\r" + " " * cols)
        sys.stdout.write(f"\r{Fore.GREEN}{self.end}{Style.RESET_ALL}" + "\n")
        sys.stdout.flush()

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()