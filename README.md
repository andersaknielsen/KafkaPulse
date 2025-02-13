# KafkaPulse

KafkaPulse is a spare time coding exercise designed to learn about streaming data using Apache Kafka. The project involves processing heart rate signals broadcast from a Garmin watch.

## Features

- **Data Streaming**: Utilizes Apache Kafka for streaming data.
- **Heart Rate Monitoring**: Processes heart rate signals from a Garmin watch.
- **Python Libraries**: Uses Bleak and Bleakheart for data processing.

## Getting Started

### Prerequisites

- Garmin watch with heart rate broadcasting capability
- Python 3.12+
- Apache Kafka (eventually)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/andersaknielsen/KafkaPulse.git
    cd KafkaPulse
    ```

1. Install the required Python libraries:
    ```bash
    uv sync
    ```

1. Set up Apache Kafka:
    ```bash
    cd kafka
    docker compose up -d
    ```

## Usage

1. Start the Kafka server:
    ```bash
    TODO
    ```

1. Run the KafkaPulse script:
    ```bash
    python src\kafka_pulse.py
    ```

## Cleanup
1. Terminate Kafka server
    ```bash
    cd kafka
    docker compose down
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please open an issue or contact me at [andersaknielsen@gmail.com].
