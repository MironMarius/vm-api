from flask import jsonify, request
from src.services.machine_service import MachineService
from src.services.machine_health_status_service import  MachineHealthStatusService
from src.util.response_builder import ResponseBuilder
import random

def register_routes(app):
    @app.route('/')
    def index():
        return jsonify({"message": "Hello, World!"}), 200


    @app.route('/machine/all', methods=['GET'])
    def virtual_machines():
        response = MachineService.get_virtual_machines()
        return jsonify(response), 200


    @app.route('/healthcheck/show/<machine_id>', methods=['GET'])
    def machine_heartbeats(machine_id):
        error = __validate_machine_id(machine_id)
        if error: return jsonify(error), 400

        response = MachineHealthStatusService.get_machine_health_statuses(machine_id)
        return jsonify(response), 200


    @app.route('/healthcheck/<machine_id>', methods=['POST'])
    def update_machine_health_status(machine_id):
        error = __validate_machine_id(machine_id)
        if error: return jsonify(error), 400

        return jsonify({"status": "ok"}), 200

        status = 'healthy' #random.choice(['healthy', 'unhealthy'])

        response = MachineHealthStatusService.update_machine_health_statuses(machine_id, status)

        if response['status'] == 'not_found': return jsonify({"machine_id": machine_id} | response), 404
        if response['status'] == 'error': return jsonify({"machine_id": machine_id} | response), 500

        return jsonify({"machine_id": machine_id} | response), 200


    @app.route('/machine/create', methods=['POST'])
    def create_virtual_machine():
        REQUIRED_FIELDS = ['image', 'name', 'cpu', 'memory']
        data = request.get_json()

        error = __validate_create_new_vm_input(data)
        if error: return jsonify(error), 400

        response = MachineService.create_virtual_machine(data)
        if response['status'] == 'error': return jsonify(response), 500

        return jsonify(response), 201


    @app.route('/machine/delete/<machine_id>', methods=['DELETE'])
    def delete_virtual_machine(machine_id):
        error = __validate_machine_id(machine_id)
        if error: return jsonify(error), 400

        response = MachineService.delete_virtual_machine(machine_id)

        if response['status'] == 'not_found': return jsonify(response), 404
        if response['status'] == 'error': return jsonify(response), 500

        return jsonify(response), 200


    # future improvements: implement a better validation mechanism, to also validate values
    def __validate_create_new_vm_input(data):
        REQUIRED_FIELDS = ['image', 'name', 'cpu', 'memory']

        if not data or not all(key in data for key in REQUIRED_FIELDS):
            missing_fields = [key for key in REQUIRED_FIELDS if key not in data]
            return ResponseBuilder.error('Missing required fields', missing_fields=missing_fields)


    def __validate_machine_id(machine_id):
        try:
            int(machine_id)
        except ValueError as e:
            return ResponseBuilder.error(f"Provided machineId is not an integer, {str(e)}")
