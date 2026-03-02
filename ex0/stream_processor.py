from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        ...
    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass
    def format_output(self, result: str) -> str:
        print("Default formatting")

class NumericProcessor(DataProcessor):
    def process(self, data: list[int]) -> str:
        return(f"Processing Data: {data}")

    def validate(self, data) -> bool:
        if data is not None:
            print("Validation: Numeric data verified")
            return True
        else:
            return False
#review
    def format_output(self, result: list[str]) -> str:
        count: int = len(result)
        sum: int = sum(result)
        avg: float = sum / count
        return(f"Output: Processed {count} numeric values, sum= {sum}, avg={avg}")
