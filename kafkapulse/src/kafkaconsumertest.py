from kafka import KafkaProducer, KafkaConsumer
consumer = KafkaConsumer('test-topic', bootstrap_servers='localhost:9094', auto_offset_reset='earliest', consumer_timeout_ms=2000)
for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")

consumer.close()
