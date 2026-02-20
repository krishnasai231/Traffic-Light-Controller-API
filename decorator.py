"""
Decorator Design 
=========================

Intent: Attach additional responsibilities to an object dynamically.
"""

from abc import ABC, abstractmethod


class TrafficLightComponent(ABC):
    @abstractmethod
    def change_state(self, state: str) -> None:
        pass


class BasicTrafficLight(TrafficLightComponent):
    def __init__(self):
        self.state = "RED"

    def change_state(self, state: str) -> None:
        self.state = state
        print(f"   Light changed to: {state}")


class LoggingDecorator(TrafficLightComponent):
    def __init__(self, component: TrafficLightComponent):
        self._component = component

    def change_state(self, state: str) -> None:
        print(f"   [LOG] Changing state to {state}")
        self._component.change_state(state)
        print(f"   [LOG] State changed successfully")


class ValidationDecorator(TrafficLightComponent):
    def __init__(self, component: TrafficLightComponent):
        self._component = component

    def change_state(self, state: str) -> None:
        if state not in ["RED", "YELLOW", "GREEN"]:
            print(f"   [VALIDATION] Invalid state: {state}")
            return
        print(f"   [VALIDATION] State {state} is valid")
        self._component.change_state(state)


def demonstrate_decorator():
    print("\n" + "="*70)
    print("DECORATOR PATTERN DEMONSTRATION")
    print("="*70)

    print("\n1️⃣ Basic light:")
    light1 = BasicTrafficLight()
    light1.change_state("GREEN")

    print("\n2️⃣ Light with logging:")
    light2 = LoggingDecorator(BasicTrafficLight())
    light2.change_state("GREEN")

    print("\n3️⃣ Light with validation and logging:")
    light3 = LoggingDecorator(ValidationDecorator(BasicTrafficLight()))
    light3.change_state("GREEN")

    print("\n4️⃣ Attempt invalid state:")
    light3.change_state("PURPLE")


if __name__ == "__main__":
    demonstrate_decorator()
