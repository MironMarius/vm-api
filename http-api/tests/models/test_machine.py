import unittest
from unittest.mock import MagicMock
from src.models.machine import Machine

class TestMachine(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()

        self.machine_id = 1
        self.image = "ubuntu"
        self.name = "test-vm"
        self.ports = [8080, 8081]
        self.cpu = 2
        self.memory = 4096
        self.remote_id = "f63cb748-841b-462d-9a66-323ba0796bf6"

        self.machine = Machine(
            id=self.machine_id,
            image=self.image,
            name=self.name,
            ports=self.ports,
            cpu=self.cpu,
            memory=self.memory,
            remote_id=self.remote_id
        )

    def test_model_attributes(self):
        self.assertEqual(self.machine.id, self.machine_id)
        self.assertEqual(self.machine.image, self.image)
        self.assertEqual(self.machine.name, self.name)
        self.assertEqual(self.machine.ports, self.ports)
        self.assertEqual(self.machine.cpu, self.cpu)
        self.assertEqual(self.machine.memory, self.memory)
        self.assertEqual(self.machine.remote_id, self.remote_id)

    def test_to_dict(self):
        expected_dict = {
            "id": self.machine_id,
            "image": self.image,
            "name": self.name,
            "ports": self.ports,
            "cpu": self.cpu,
            "memory": self.memory,
            "remote_id": self.remote_id
        }
        self.assertEqual(self.machine.to_dict(), expected_dict)

    def test_repr(self):
        expected_repr = f"<Machine(id={self.machine_id}, image={self.image}, name={self.name})>, remote_id={self.remote_id}, cpu={self.cpu}, memory={self.memory}, ports={self.ports})>"
        self.assertEqual(repr(self.machine), expected_repr)

    def test_get_machine_by_id(self):
        mock_query = MagicMock()
        mock_query.filter.return_value.first.return_value = self.machine
        self.session.query.return_value = mock_query

        result = Machine.get_machine_by_id(self.machine_id, self.session)

        self.assertEqual(result, self.machine)

        self.session.query.assert_called_once_with(Machine)
        mock_query.filter.assert_called_once()
        mock_query.filter().first.assert_called_once()

if __name__ == '__main__':
    unittest.main()
