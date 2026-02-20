"""
Factory  Design 
==============================

Intent: Define an interface for creating objects, letting subclasses decide 
which class to instantiate.

Use Case: Create different types of traffic lights based on direction or configuration.

Real-world examples:
- Document readers (PDF, Word, Excel)
- Database connections (MySQL, PostgreSQL, MongoDB)
- UI components (Button, TextField, Checkbox)
"""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict


class LightColor(Enum):
    """Traffic light color states."""
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


class TrafficLight(ABC):
    """Abstract traffic light interface."""

    def __init__(self, direction: str):
        self.direction = direction
        self.color = LightColor.RED

    @abstractmethod
    def get_duration(self) -> int:
        """Return duration in seconds for this light type."""
        pass

    @abstractmethod
    def get_sequence(self) -> list[LightColor]:
        """Return the sequence of colors for this light."""
        pass

    def display_info(self):
        """Display light information."""
        print(f"  Direction: {self.direction}")
        print(f"  Current color: {self.color.value}")
        print(f"  Duration: {self.get_duration()}s")
        print(f"  Sequence: {' → '.join(c.value for c in self.get_sequence())}")


class VehicleLight(TrafficLight):
    """Standard vehicle traffic light."""

    def get_duration(self) -> int:
        return 60  # 60 seconds green

    def get_sequence(self) -> list[LightColor]:
        return [LightColor.GREEN, LightColor.YELLOW, LightColor.RED]


class PedestrianLight(TrafficLight):
    """Pedestrian crossing light."""

    def get_duration(self) -> int:
        return 30  # 30 seconds to cross

    def get_sequence(self) -> list[LightColor]:
        return [LightColor.GREEN, LightColor.RED]  # No yellow for pedestrians


class EmergencyLight(TrafficLight):
    """Emergency vehicle priority light."""

    def get_duration(self) -> int:
        return 120  # 2 minutes for emergency vehicles

    def get_sequence(self) -> list[LightColor]:
        return [LightColor.GREEN]  # Always green for emergency


class ArrowLight(TrafficLight):
    """Turn arrow light."""

    def get_duration(self) -> int:
        return 20  # 20 seconds for turn

    def get_sequence(self) -> list[LightColor]:
        return [LightColor.GREEN, LightColor.YELLOW, LightColor.RED]


class TrafficLightFactory:
    """
    Factory for creating different types of traffic lights.

    This factory encapsulates the creation logic, making it easy to:
    - Add new light types without modifying existing code
    - Configure lights based on intersection requirements
    - Ensure consistent light creation
    """

    _light_types: Dict[str, type] = {
        "vehicle": VehicleLight,
        "pedestrian": PedestrianLight,
        "emergency": EmergencyLight,
        "arrow": ArrowLight,
    }

    @classmethod
    def create_light(cls, light_type: str, direction: str) -> TrafficLight:
        """
        Create a traffic light of the specified type.

        Args:
            light_type: Type of light ("vehicle", "pedestrian", "emergency", "arrow")
            direction: Direction (e.g., "NORTH", "SOUTH", "EAST", "WEST")

        Returns:
            TrafficLight instance

        Raises:
            ValueError: If light_type is not supported
        """
        light_class = cls._light_types.get(light_type.lower())
        if light_class is None:
            raise ValueError(
                f"Unknown light type: {light_type}. "
                f"Supported types: {list(cls._light_types.keys())}"
            )
        return light_class(direction)

    @classmethod
    def register_light_type(cls, name: str, light_class: type):
        """Register a new light type (extension point)."""
        cls._light_types[name.lower()] = light_class

    @classmethod
    def get_supported_types(cls) -> list[str]:
        """Return list of supported light types."""
        return list(cls._light_types.keys())


def demonstrate_factory():
    """Demonstrate factory method pattern."""
    print("\n" + "="*70)
    print("FACTORY METHOD PATTERN DEMONSTRATION")
    print("="*70)

    factory = TrafficLightFactory()

    print("\n📋 Supported light types:", factory.get_supported_types())

    # Create different types of lights
    lights = [
        ("vehicle", "NORTH"),
        ("pedestrian", "NORTH_CROSSING"),
        ("arrow", "NORTH_LEFT"),
        ("emergency", "EMERGENCY_LANE"),
    ]

    print("\n🏭 Creating lights using factory:\n")

    for light_type, direction in lights:
        print(f"Creating {light_type.upper()} light for {direction}:")
        light = factory.create_light(light_type, direction)
        light.display_info()
        print()

    
if __name__ == "__main__":
    demonstrate_factory()
