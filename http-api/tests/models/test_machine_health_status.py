import unittest
from unittest.mock import MagicMock
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.models.machine_health_status import MachineHealthStatus

class TestMachineHealthStatus(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)

        self.machine_id = 1
        self.status = "healthy"
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

        self.machine_health_status = MachineHealthStatus(
            id=1,
            machine_id=self.machine_id,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    def test_model_attributes(self):
        self.assertEqual(self.machine_health_status.id, 1)
        self.assertEqual(self.machine_health_status.machine_id, self.machine_id)
        self.assertEqual(self.machine_health_status.status, self.status)
        self.assertEqual(self.machine_health_status.created_at, self.created_at)
        self.assertEqual(self.machine_health_status.updated_at, self.updated_at)

    def test_to_dict(self):
        expected_dict = {
            "id": 1,
            "machine_id": self.machine_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
        self.assertEqual(self.machine_health_status.to_dict(), expected_dict)

    def test_latest_heartbeat_by_machine_id(self):
        mock_query = MagicMock()
        mock_query.filter.return_value.order_by.return_value.first.return_value = self.machine_health_status
        self.session.query.return_value = mock_query

        result = MachineHealthStatus.latest_heartbeat_by_machine_id(self.machine_id, self.session)

        self.assertEqual(result, self.machine_health_status)

        self.session.query.assert_called_once_with(MachineHealthStatus)
        mock_query.filter.assert_called_once()
        mock_query.filter().order_by.assert_called_once()
        mock_query.filter().order_by().first.assert_called_once()

    def test_all_heartbeats_by_machine_id(self):
        mock_query = MagicMock()
        mock_query.filter.return_value.order_by.return_value = [self.machine_health_status]
        self.session.query.return_value = mock_query

        result = MachineHealthStatus.all_heartbeats_by_machine_id(self.machine_id, self.session)

        self.assertEqual(list(result), [self.machine_health_status])

        self.session.query.assert_called_once_with(MachineHealthStatus)
        mock_query.filter.assert_called_once()
        mock_query.filter().order_by.assert_called_once()

    def test_repr(self):
        expected_repr = f"<MachineHealthStatus(id=1, machine_id={self.machine_id}, status={self.status})>, updated_at={self.updated_at}, created_at={self.created_at})>"
        self.assertEqual(repr(self.machine_health_status), expected_repr)

if __name__ == '__main__':
    unittest.main()
