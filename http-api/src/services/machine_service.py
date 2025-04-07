from src.models.machine import Machine
from src.util.response_builder import ResponseBuilder
from src import db
from src.config import Config
import requests

class MachineService:
    HEADERS = {"Content-Type": "application/json"}

    def get_virtual_machines():
        machines = db.session.query(Machine).all()
        return {'machines': [machine.to_dict() for machine in machines]}


    @classmethod
    def create_virtual_machine(cls, data):
        payload = {
            "image": data['image'],
            "name": data['name'],
            "ports": data.get('ports', []),
            "resources": {
                "cpu": data['cpu'],
                "memory": data['memory']
            }
        }

        # future improvements: make requests async

        response = requests.post(f"{Config.VM_SERVICE_URL}/create", json=payload, headers=cls.HEADERS)

        if response.ok:
            remote_id = response.text.strip().split(": ")[1].strip()
            data.update(remote_id=remote_id)

            session_data = cls.create_machine(data)
            session_data.update(details=response.text)
            return session_data
        else:
            return ResponseBuilder.error(response.text)

    # future improvements:
    # vm service might fail even though the request is successful in some cases
    # add a functinality to scan for machines that might exist in the vm-service but not in http-api database, or vice versa
    # if machine is deleted in vm-service, but transaction fails in http-api, implement a retry mechanism
    # handle concurrent requests to delete the same machine

    @classmethod
    def delete_virtual_machine(cls, machine_id):
        result = ''

        machine = db.session.query(Machine).filter(Machine.id == machine_id).first()
        if not machine: return ResponseBuilder.machine_not_found(machine_id)

        payload = {"UUID": machine.remote_id}
        response = requests.delete(f"{Config.VM_SERVICE_URL}/delete", json=payload, headers=cls.HEADERS)
        if response.ok:
            try:
                db.session.delete(machine)
                db.session.commit()
                result = ResponseBuilder.ok(response.text)
            except Exception as e:
                db.session.rollback()
                result = ResponseBuilder.error(str(e))
        else:
            result = ResponseBuilder.error(response.text)

        return result

    @classmethod
    def create_machine(cls, data):
        result = {}
        machine = Machine(
            image = data['image'],
            name=data['name'],
            ports=data.get('ports', None),
            cpu=data['cpu'],
            memory=data['memory'],
            remote_id=data['remote_id']
        )

        try:
            db.session.add(machine)
            db.session.commit()
            result = ResponseBuilder.ok('Machine created successfully') | {'machine_id': machine.id}
        except Exception as e:
            db.session.rollback()
            cls.handle_machine_created_inconsistencies(data['remote_id'])
            result = ResponseBuilder.error(str(e))

        return result

    # handle case when machine was created in vm-service, but transaction failed in http-api
    @classmethod
    def handle_machine_created_inconsistencies(cls, remote_id):
        if not remote_id: return f"No machine with UUID: {remote_id}"

        payload = {"UUID": remote_id}
        try:
            response = requests.delete(f"{Config.VM_SERVICE_URL}/delete", json=payload, headers=cls.HEADERS)
            if response.ok:
                print(f"Cleanup succesful: {response.text}")
        except Exception as e:
                print(f"Couldn't cleanup machine({remote_id}): {str(e)}")
