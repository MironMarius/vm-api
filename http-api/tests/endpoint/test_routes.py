import unittest
from unittest.mock import patch, MagicMock
from flask import json
from src import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        self.machine_data = {
            "image": "ubuntu",
            "name": "test-vm",
            "cpu": 2,
            "memory": 4096,
            "ports": [8080]
        }
        self.remote_id = "f63cb748-841b-462d-9a66-323ba0796bf6"
        self.machine_id = 1

    @patch('src.services.machine_service.MachineService.create_machine')
    @patch('src.services.machine_service.requests.post')
    def test_create_virtual_machine_success(self, mock_post, mock_create_machine):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = f"VM created with UUID: {self.remote_id}"
        mock_post.return_value = mock_response

        mock_create_machine.return_value = {
            'status': 'ok',
            'msg': 'Machine created successfully',
            'machine_id': self.machine_id
            }

        response = self.client.post('/machine/create', json=self.machine_data)
        self.assertEqual(response.status_code, 201)

        response = response.get_json()
        self.assertEqual(response['status'], 'ok')
        self.assertEqual(response['msg'], 'Machine created successfully')
        self.assertEqual(response['machine_id'], self.machine_id)
        self.assertEqual(response['details'], f"VM created with UUID: {self.remote_id}")

        mock_post.assert_called_once_with(
            f"{app.config['VM_SERVICE_URL']}/create",
            json={
                "image": "ubuntu",
                "name": "test-vm",
                "ports": [8080],
                "resources": {
                    "cpu": 2,
                    "memory": 4096
                }
            },
            headers={'Content-Type': 'application/json'}
        )

    def test_create_virtual_machine_with_missing_fields(self):
        response = self.client.post('/machine/create', json={
            "image": "ubuntu",
            "name": "test-vm"
        })

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {
            "status": "error",
            "message": "Missing required fields",
            "missingFields": ["cpu", "memory"]
        })

    @patch('src.services.machine_health_status_service.MachineHealthStatusService.update_machine_health_statuses')
    def test_update_machine_health_status(self, mock_update_statuses):
        mock_update_statuses.return_value = {
            'status': 'ok',
            'msg': 'Heartbeat status changed to healthy',
            }

        response = self.client.post('/healthcheck/1', json={})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {
            "status": "ok",
            "msg": "Heartbeat status changed to healthy",
            "machine_id": "1"
        })

    @patch('src.services.machine_service.requests.delete')
    @patch('src.services.machine_service.db.session')
    def test_delete_virtual_machine(self, mock_db_session, mock_delete_request):
        mock_response = MagicMock()
        mock_response.ok = True
        mock_response.text = f"VM {self.remote_id} deleted successfully"
        mock_delete_request.return_value = mock_response

        mock_machine = MagicMock()
        mock_machine.remote_id = self.remote_id

        mock_db_session.query().filter().first.return_value = mock_machine
        mock_db_session.delete.return_value = None
        mock_db_session.commit.return_value = None

        response = self.client.delete('/machine/delete/1', json={})
        self.assertEqual(response.status_code, 200)

        response = response.get_json()
        self.assertEqual(response['status'], 'ok')
        self.assertEqual(response['msg'], f"VM {self.remote_id} deleted successfully")

        mock_delete_request.assert_called_once_with(
            f"{app.config['VM_SERVICE_URL']}/delete",
            json={'UUID': self.remote_id},
            headers={'Content-Type': 'application/json'}
        )

    @patch('src.services.machine_service.db.session')
    def test_delete_virtual_machine_not_found(self, mock_db_session):
        mock_machine = MagicMock()
        mock_machine.id = 2
        mock_db_session.query().filter().first.return_value = None

        mock_db_session.delete.return_value = None
        mock_db_session.commit.return_value = None

        response = self.client.delete('/machine/delete/1', json={})

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {
            "status": "not_found",
            "msg": "Machine with id: 1 not found"
        })

if __name__ == '__main__':
    unittest.main()
