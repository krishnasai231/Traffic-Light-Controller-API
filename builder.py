"""
Builder Design 
=======================

Intent: Separate the construction of a complex object from its representation,
allowing the same construction process to create different representations.

Use Case: Build complex traffic light sequences with many configuration options.

Real-world examples:
- SQL query builders
- HTTP request builders
- Document/Report builders
- Configuration objects
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class Direction(Enum):
    """Traffic directions."""
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


class SequenceMode(Enum):
    """Sequence operation modes."""
    NORMAL = "NORMAL"
    RUSH_HOUR = "RUSH_HOUR"
    NIGHT = "NIGHT"
    EMERGENCY = "EMERGENCY"


@dataclass
class LightTiming:
    """Timing configuration for a single light state."""
    green_duration: int
    yellow_duration: int
    red_duration: int


@dataclass
class TrafficSequence:
    """Complete traffic light sequence configuration."""
    directions: List[Direction]
    timing: LightTiming
    mode: SequenceMode
    pedestrian_enabled: bool
    pedestrian_duration: int
    emergency_override: bool
    sensor_enabled: bool
    log_events: bool

    def display(self):
        """Display sequence configuration."""
        print(f"🚦 Traffic Sequence Configuration")
        print(f"   Directions: {', '.join(d.value for d in self.directions)}")
        print(f"   Mode: {self.mode.value}")
        print(f"   Green: {self.timing.green_duration}s, "
              f"Yellow: {self.timing.yellow_duration}s, "
              f"Red: {self.timing.red_duration}s")
        print(f"   Pedestrian: {'Enabled' if self.pedestrian_enabled else 'Disabled'}", end="")
        if self.pedestrian_enabled:
            print(f" ({self.pedestrian_duration}s)")
        else:
            print()
        print(f"   Emergency Override: {'Yes' if self.emergency_override else 'No'}")
        print(f"   Sensor Enabled: {'Yes' if self.sensor_enabled else 'No'}")
        print(f"   Event Logging: {'Yes' if self.log_events else 'No'}")


class TrafficSequenceBuilder:
    """
    Builder for creating complex traffic sequences step by step.

    Advantages:
    - Readable, fluent API
    - Prevents invalid state (required fields enforced)
    - Provides sensible defaults
    - Easy to extend with new options
    """

    def __init__(self):
        """Initialize with default values."""
        self._directions: List[Direction] = []
        self._green_duration: int = 60
        self._yellow_duration: int = 5
        self._red_duration: int = 0  # Calculated
        self._mode: SequenceMode = SequenceMode.NORMAL
        self._pedestrian_enabled: bool = False
        self._pedestrian_duration: int = 30
        self._emergency_override: bool = True
        self._sensor_enabled: bool = False
        self._log_events: bool = True

    def for_directions(self, *directions: Direction) -> 'TrafficSequenceBuilder':
        """Set traffic directions (required)."""
        self._directions = list(directions)
        return self

    def with_timing(self, green: int, yellow: int = 5) -> 'TrafficSequenceBuilder':
        """Set light timing durations."""
        self._green_duration = green
        self._yellow_duration = yellow
        return self

    def in_mode(self, mode: SequenceMode) -> 'TrafficSequenceBuilder':
        """Set operation mode."""
        self._mode = mode
        # Adjust timing based on mode
        if mode == SequenceMode.RUSH_HOUR:
            self._green_duration = max(90, self._green_duration)
        elif mode == SequenceMode.NIGHT:
            self._green_duration = 30
        elif mode == SequenceMode.EMERGENCY:
            self._green_duration = 120
        return self

    def enable_pedestrian(self, duration: int = 30) -> 'TrafficSequenceBuilder':
        """Enable pedestrian crossing."""
        self._pedestrian_enabled = True
        self._pedestrian_duration = duration
        return self

    def disable_emergency_override(self) -> 'TrafficSequenceBuilder':
        """Disable emergency vehicle override."""
        self._emergency_override = False
        return self

    def enable_sensors(self) -> 'TrafficSequenceBuilder':
        """Enable traffic sensors for adaptive timing."""
        self._sensor_enabled = True
        return self

    def disable_logging(self) -> 'TrafficSequenceBuilder':
        """Disable event logging."""
        self._log_events = False
        return self

    def build(self) -> TrafficSequence:
        """
        Build the traffic sequence.

        Raises:
            ValueError: If required fields are missing or invalid.
        """
        # Validation
        if not self._directions:
            raise ValueError("At least one direction must be specified")

        if self._green_duration <= 0:
            raise ValueError("Green duration must be positive")

        # Calculate red duration based on other lights
        # (simplified - in real system would consider all directions)
        self._red_duration = (len(self._directions) - 1) * (
            self._green_duration + self._yellow_duration
        )

        timing = LightTiming(
            green_duration=self._green_duration,
            yellow_duration=self._yellow_duration,
            red_duration=self._red_duration
        )

        return TrafficSequence(
            directions=self._directions,
            timing=timing,
            mode=self._mode,
            pedestrian_enabled=self._pedestrian_enabled,
            pedestrian_duration=self._pedestrian_duration,
            emergency_override=self._emergency_override,
            sensor_enabled=self._sensor_enabled,
            log_events=self._log_events
        )

    def reset(self) -> 'TrafficSequenceBuilder':
        """Reset builder to default state."""
        self.__init__()
        return self


def demonstrate_builder():
    """Demonstrate builder pattern."""
    print("\n" + "="*70)
    print("BUILDER PATTERN DEMONSTRATION")
    print("="*70)

    # Example 1: Simple sequence
    print("\n1️⃣ Simple normal sequence:")
    sequence1 = (TrafficSequenceBuilder()
                 .for_directions(Direction.NORTH, Direction.SOUTH)
                 .with_timing(green=60)
                 .build())
    sequence1.display()

    # Example 2: Rush hour with pedestrians
    print("\n2️⃣ Rush hour sequence with pedestrians:")
    sequence2 = (TrafficSequenceBuilder()
                 .for_directions(Direction.EAST, Direction.WEST)
                 .in_mode(SequenceMode.RUSH_HOUR)
                 .enable_pedestrian(duration=45)
                 .enable_sensors()
                 .build())
    sequence2.display()

    # Example 3: Night mode
    print("\n3️⃣ Night mode (shorter durations):")
    sequence3 = (TrafficSequenceBuilder()
                 .for_directions(Direction.NORTH)
                 .in_mode(SequenceMode.NIGHT)
                 .disable_logging()
                 .build())
    sequence3.display()

    # Example 4: Emergency override
    print("\n4️⃣ Emergency mode:")
    sequence4 = (TrafficSequenceBuilder()
                 .for_directions(Direction.NORTH, Direction.SOUTH, 
                                Direction.EAST, Direction.WEST)
                 .in_mode(SequenceMode.EMERGENCY)
                 .enable_sensors()
                 .build())
    sequence4.display()

    # Example 5: Error handling
    print("\n5️⃣ Error handling - missing required fields:")
    try:
        TrafficSequenceBuilder().build()  # No directions
    except ValueError as e:
        print(f"   ❌ Error: {e}")


if __name__ == "__main__":
    demonstrate_builder()
