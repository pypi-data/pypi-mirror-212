import os
import sys
from abc import ABC


class Command(ABC):
    def clear(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def confirm(self, message: str) -> bool:
        if message:
            message += "\n\n"
        confirmation = input(f"{message}Are you sure you want to proceed? (y/n): ")
        return confirmation.lower() == 'y'

    def abort(self, message: str = "") -> None:
        if message:
            message = f"\n{message.strip()}"

        message = message or ''
        print(f"\033[F\033[K\n🚫 abort {message}")
        
        sys.exit(0)


    def ok(self, message: str = "") -> None:
        if message:
            message = f"\n{message.strip()}"

        message = message or ''
        print(f"\033[F\033[K\n✅ OK {message}")
        sys.exit(0)