from kafka import KafkaProducer, KafkaConsumer
import asyncio
from kafka.errors import KafkaError
from time import time
import random
from kafka_pulse import HeartRateMonitor, HeartRateDataCollector, DEVICE_ADDRESS

KAFKA_TOPIC = 'test-topic'
KAFKA_SERVER = 'localhost:9094'

class KafkaHeartRateMonitor(HeartRateMonitor):
    def __init__(self, address: str, data_collector: HeartRateDataCollector):
        super().__init__(address, data_collector)
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

    def send_to_kafka(self, heart_rate: int, timestamp: float) -> None:
        """Sends heart rate data to Kafka"""
        message = f"{heart_rate},{timestamp}".encode('utf-8')
        try:
            future = self.producer.send(KAFKA_TOPIC, message)
            result = future.get(timeout=10)
            print(f"Message sent to Kafka: {result}")
        except KafkaError as e:
            print(f"Failed to send message to Kafka: {e}")


    async def mock_heart_rate(self) -> None:
        while True:
            heart_rate = random.randint(50, 70)
            timestamp = time()
            print(f"Mock HR Value: {heart_rate} at {timestamp}")
            self.data_collector.add_data(heart_rate, timestamp)
            self.send_to_kafka(heart_rate, timestamp)
            await asyncio.sleep(1)

def main() -> None:
    data_collector = HeartRateDataCollector()
    monitor = KafkaHeartRateMonitor(DEVICE_ADDRESS, data_collector)
    # asyncio.run(monitor.connect_and_receive_hr(plot_data=True))
    # Use the mock heart rate method for testing
    asyncio.run(monitor.mock_heart_rate())
    # close the producer
    monitor.producer.close()

if __name__ == "__main__":
    main()