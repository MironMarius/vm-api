import unittest
from unittest.mock import patch, MagicMock
from src.services.machine_service import MachineService
from src.config import Config

class TestMachineService(unittest.TestCase):
    def setUp(self):
        self.machine_data = {
            "image": "ubuntu",
            "name": "test-vm",
            "cpu": 2,
            "memory": 4096,
            "ports": [8080]
        }
        self.remote_id = "f63cb748-841b-462d-9a66-323ba0796bf6"
        self.machine_id = 1

    @patch('src.services.machine_service.requests.post')
    @patch('src.services.machine_service.db.session')
    def test_create_virtual_machine_success(self, mock_db_session, mock_post):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = f"VM created with ID: {self.remote_id}"
        mock_post.return_value = mock_response

        result = MachineService.create_virtual_machine(self.machine_data)

        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['msg'], 'Machine created successfully')
        mock_post.assert_called_once_with(
            f"{Config.VM_SERVICE_URL}/create",
            json={
                "image": self.machine_data['image'],
                "name": self.machine_data['name'],
                "ports": self.machine_data['ports'],
                "resources": {
                    "cpu": self.machine_data['cpu'],
                    "memory": self.machine_data['memory']
                }
            },
            headers=MachineService.HEADERS
        )
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()


    @patch('src.services.machine_service.requests.post')
    @patch('src.services.machine_service.db.session')
    def test_create_virtual_machine_external_service_failure(self, mock_db_session, mock_post):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.text = "External service error"
        mock_post.return_value = mock_response

        result = MachineService.create_virtual_machine(self.machine_data)

        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['msg'], 'External service error')

        mock_post.assert_called_once()
        mock_db_session.add.assert_not_called()
        mock_db_session.commit.assert_not_called()


    @patch('src.services.machine_service.requests.delete')
    @patch('src.services.machine_service.db.session')
    def test_delete_virtual_machine_success(self, mock_db_session, mock_delete):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = "VM deleted successfully"
        mock_delete.return_value = mock_response

        mock_machine = MagicMock()
        mock_machine.remote_id = self.remote_id

        mock_db_session.query().filter().first.return_value = mock_machine
        mock_db_session.delete.return_value = None
        mock_db_session.commit.return_value = None

        result = MachineService.delete_virtual_machine(self.machine_id)

        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['msg'], 'VM deleted successfully')

        mock_delete.assert_called_once_with(
            f"{Config.VM_SERVICE_URL}/delete",
            json={"UUID": self.remote_id},
            headers=MachineService.HEADERS
        )

        mock_db_session.delete.assert_called_once_with(mock_machine)
        mock_db_session.commit.assert_called_once()

    @patch('src.services.machine_service.requests.delete')
    @patch('src.services.machine_service.db.session')
    def test_delete_virtual_machine_not_found(self, mock_db_session, mock_delete):
        mock_db_session.query().filter().first.return_value = None

        result = MachineService.delete_virtual_machine(self.machine_id)

        self.assertEqual(result['status'], 'not_found')
        self.assertEqual(result['msg'], f"Machine with id: {self.machine_id} not found")
        mock_delete.assert_not_called()
        mock_db_session.delete.assert_not_called()
        mock_db_session.commit.assert_not_called()

    @patch('src.services.machine_service.requests.delete')
    @patch('src.services.machine_service.db.session')
    def test_delete_virtual_machine_external_service_failure(self, mock_db_session, mock_delete):
        mock_response = MagicMock()
        mock_response.ok = False
        mock_response.text = "External service error"
        mock_delete.return_value = mock_response

        mock_machine = MagicMock()
        mock_machine.remote_id = self.remote_id
        mock_db_session.query().filter().first().return_value = mock_machine

        result = MachineService.delete_virtual_machine(self.machine_id)

        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['msg'], 'External service error')
        mock_delete.assert_called_once()
        mock_db_session.delete.assert_not_called()
        mock_db_session.commit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
