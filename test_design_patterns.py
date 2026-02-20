import pytest
from datetime import datetime
import sys
import os

# Add examples to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'examples'))

# Import pattern examples
from design_patterns.creational.singleton import TrafficLightController as SingletonController
from design_patterns.creational.factory import TrafficLightFactory, LightColor
from design_patterns.behavioral.observer import (
    TrafficLightSubject, MonitoringSystemObserver, DatabaseObserver
)
from design_patterns.behavioral.strategy import (
    FixedTimeStrategy, AdaptiveStrategy, TrafficLightController as StrategyController,
    TrafficData
)
from design_patterns.behavioral.state import TrafficLight, RedState, GreenState
from design_patterns.behavioral.command import (
    TrafficLightReceiver, ChangeToGreenCommand, TrafficLightInvoker
)


class TestSingletonPattern:
    """Test Singleton pattern implementation."""

    def test_singleton_returns_same_instance(self):
        """Verify only one instance is created."""
        controller1 = SingletonController("Test-1")
        controller2 = SingletonController("Test-2")

        assert controller1 is controller2
        assert id(controller1) == id(controller2)

    def test_singleton_state_shared(self):
        """Verify state is shared across references."""
        controller1 = SingletonController()
        controller1.change_state("GREEN")

        controller2 = SingletonController()
        assert controller2.get_state() == "GREEN"

    def test_singleton_thread_safe(self):
        """Verify thread safety of singleton."""
        import threading

        instances = []

        def create_instance():
            instances.append(SingletonController())

        threads = [threading.Thread(target=create_instance) for _ in range(10)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # All instances should be the same
        assert all(inst is instances[0] for inst in instances)


class TestFactoryPattern:
    """Test Factory pattern implementation."""

    def test_factory_creates_vehicle_light(self):
        """Test creation of vehicle light."""
        factory = TrafficLightFactory()
        light = factory.create_light("VEHICLE", "NORTH")

        assert light.light_type == "VEHICLE"
        assert light.direction == "NORTH"
        assert light.color == LightColor.RED

    def test_factory_creates_pedestrian_light(self):
        """Test creation of pedestrian light."""
        factory = TrafficLightFactory()
        light = factory.create_light("PEDESTRIAN", "EAST")

        assert light.light_type == "PEDESTRIAN"
        assert light.direction == "EAST"
        assert hasattr(light, 'has_audio')

    def test_factory_raises_error_for_invalid_type(self):
        """Test factory raises error for invalid type."""
        factory = TrafficLightFactory()

        with pytest.raises(ValueError, match="Unknown light type"):
            factory.create_light("INVALID", "NORTH")


class TestObserverPattern:
    """Test Observer pattern implementation."""

    def test_observer_receives_notifications(self):
        """Test observers are notified of state changes."""
        subject = TrafficLightSubject("Test-Intersection")
        database = DatabaseObserver()

        subject.attach(database)
        subject.change_state("GREEN", "NORTH")

        history = database.get_history()
        assert len(history) == 1
        assert history[0]['new_state'] == "GREEN"
        assert history[0]['direction'] == "NORTH"

    def test_multiple_observers(self):
        """Test multiple observers receive notifications."""
        subject = TrafficLightSubject("Test-Intersection")
        observer1 = DatabaseObserver()
        observer2 = MonitoringSystemObserver("Test-Monitor")

        subject.attach(observer1)
        subject.attach(observer2)

        subject.change_state("YELLOW", "EAST")

        assert len(observer1.get_history()) == 1

    def test_detached_observer_not_notified(self):
        """Test detached observers don't receive notifications."""
        subject = TrafficLightSubject("Test-Intersection")
        observer = DatabaseObserver()

        subject.attach(observer)
        subject.change_state("GREEN", "NORTH")

        subject.detach(observer)
        subject.change_state("RED", "NORTH")

        # Only first change should be recorded
        assert len(observer.get_history()) == 1


class TestStrategyPattern:
    """Test Strategy pattern implementation."""

    def test_fixed_time_strategy(self):
        """Test fixed time strategy."""
        strategy = FixedTimeStrategy(green_duration=30)
        traffic_data = [TrafficData("NORTH", 10, 20)]

        sequence = strategy.calculate_sequence(traffic_data)

        assert len(sequence) == 1
        assert sequence[0] == ("NORTH", 30)

    def test_adaptive_strategy_allocates_more_time_to_busy_direction(self):
        """Test adaptive strategy prioritizes busy directions."""
        strategy = AdaptiveStrategy(min_duration=15, max_duration=60)
        traffic_data = [
            TrafficData("NORTH", 50, 60),  # Very busy
            TrafficData("EAST", 5, 10)     # Not busy
        ]

        sequence = strategy.calculate_sequence(traffic_data)
        north_duration = sequence[0][1]
        east_duration = sequence[1][1]

        # North should get more time
        assert north_duration > east_duration

    def test_strategy_can_be_swapped_at_runtime(self):
        """Test strategies can be changed dynamically."""
        controller = StrategyController(FixedTimeStrategy(30))
        traffic_data = [TrafficData("NORTH", 10, 20)]

        # Use fixed strategy
        sequence1 = controller._strategy.calculate_sequence(traffic_data)

        # Change to adaptive
        controller.set_strategy(AdaptiveStrategy(15, 60))
        sequence2 = controller._strategy.calculate_sequence(traffic_data)

        # Sequences should be different
        assert sequence1 != sequence2


class TestStatePattern:
    """Test State pattern implementation."""

    def test_initial_state_is_red(self):
        """Test traffic light starts in red state."""
        light = TrafficLight("NORTH")
        assert light.get_color() == "RED"
        assert not light.can_cross()

    def test_state_transitions(self):
        """Test state transitions follow correct order."""
        light = TrafficLight("NORTH")

        # RED → GREEN
        light.next()
        assert light.get_color() == "GREEN"
        assert light.can_cross()

        # GREEN → YELLOW
        light.next()
        assert light.get_color() == "YELLOW"
        assert not light.can_cross()

        # YELLOW → RED
        light.next()
        assert light.get_color() == "RED"
        assert not light.can_cross()

    def test_night_mode(self):
        """Test night mode (flashing yellow)."""
        light = TrafficLight("NORTH")
        light.enable_night_mode()

        assert light.get_color() == "FLASHING_YELLOW"
        assert light.can_cross()  # Can cross with caution

    def test_state_history_logged(self):
        """Test state changes are logged."""
        light = TrafficLight("NORTH")
        light.next()
        light.next()

        history = light.get_history()
        assert len(history) >= 2


class TestCommandPattern:
    """Test Command pattern implementation."""

    def test_command_execution(self):
        """Test command executes correctly."""
        receiver = TrafficLightReceiver("Test")
        command = ChangeToGreenCommand(receiver, "NORTH")

        command.execute()

        state = receiver.get_state()
        assert state['state'] == "GREEN"
        assert state['direction'] == "NORTH"

    def test_command_undo(self):
        """Test command can be undone."""
        receiver = TrafficLightReceiver("Test")
        command = ChangeToGreenCommand(receiver, "NORTH")

        # Execute
        command.execute()
        assert receiver.get_state()['state'] == "GREEN"

        # Undo
        command.undo()
        assert receiver.get_state()['state'] == "RED"

    def test_invoker_maintains_history(self):
        """Test invoker tracks command history."""
        receiver = TrafficLightReceiver("Test")
        invoker = TrafficLightInvoker()

        cmd1 = ChangeToGreenCommand(receiver, "NORTH")
        cmd2 = ChangeToGreenCommand(receiver, "EAST")

        invoker.execute_command(cmd1)
        invoker.execute_command(cmd2)

        # History should have 2 commands
        assert len(invoker._history) == 2

    def test_undo_redo(self):
        """Test undo and redo functionality."""
        receiver = TrafficLightReceiver("Test")
        invoker = TrafficLightInvoker()

        command = ChangeToGreenCommand(receiver, "NORTH")
        invoker.execute_command(command)

        # Undo
        invoker.undo()
        assert receiver.get_state()['state'] == "RED"

        # Redo
        invoker.redo()
        assert receiver.get_state()['state'] == "GREEN"


# Pytest configuration and fixtures
@pytest.fixture
def sample_traffic_data():
    """Fixture providing sample traffic data."""
    return [
        TrafficData("NORTH", 25, 45),
        TrafficData("EAST", 10, 20),
        TrafficData("SOUTH", 30, 60),
        TrafficData("WEST", 5, 15)
    ]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
