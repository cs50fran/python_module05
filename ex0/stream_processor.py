from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        ...

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: Any) -> str:
        return f"Default Output: {result}"


class NumericProcessor(DataProcessor):
    def __init__(self) -> None:
        print("\nInitializing Numeric Processor...")

    def validate(self, data: list[float]) -> bool:
        if isinstance(data, list) and len(data) > 0:
            if all(isinstance(i, (float)) for i in data):
                return True
        return False

    def process(self, data: list[float]) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Invalid numeric data")

            count: int = len(data)
            total: float = sum(data)
            avg: float = total / count

            result = (
                f"Processed {count} numeric values, sum={total}, avg={avg}"
            )
            return self.format_output(result)
        except ValueError as e:
            return f"Error: {e}"

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class TextProcessor(DataProcessor):
    def __init__(self) -> None:
        print("\nInitializing Text Processor...")

    def validate(self, data: str) -> bool:
        if isinstance(data, str) and len(data) > 0:
            return True
        return False

    def process(self, data: str) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Invalid text data")

            chars: int = len(data)
            words: int = len(data.split())

            result = f"Processed text: {chars} characters, {words} words"
            return self.format_output(result)
        except ValueError as e:
            return f"Error: {e}"

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class LogProcessor(DataProcessor):
    def __init__(self) -> None:
        print("\nInitializing log processor")

    def validate(self, data: str) -> bool:
        if isinstance(data, str) and len(data) > 0:
            if len(data.split(":")) == 2:
                return True
        return False

    def process(self, data: str) -> str:
        try:
            if not self.validate(data):
                raise ValueError("Invalid text string")

            level = data.split(":")[0]
            message = data.split(":")[1].strip()

            if level == "ERROR":
                tag = "[ALERT]"
            elif level == "INFO":
                tag = "[INFO]"
            else:
                tag = "[DEFAULT]"

            result = f"{tag} {level} level detected: {message}"
            return self.format_output(result)
        except (ValueError, IndexError):
            return "[ALERT]: Invalid log formatting"

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


def check_processors() -> None:
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")

    num_data: list[float] = [1, 2, 3, 4, 5]
    text_data: str = "Hello 42 World"
    log_data: str = "ERROR: Connection timeout"
    log_data2: str = "INFO: System ready"

    # NUM PROCESSOR
    num_processor = NumericProcessor()
    if (num_processor.validate(num_data)):
        print(f"Processing Data: {num_data}")
        print("Validation: Numeric data verified")
    print(num_processor.process(num_data))

    # TEXT PROCESSOR
    print()
    text_processor = TextProcessor()
    if (text_processor.validate(text_data)):
        print(f"Processing Data: {text_data}")
        print("Validation: Text data verified")
    print(text_processor.process(text_data))

    # LOG PROCESSOR
    print()
    log_processor = LogProcessor()
    if (log_processor.validate(log_data)):
        print(f"Processing Data: {log_data}")
        print("Validation: Log entry verified")
    print(log_processor.process(log_data))

    print("\n=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")

    processors: list[tuple[DataProcessor, Any]] = [
        (num_processor, num_data),
        (text_processor, text_data),
        (log_processor, log_data2),
    ]

    for processor, data in processors:
        print(f"Result: {processor.process(data)}")


if __name__ == "__main__":
    check_processors()
