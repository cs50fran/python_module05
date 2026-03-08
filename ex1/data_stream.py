from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):

    def __init__(self, stream_id: str, stream_type: str) -> None:
        self.stream_id: str = stream_id
        self.stream_type: str = stream_type
        self.processed_batches: int = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:

        if criteria is None:
            return data_batch

        return [i for i in data_batch if criteria.lower() in str(i).lower()]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "stream_id": self.stream_id,
            "stream_type": self.stream_type,
            "processed_batches": self.processed_batches
        }


# SENSOR STREAM

class SensorStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id, "Environmental Data")

    def process_batch(self, data_batch: List[str]) -> str:

        temps = []
        for item in data_batch:
            try:
                key, value = item.split(":")
                if key.lower() == "temp":
                    temps.append(float(value))

                avg_temp = sum(temps) / len(temps) if temps else 0.0
            except ValueError:
                print(f"Invalid data format: {item}")

        self.processed_batches += 1

        return (
            f"Sensor analysis: {len(data_batch)} readings processed,"
            f" avg temp: {avg_temp:.1f}°C"
        )


# TRANSACTION STREAM

class TransactionStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id, "Financial Data")

    def process_batch(self, data_batch: List[str]) -> str:

        net_flow = 0

        for item in data_batch:
            try:
                op, value = item.split(":")
                # net_flow = int(value) if op == "buy" else -int(value)

                if op.lower().strip() == "buy":
                    net_flow -= int(value)
                elif op.lower().strip() == "sell":
                    net_flow += int(value)
                else:
                    raise ValueError(
                        f"Invalid data format: {op} - use 'buy' or 'sell'")

            except ValueError:
                print(f"Invalid transaction format: {item}, skipping")

        self.processed_batches += 1

        net_flow = -net_flow
        sign = "+" if net_flow >= 0 else ""

        return (
            f"Transaction analysis: {len(data_batch)} operations,"
            f" net flow: {sign}{net_flow} units"
        )


# EVENT STREAM

class EventStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id, "System Events")

    def process_batch(self, data_batch: List[str]) -> str:

        error_count = sum(
            1 for event in data_batch if "error" in event.lower())

        self.processed_batches += 1

        return (
            f"Event analysis: {len(data_batch)} events,"
            f" {error_count} error detected"
        )


# STREAM PROCESSOR

class StreamProcessor:

    def process_streams(
        self,
        streams: List[DataStream],
        batches: List[List[str]]
    ) -> None:

        print("=== Polymorphic Stream Processing ===")
        print("Processing mixed stream types through unified interface...\n")

        print("Batch 1 Results:")

        for stream, batch in zip(streams, batches):

            filtered = stream.filter_data(batch)

            if isinstance(stream, SensorStream):
                print(f"- Sensor data: {len(filtered)} readings processed")

            elif isinstance(stream, TransactionStream):
                print(
                    "- Transaction data: "
                    f"{len(filtered)} operations processed")

            elif isinstance(stream, EventStream):
                print(f"- Event data: {len(filtered)} events processed")

        print("\nStream filtering active: High-priority data only")

        critical_counts: Dict[str, int] = {}

        for stream, batch in zip(streams, batches):
            if isinstance(stream, SensorStream):
                alerts = stream.filter_data(batch, "temp")
                critical_counts["sensor_alerts"] = len(alerts)
            elif isinstance(stream, TransactionStream):
                large = stream.filter_data(batch, "sell")
                critical_counts["large_transactions"] = len(
                    [t for t in large if int(t.split(":")[1]) >= 100]
                )

        sensor_alerts = critical_counts.get("sensor_alerts", 0)
        large_tx = critical_counts.get("large_transactions", 0)

        print(
            f"Filtered results: {sensor_alerts} critical sensor alerts,"
            f" {large_tx} large transaction"
        )


# MAIN DEMO

def main() -> None:

    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")

    # Sensor example
    print("Initializing Sensor Stream...")
    sensor = SensorStream("SENSOR_001")
    print(f"Stream ID: {sensor.stream_id}, Type: {sensor.stream_type}")

    batch_sensor = ["temp:22.5", "humidity:65", "pressure:1013"]
    print(f"Processing sensor batch: [{', '.join(batch_sensor)}]")
    print(sensor.process_batch(batch_sensor))
    print()

    # Transaction example
    print("Initializing Transaction Stream...")
    transaction = TransactionStream("TRANS_001")
    print(
        f"Stream ID: {transaction.stream_id}, Type: {transaction.stream_type}")

    batch_trans = ["buy:100", "sell:150", "Buy : 75"]
    print(f"Processing transaction batch: [{', '.join(batch_trans)}]")
    print(transaction.process_batch(batch_trans))
    print()
    # Event example
    print("Initializing Event Stream...")
    event = EventStream("EVENT_001")
    print(f"Stream ID: {event.stream_id}, Type: {event.stream_type}")

    batch_event = ["login", "error", "logout"]
    print(f"Processing event batch: [{', '.join(batch_event)}]")
    print(event.process_batch(batch_event))
    print()
    # POLYMORPHIC DEMO
    # -----------------------

    streams: List[DataStream] = [sensor, transaction, event]

    batches: List[List[str]] = [
        ["temp:21.0", "temp:23.0"],
        ["buy:50", "sell:100", "buy:20", "sell:10"],
        ["login", "error", "logout"]
    ]

    processor = StreamProcessor()

    processor.process_streams(streams, batches)

    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()
