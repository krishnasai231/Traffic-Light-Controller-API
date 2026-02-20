"""
Singleton Design 
========================

Intent: Ensure a class has only one instance and provide a global point of access.

Use Case: Traffic light controller - one controller per intersection.

Real-world examples:
- Database connections
- Logger instances
- Configuration managers
- Thread pools
"""

import threading
from typing import Optional


class TrafficLightController:
    """
    Thread-safe Singleton implementation using double-checked locking.

    This ensures only one controller instance exists per intersection,
    preventing conflicts from multiple controller instances.
    """

    _instance: Optional['TrafficLightController'] = None
    _lock: threading.Lock = threading.Lock()

    def __new__(cls):
        """
        Create or return the single instance.
        Uses double-checked locking for thread safety with minimal overhead.
        """
        if cls._instance is None:
            with cls._lock:
                # Double-check: another thread might have created instance
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize the controller only once."""
        if self._initialized:
            return

        self.intersection_id = "MAIN_INTERSECTION"
        self.current_state = "RED"
        self._initialized = True
        print(f"✅ Traffic Light Controller created for {self.intersection_id}")

    def get_state(self) -> str:
        """Return current traffic light state."""
        return self.current_state

    def change_state(self, new_state: str) -> None:
        """Change traffic light state."""
        print(f"🚦 State changing: {self.current_state} → {new_state}")
        self.current_state = new_state

    @classmethod
    def reset(cls):
        """Reset singleton (useful for testing)."""
        with cls._lock:
            cls._instance = None


def demonstrate_singleton():
    """Demonstrate that only one instance is created."""
    print("\n" + "="*70)
    print("SINGLETON PATTERN DEMONSTRATION")
    print("="*70)

    # Create first instance
    print("\n1. Creating first controller instance...")
    controller1 = TrafficLightController()
    print(f"   Instance ID: {id(controller1)}")
    print(f"   Current state: {controller1.get_state()}")

    # Change state
    print("\n2. Changing state to GREEN...")
    controller1.change_state("GREEN")

    # Try to create second instance
    print("\n3. Creating 'second' controller instance...")
    controller2 = TrafficLightController()
    print(f"   Instance ID: {id(controller2)}")
    print(f"   Current state: {controller2.get_state()}")

    # Verify they're the same
    print("\n4. Verification:")
    print(f"   controller1 is controller2: {controller1 is controller2}")
    print(f"   Same state: {controller1.get_state() == controller2.get_state()}")

    # Thread safety test
    print("\n5. Thread safety test...")
    instances = []

    def create_instance():
        instances.append(TrafficLightController())

    threads = [threading.Thread(target=create_instance) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    all_same = all(inst is instances[0] for inst in instances)
    print(f"   Created {len(instances)} references from 10 threads")
    print(f"   All references same instance: {all_same}")
    print(f"   Unique instances: {len(set(id(inst) for inst in instances))}")


if __name__ == "__main__":
    demonstrate_singleton()
