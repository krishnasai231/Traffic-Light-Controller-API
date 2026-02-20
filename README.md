Code Architecture, Design Patterns, and Programming Styles
 
A comprehensive learning repository for mastering software architecture, design patterns, and programming paradigms through hands-on exercises and real-world examples.
🎯 Overview
This repository provides a structured lesson plan with practical examples to help developers understand:
•Code Architecture (Layered, Hexagonal, Microservices, Modular Monolith)
•Design Patterns (23 Gang of Four patterns with practical examples)
•Programming Styles (Imperative vs Functional programming)
•Test-Driven Development (TDD best practices)
•Concurrency and Thread Safety
All concepts are demonstrated through a real-world Traffic Light Controller API case study based on the NatWest coding kata.
📚 Repository Structure
code-architecture-lessons/
│
├── README.md                          # This file
├── lessons/                           # Detailed lesson notes
│   ├── 01_code_architecture.md
│   ├── 02_design_patterns.md
│   ├── 03_programming_styles.md
│   ├── 04_functional_programming.md
│   └── 05_tdd_and_testing.md
│
├── examples/                          # Complete working examples
│   ├── architecture/
│   │   ├── layered/                  # Layered architecture demo
│   │   ├── hexagonal/                # Hexagonal/Ports & Adapters
│   │   ├── modular_monolith/         # Modular monolith example
│   │   └── microservices/            # Microservices approach
│   │
│   ├── design_patterns/
│   │   ├── creational/               # Singleton, Factory, Builder, etc.
│   │   ├── structural/               # Adapter, Decorator, Facade, etc.
│   │   └── behavioral/               # Observer, Strategy, State, etc.
│   │
│   └── programming_styles/
│       ├── imperative/               # Imperative examples
│       ├── functional/               # Functional examples
│       └── tiramisu_flow/            # Creative functional recipe example
│
├── exercises/                         # Hands-on exercises
│   ├── traffic_light_controller/     # Main kata exercise
│   ├── design_pattern_katas/         # Pattern-specific exercises
│   └── refactoring_challenges/       # Code refactoring exercises
│
├── tests/                            # Comprehensive test suite
│   ├── test_architecture_examples.py
│   ├── test_design_patterns.py
│   ├── test_traffic_light_controller.py
│   └── test_functional_examples.py
│
├── resources/                        # Additional learning materials
│   ├── cheat_sheets/
│   ├── diagrams/
│   └── references.md
│
├── requirements.txt                  # Python dependencies
├── .gitignore
└── LICENSE
🚀 Getting Started
Prerequisites
•Python 3.8 or higher
•Git
•pip (Python package manager)
Installation
1.Clone the repository:
cd code-architecture
2.Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3.Install dependencies:
pip install -r requirements.txt
Running Examples
# Run design pattern examples
python examples/design_patterns/creational/singleton.py
python examples/design_patterns/behavioral/observer.py

# Run functional programming examples
python examples/programming_styles/functional/tiramisu_flow.py

# Run traffic light controller
python examples/architecture/hexagonal/main.py
Running Tests
# Run all tests
pytest

# Run with coverage
pytest --cov=examples --cov-report=html

# Run specific test file
pytest tests/test_design_patterns.py -v
📖 Learning Path
Beginner Track (Start Here)
1.Read lessons/01_code_architecture.md
2.Complete exercises/traffic_light_controller/01_basic_implementation.py
3.Study examples/design_patterns/creational/singleton.py
4.Practice with exercises/design_pattern_katas/singleton_kata.py
Intermediate Track
1.Read lessons/02_design_patterns.md
2.Study all design pattern examples in examples/design_patterns/
3.Complete exercises/traffic_light_controller/02_with_patterns.py
4.Read lessons/03_programming_styles.md
Advanced Track
1.Study examples/architecture/hexagonal/
2.Read lessons/04_functional_programming.md
3.Implement full Traffic Light Controller with hexagonal architecture
4.Complete exercises/refactoring_challenges/
🎓 Key Concepts
Architecture Patterns Covered
Pattern	Use Case	Example Location
Layered	Simple web applications	examples/architecture/layered/
Hexagonal	Testable, maintainable systems	examples/architecture/hexagonal/
Microservices	Scalable distributed systems	examples/architecture/microservices/
Modular Monolith	Large applications with clear boundaries	examples/architecture/modular_monolith/
Design Patterns Covered
Creational: Singleton, Factory Method, Abstract Factory, Builder, Prototype
Structural: Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy
Behavioral: Observer, Strategy, Command, State, Template Method, Iterator, Chain of Responsibility, Mediator, Memento, Visitor, Interpreter
🏆 Traffic Light Controller Case Study
The repository centers around a Traffic Light Controller API that demonstrates:
•✅ State management for multiple directions (North, South, East, West)
•✅ Validation of conflicting directions (never green simultaneously)
•✅ Command pattern for changing sequences, pausing, resuming
•✅ Observer pattern for state change notifications
•✅ Thread-safe concurrent operations
•✅ Timing history and state queries
•✅ Extensible design for future expansion
See exercises/traffic_light_controller/ for incremental implementations.
🧪 Test-Driven Development (TDD)
All examples follow TDD principles:
1.Red - Write a failing test
2.Green - Write minimal code to pass
3.Refactor - Improve code while keeping tests green
Example TDD workflow:
# tests/test_traffic_light.py
def test_no_conflicting_green_lights():
    controller = TrafficLightController()
    controller.set_green('NORTH')

    with pytest.raises(ConflictError):
        controller.set_green('EAST')  # Should raise - conflicts with NORTH
📊 Assessment Rubric
Use this rubric to evaluate implementations:
Criteria	Poor (1)	Fair (2)	Good (3)	Excellent (4)
Problem Analysis	Incomplete	Partial	Mostly correct	Complete, insightful
Architecture	Ad hoc	Some structure	Clear structure	Modular, extensible
Code Readability	Hard to read	Somewhat readable	Readable	Very clear, well-documented
Edge Cases	None	Some	Most	All, with creative solutions
Test Coverage	Minimal	Some	Good	Comprehensive, TDD evident
Concurrency Safety	Unsafe	Some issues	Mostly safe	Fully safe, well-justified
🤝 Contributing
Contributions are welcome! Please:
1.Fork the repository
2.Create a feature branch (git checkout -b feature/new-pattern)
3.Write tests for your changes
4.Ensure all tests pass (pytest)
5.Submit a pull request
Contribution Guidelines
•Keep examples simple and educational
•Follow PEP 8 style guidelines
•Include comprehensive tests
•Update documentation as needed
•Add type hints to functions
📚 Additional Resources
Books
•Design Patterns: Elements of Reusable Object-Oriented Software (Gang of Four)
•Clean Code by Robert C. Martin
•Functional Programming in Python by David Mertz
Online Resources
•Refactoring Guru - Design Patterns
•Python Design Patterns Guide
•TDD by Example
Related Repositories
•python-design-patterns
•python-design-pattern-rag
•Functional-Programming-Exercises
📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments
•Based on the NatWest Traffic Light Controller coding kata
•Inspired by the Gang of Four design patterns
•Functional programming examples adapted from real-world recipes
•TDD practices from Emily Bache’s guide to code katas
