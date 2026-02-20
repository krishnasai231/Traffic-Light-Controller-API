"""
Command Design Pattern
=======================

Intent: Encapsulate a request as an object, allowing parameterization and queuing.
"""

from abc import ABC, abstractmethod
from typing import List


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class ChangeToGreenCommand(Command):
    def __init__(self, light: 'TrafficLight'):
        self.light = light
        self.previous_state = None

    def execute(self) -> None:
        self.previous_state = self.light.state
        self.light.state = "GREEN"
        print(f"   Changed to GREEN")

    def undo(self) -> None:
        self.light.state = self.previous_state
        print(f"   Undid: Restored to {self.previous_state}")


class TrafficLight:
    def __init__(self):
        self.state = "RED"


class TrafficController:
    def __init__(self):
        self.history: List[Command] = []

    def execute_command(self, command: Command):
        command.execute()
        self.history.append(command)

    def undo_last(self):
        if self.history:
            command = self.history.pop()
            command.undo()


def demonstrate_command():
    print("\n" + "="*70)
    print("COMMAND PATTERN DEMONSTRATION")
    print("="*70)

    light = TrafficLight()
    controller = TrafficController()

    print(f"\n1️⃣ Initial state: {light.state}")

    print("\n2️⃣ Execute change to GREEN:")
    cmd = ChangeToGreenCommand(light)
    controller.execute_command(cmd)
    print(f"   Current state: {light.state}")

    print("\n3️⃣ Undo last command:")
    controller.undo_last()
    print(f"   Current state: {light.state}")


if __name__ == "__main__":
    demonstrate_command()
