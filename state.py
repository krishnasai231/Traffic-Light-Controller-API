"""
State Design Pattern
====================

Intent: Allow an object to alter its behavior when its internal state changes.
"""

from abc import ABC, abstractmethod


class TrafficLightState(ABC):
    @abstractmethod
    def handle(self, context: 'TrafficLight') -> None:
        pass


class RedState(TrafficLightState):
    def handle(self, context: 'TrafficLight') -> None:
        print("🔴 RED - Stop!")
        context.state = GreenState()


class YellowState(TrafficLightState):
    def handle(self, context: 'TrafficLight') -> None:
        print("🟡 YELLOW - Prepare to stop")
        context.state = RedState()


class GreenState(TrafficLightState):
    def handle(self, context: 'TrafficLight') -> None:
        print("🟢 GREEN - Go!")
        context.state = YellowState()


class TrafficLight:
    def __init__(self):
        self.state = RedState()

    def change(self):
        self.state.handle(self)


def demonstrate_state():
    print("\n" + "="*70)
    print("STATE PATTERN DEMONSTRATION")
    print("="*70)

    light = TrafficLight()
    for i in range(6):
        print(f"\nTransition {i+1}:")
        light.change()


if __name__ == "__main__":
    demonstrate_state()
