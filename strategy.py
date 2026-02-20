"""
Strategy Design Pattern
========================

Intent: Define a family of algorithms, encapsulate each one, and make them
interchangeable. Strategy lets the algorithm vary independently from clients.

Use Case: Different traffic light sequencing algorithms (fixed, adaptive, emergency).
"""

from abc import ABC, abstractmethod
from typing import List
from enum import Enum


class LightState(Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class SequencingStrategy(ABC):
    """Abstract strategy for traffic light sequencing."""

    @abstractmethod
    def get_sequence(self) -> List[LightState]:
        """Return the sequence of light states."""
        pass

    @abstractmethod
    def get_duration(self, state: LightState) -> int:
        """Return duration for given state."""
        pass


class FixedTimeStrategy(SequencingStrategy):
    """Fixed-time sequencing (traditional traffic lights)."""

    def get_sequence(self) -> List[LightState]:
        return [LightState.GREEN, LightState.YELLOW, LightState.RED]

    def get_duration(self, state: LightState) -> int:
        durations = {
            LightState.GREEN: 60,
            LightState.YELLOW: 5,
            LightState.RED: 65
        }
        return durations[state]


class AdaptiveStrategy(SequencingStrategy):
    """Adaptive sequencing based on traffic sensors."""

    def __init__(self, traffic_level: str = "medium"):
        self.traffic_level = traffic_level

    def get_sequence(self) -> List[LightState]:
        return [LightState.GREEN, LightState.YELLOW, LightState.RED]

    def get_duration(self, state: LightState) -> int:
        if self.traffic_level == "heavy":
            durations = {LightState.GREEN: 90, LightState.YELLOW: 5, LightState.RED: 45}
        elif self.traffic_level == "light":
            durations = {LightState.GREEN: 30, LightState.YELLOW: 3, LightState.RED: 30}
        else:  # medium
            durations = {LightState.GREEN: 60, LightState.YELLOW: 5, LightState.RED: 60}
        return durations[state]


class EmergencyStrategy(SequencingStrategy):
    """Emergency mode - keep green for emergency vehicles."""

    def get_sequence(self) -> List[LightState]:
        return [LightState.GREEN]  # Stay green

    def get_duration(self, state: LightState) -> int:
        return 999999  # Indefinite


class TrafficLightContext:
    """Context that uses a sequencing strategy."""

    def __init__(self, strategy: SequencingStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SequencingStrategy):
        """Change strategy at runtime."""
        print(f"   Switching to: {strategy.__class__.__name__}")
        self._strategy = strategy

    def execute_cycle(self):
        """Execute one complete light cycle."""
        print(f"   Executing {self._strategy.__class__.__name__}:")
        for state in self._strategy.get_sequence():
            duration = self._strategy.get_duration(state)
            print(f"      {state.value}: {duration}s")


def demonstrate_strategy():
    """Demonstrate strategy pattern."""
    print("\n" + "="*70)
    print("STRATEGY PATTERN DEMONSTRATION")
    print("="*70)

    controller = TrafficLightContext(FixedTimeStrategy())

    print("\n1️⃣ Fixed Time Strategy:")
    controller.execute_cycle()

    print("\n2️⃣ Adaptive Strategy (Heavy Traffic):")
    controller.set_strategy(AdaptiveStrategy("heavy"))
    controller.execute_cycle()

    print("\n3️⃣ Emergency Strategy:")
    controller.set_strategy(EmergencyStrategy())
    controller.execute_cycle()


if __name__ == "__main__":
    demonstrate_strategy()
