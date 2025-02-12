import pytest
from src.kafka_pulse import parse_heart_rate
import struct


def test_parse_heart_rate_8bit():
    # Create sample 8-bit heart rate data
    data = bytearray([0b00000000, 70])  # 8-bit heart rate value of 70
    hr_val, timestamp = parse_heart_rate(data)
    assert hr_val == 70
    assert isinstance(timestamp, float)

def test_parse_heart_rate_16bit():
    # Create sample 16-bit heart rate data
    data = bytearray([0b00000001, 0x46, 0x00])  # 16-bit heart rate value of 70
    hr_val, timestamp = parse_heart_rate(data)
    assert hr_val == 70
    assert isinstance(timestamp, float)

def test_parse_heart_rate_invalid_data():
    # Create invalid heart rate data
    data = bytearray([0b00000000])  # Missing heart rate value
    with pytest.raises(struct.error):
        parse_heart_rate(data)