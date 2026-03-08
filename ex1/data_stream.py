from abc import ABC, abstractmethod
from typing import Any, Optional, Union, List


class DataStream(ABC):

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id
        
    # Process a batch of data
    @abstractmethod
    def process_batch(self, data_batch: list[Any]) -> str:
        pass

    #  data based on criteria
    @abstractmethod
    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        pass

    # Returnstream statistics
    @abstractmethod
    def get_stats(self) -> dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id)
    pass


class TransactionStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id)
    pass


class EventStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id)
    pass

