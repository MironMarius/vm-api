from unittest.mock import patch, MagicMock
from src.services.machine_health_status_service import MachineHealthStatusService
import unittest
import random

class TestMachineHealthStatusService(unittest.TestCase):
    @patch('src.services.machine_health_status_service.db.session')
    def test_update_machine_health_statuses_with_new_status(self, mock_db_session):
        mock_status = 'healthy'
        mock_machine = MagicMock()
        mock_machine.id = 1

        mock_db_session.query().filter().first.return_value = mock_machine
        mock_db_session.query().filter().order_by().first.return_value = None

        response = MachineHealthStatusService.update_machine_health_statuses(machine_id=1, status=mock_status)

        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

        self.assertEqual(response['status'], 'ok')
        self.assertIn(f"Heartbeat status changed to: {mock_status}", response['msg'])

    @patch('src.services.machine_health_status_service.db.session')
    def test_update_machine_health_statuses_existing_status(self, mock_db_session):
        mock_heartbeat = MagicMock()
        mock_heartbeat.status = "healthy"
        mock_db_session.query().filter().order_by().first.return_value = mock_heartbeat

        response = MachineHealthStatusService.update_machine_health_statuses(machine_id=1, status="healthy")

        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

        self.assertEqual(response['status'], 'ok')
        self.assertIn(f"Last heartbeat status: {mock_heartbeat.status}, updating timestamp only", response['msg'])

    @patch('src.services.machine_health_status_service.db.session')
    def test_update_machine_health_statuses_with_machine_id_not_found(self, mock_db_session):
        mock_machine_id = random.randrange(99)

        mock_db_session.query().filter().first.return_value = None

        response = MachineHealthStatusService.update_machine_health_statuses(machine_id=mock_machine_id, status="healthy")

        mock_db_session.commit.assert_not_called()
        mock_db_session.add.assert_not_called()

        self.assertEqual(response['status'], 'not_found')
        self.assertEqual(response['msg'], f"Machine with id: {mock_machine_id} not found")

    @patch('src.services.machine_health_status_service.db.session')
    def test_update_machine_health_statuses_error(self, mock_db_session):
        mock_db_session.commit.side_effect = Exception("Database error")

        response = MachineHealthStatusService.update_machine_health_statuses(machine_id=1, status="healthy")

        mock_db_session.rollback.assert_called_once()
        
        self.assertEqual(response['status'], 'error')
        self.assertEqual(response['msg'], "Database error")


if __name__ == '__main__':
    unittest.main()
