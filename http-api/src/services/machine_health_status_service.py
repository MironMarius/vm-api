from src.models.machine_health_status import MachineHealthStatus
from src.models.machine import Machine
from src import db
from datetime import datetime, timezone
from src.util.response_builder import ResponseBuilder


class MachineHealthStatusService:
    @staticmethod
    def get_machine_health_statuses(machine_id):
        heartbeats = MachineHealthStatus.all_heartbeats_by_machine_id(machine_id, db.session)
        return {'heartbeats': [heartbeat.to_dict() for heartbeat in heartbeats], 'count': heartbeats.count()}


    @staticmethod
    def update_machine_health_statuses(machine_id, status):
        msg = ''

        machine = db.session.query(Machine).filter(Machine.id == machine_id).first()
        if not machine: return ResponseBuilder.machine_not_found(machine_id)

        heartbeat = MachineHealthStatus.latest_heartbeat_by_machine_id(machine_id, db.session)

        if heartbeat and heartbeat.status == status:
            heartbeat.updated_at = datetime.now(timezone.utc)
            msg = f"Last heartbeat status: {status}, updating timestamp only"
        else:
            heartbeat = MachineHealthStatus(machine_id=machine_id, status=status)
            msg = f"Heartbeat status changed to: {status}"

        response = ResponseBuilder.ok(msg)

        try:
            db.session.add(heartbeat)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            response = ResponseBuilder.error(str(e))

        return response
