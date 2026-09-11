import socket
import json
import time
import threading
from ML import AI

class ESP32Com:
    def __init__(self, ip="192.168.1.6", port=5000):
        self.ip = ip
        self.port = port
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread = None

        # shared state, GUI reads these
        self.dark = False
        self.light = False
        self.temperature = None
        self.fan = None
        self.gas_state = False
        self.buzzer_state = False
        self.servo_state = False
        self._classification = '3'

        self._sock = None

    def connect(self):
        while not self._stop_event.is_set():
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((self.ip, self.port))
                print("Connected to ESP32")
                return s
            except OSError:
                print("Connection failed, retrying...")
                time.sleep(1)
        return None

    def classify_cry(self):
        return AI.get_prediction()

    def get_classification(self):
        with self._lock:
            return self._classification

    def start(self):
        AI.start()

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run,daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._sock:
            self._sock.close()
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self):
        self._sock = self.connect()
        if self._sock is None:
            return
        f = self._sock.makefile("r")

        while not self._stop_event.is_set():
            line = f.readline()
            if not line:
                print("Disconnected, reconnecting...")
                self._sock.close()
                self._sock = self.connect()
                if self._sock is None:
                    return
                f = self._sock.makefile("r")
                continue

            line = line.strip()
            if not line:
                continue

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                print("Bad JSON:", line)
                continue

            classification = self.classify_cry()

            with self._lock:
                self.dark = bool(data.get("Dark"))
                self.light = bool(data.get("Light"))
                self.temperature = int(data.get("Temperature"))
                self.fan = data.get("Fan")
                self.gas_state = bool(data.get("Gas"))
                self.buzzer_state = bool(data.get("Buzzer"))
                self.servo_state = bool(data.get("Servo"))
                self._classification = classification

            try:
                self._sock.sendall(classification.encode())
            except OSError:
                print("Send failed, will reconnect")
                continue