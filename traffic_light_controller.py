"""
 Traffic Light Controller - Hexagonal 
===========================================================


Features:
- Thread-safe concurrent operations
- Conflict validation (no conflicting green lights)
- Hexagonal architecture (Ports & Adapters)
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional
import threading


# Domain Model
class Direction(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


class LightColor(Enum):
    RED = "RED"
    YELLOW = "YELLOW"
    GREEN = "GREEN"


@dataclass
class StateChange:
    """Record of a state change."""
    direction: Direction
    color: LightColor
    timestamp: datetime


class ConflictError(Exception):
    """Raised when conflicting directions would both be green."""
    pass


# Domain Logic
class TrafficLight:
    """Domain entity representing a single traffic light."""

    def __init__(self, direction: Direction):
        self.direction = direction
        self.color = LightColor.RED
        self.history: List[StateChange] = []

    def change_color(self, new_color: LightColor) -> None:
        """Change light color and record in history."""
        self.color = new_color
        change = StateChange(self.direction, new_color, datetime.now())
        self.history.append(change)


class ConflictValidator:
    """Domain service for validating traffic light conflicts."""

    CONFLICTING_DIRECTIONS = {
        Direction.NORTH: [Direction.EAST, Direction.WEST],
        Direction.SOUTH: [Direction.EAST, Direction.WEST],
        Direction.EAST: [Direction.NORTH, Direction.SOUTH],
        Direction.WEST: [Direction.NORTH, Direction.SOUTH],
    }

    @classmethod
    def would_conflict(cls, direction: Direction, 
                      current_states: Dict[Direction, LightColor]) -> bool:
        """Check if setting direction to green would conflict."""
        conflicts = cls.CONFLICTING_DIRECTIONS.get(direction, [])
        return any(
            current_states.get(conflict_dir) == LightColor.GREEN
            for conflict_dir in conflicts
        )


# Ports (Interfaces)
class TrafficLightRepository(ABC):
    """Port: Interface for persistence."""

    @abstractmethod
    def save_state(self, lights: Dict[Direction, TrafficLight]) -> None:
        pass

    @abstractmethod
    def load_state(self) -> Dict[Direction, TrafficLight]:
        pass


class EventPublisher(ABC):
    """Port: Interface for publishing events."""

    @abstractmethod
    def publish(self, event: StateChange) -> None:
        pass


# Adapters (Implementations)
class InMemoryRepository(TrafficLightRepository):
    """Adapter: In-memory storage."""

    def __init__(self):
        self._storage: Dict[Direction, TrafficLight] = {}

    def save_state(self, lights: Dict[Direction, TrafficLight]) -> None:
        self._storage = lights.copy()

    def load_state(self) -> Dict[Direction, TrafficLight]:
        if not self._storage:
            # Initialize default state
            return {
                direction: TrafficLight(direction)
                for direction in Direction
            }
        return self._storage.copy()


class ConsoleEventPublisher(EventPublisher):
    """Adapter: Console output for events."""

    def publish(self, event: StateChange) -> None:
        timestamp = event.timestamp.strftime("%H:%M:%S")
        print(f"[{timestamp}] {event.direction.value}: {event.color.value}")


# Application Service (Use Cases)
class TrafficLightController:
    """
    Core application service implementing traffic light control logic.

    This is the heart of the hexagonal architecture - contains all
    business logic, isolated from external concerns.
    """

    def __init__(self, repository: TrafficLightRepository,
                 publisher: EventPublisher):
        self.repository = repository
        self.publisher = publisher
        self.lights = repository.load_state()
        self._lock = threading.Lock()
        self._paused = False

    def change_light(self, direction: Direction, color: LightColor) -> None:
        """
        Change a traffic light color.

        Validates conflicts and publishes events.
        Thread-safe.
        """
        with self._lock:
            if self._paused:
                raise RuntimeError("Controller is paused")

            # Validate no conflicts if changing to green
            if color == LightColor.GREEN:
                current_states = {d: light.color for d, light in self.lights.items()}
                if ConflictValidator.would_conflict(direction, current_states):
                    conflicting = [
                        d.value for d, c in current_states.items()
                        if d != direction and c == LightColor.GREEN
                    ]
                    raise ConflictError(
                        f"Cannot set {direction.value} to GREEN: "
                        f"conflicts with {conflicting}"
                    )

            # Change light
            light = self.lights[direction]
            light.change_color(color)

            # Publish event
            self.publisher.publish(light.history[-1])

            # Save state
            self.repository.save_state(self.lights)

    def get_current_state(self) -> Dict[Direction, LightColor]:
        """Get current state of all lights."""
        with self._lock:
            return {direction: light.color for direction, light in self.lights.items()}

    def get_history(self, direction: Optional[Direction] = None) -> List[StateChange]:
        """Get history of state changes."""
        with self._lock:
            if direction:
                return self.lights[direction].history.copy()
            else:
                all_history = []
                for light in self.lights.values():
                    all_history.extend(light.history)
                return sorted(all_history, key=lambda x: x.timestamp)

    def pause(self) -> None:
        """Pause the controller."""
        with self._lock:
            self._paused = True
            print("⏸️  Controller paused")

    def resume(self) -> None:
        """Resume the controller."""
        with self._lock:
            self._paused = False
            print("▶️  Controller resumed")

    def execute_sequence(self) -> None:
        """Execute a standard traffic sequence."""
        with self._lock:
            print("\n🔄 Executing sequence...")

            # North-South green
            self.change_light(Direction.NORTH, LightColor.GREEN)
            self.change_light(Direction.SOUTH, LightColor.GREEN)

            # Change to yellow
            self.change_light(Direction.NORTH, LightColor.YELLOW)
            self.change_light(Direction.SOUTH, LightColor.YELLOW)

            # Change to red
            self.change_light(Direction.NORTH, LightColor.RED)
            self.change_light(Direction.SOUTH, LightColor.RED)

            # East-West green
            self.change_light(Direction.EAST, LightColor.GREEN)
            self.change_light(Direction.WEST, LightColor.GREEN)

            print("✅ Sequence complete")


def demonstrate_traffic_controller():
    """Demonstrate complete traffic light controller."""
    print("\n" + "="*70)
    print("COMPLETE TRAFFIC LIGHT CONTROLLER - HEXAGONAL ARCHITECTURE")
    print("="*70)

    # Setup (Dependency Injection)
    repository = InMemoryRepository()
    publisher = ConsoleEventPublisher()
    controller = TrafficLightController(repository, publisher)

    print("\n1️⃣ Initial state:")
    for direction, color in controller.get_current_state().items():
        print(f"   {direction.value}: {color.value}")

    print("\n2️⃣ Execute standard sequence:")
    controller.execute_sequence()

    print("\n3️⃣ Try conflicting change (should fail):")
    try:
        controller.change_light(Direction.NORTH, LightColor.GREEN)
        controller.change_light(Direction.EAST, LightColor.GREEN)  # Conflicts!
    except ConflictError as e:
        print(f"   ❌ Prevented conflict: {e}")

    print("\n4️⃣ View history:")
    history = controller.get_history()
    print(f"   Total state changes: {len(history)}")
    for change in history[-5:]:
        print(f"   {change.direction.value}: {change.color.value}")


if __name__ == "__main__":
    demonstrate_traffic_controller()
