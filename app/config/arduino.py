from app.config.base import BaseConfig

class ArduinoConfig(BaseConfig):
    DEBUG = True
    MOCK_ENABLED = False
    ARDUINO_PORT = '/dev/ttyACM0'  # Altere conforme necessário