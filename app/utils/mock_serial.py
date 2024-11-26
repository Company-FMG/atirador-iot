import threading
import time
import queue
import random

class MockArduino:
    def __init__(self):
        self.in_waiting = 0
        self._data_queue = queue.Queue()
        self._running = False

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._mock_data_generator)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        self._running = False
        if hasattr(self, '_thread') and self._thread.is_alive():
            self._thread.join(timeout=1)  # Aguarda até 1 segundo para finalizar
            if self._thread.is_alive():
                print("Warning: MockArduino thread did not terminate in time.")

    def _mock_data_generator(self):
        while self._running:
            time.sleep(0.1)  # Intervalo entre verificações, ajustável para simular mais ou menos frequência
            if self._running:
                # Simulação de movimento aleatório com 50% de chance de detectar movimento
                if random.random() < 0.5:  # 50% de chance de detectar movimento
                    self._data_queue.put("1\n")  # Simula movimento detectado
                    self.in_waiting = self._data_queue.qsize()
                else:
                    self._data_queue.put("0\n")  # Sem movimento detectado
                    self.in_waiting = self._data_queue.qsize()


    def readline(self):
        try:
            data = self._data_queue.get_nowait()
            self.in_waiting = self._data_queue.qsize()
            return data.encode('utf-8')  # Simula dados em bytes
        except queue.Empty:
            return b""

    def write(self, data):
        print(f"MockArduino recebeu comando: {data.decode('utf-8')}")