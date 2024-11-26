from flask import Blueprint, current_app, render_template, jsonify, request, g
import threading
import time
from flask import jsonify

bp = Blueprint('routes', __name__)

# Variáveis globais
ser = None
pir_thread = None
pir_status = "No motion"

@bp.before_app_request
def setup_serial():
    global ser
    if current_app.config['MOCK_ENABLED']:
        from app.utils.mock_serial import MockArduino
        import atexit

        ser = MockArduino()
        ser.start()
        atexit.register(ser.stop)
    else:
        import serial
        ser = serial.Serial(current_app.config['ARDUINO_PORT'], 9600, timeout=1)
        ser.reset_input_buffer()

@bp.before_app_request
def start_pir_thread():
    global pir_thread
    if not pir_thread:
        pir_thread = threading.Thread(target=read_pir)
        pir_thread.daemon = True
        pir_thread.start()

# Thread para monitorar o PIR
def read_pir():
    global pir_status
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line == "1":
                pir_status = "Motion detected!"
            else:
                pir_status = "No motion"
        time.sleep(0.1)

@bp.route('/')
def index():
    return render_template('index.html', pir_status=pir_status)

@bp.route('/api/pir_status', methods=['GET'])
def get_pir_status():
    return jsonify({"pir_status": pir_status})

@bp.route('/api/move_servo', methods=['POST'])
def move_servo():
    data = request.json
    servo_angle = data.get('servo_angle', 0)
    ser.write(f"{servo_angle}\n".encode('utf-8'))
    return jsonify({"message": f"Servo movido para o ângulo {servo_angle}"}), 200

@bp.route('/api/trigger', methods=['POST'])
def trigger():
    ser.write(b"TRIGGER\n")
    return jsonify({"message": "Servo do gatilho ativado e retornado para a posição inicial"}), 200
