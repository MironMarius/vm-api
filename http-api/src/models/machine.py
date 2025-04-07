from src.models import Base
from sqlalchemy import Column, Integer, String, JSON

class Machine(Base):
    __tablename__ = 'machines'

    # future improvements: make Name attribute unique if needed
    # validate remote_id

    id = Column(Integer, primary_key=True, autoincrement=True)
    image = Column(String, nullable=False)
    name = Column(String, nullable=False)
    ports = Column(JSON, nullable=True)
    cpu = Column(Integer, nullable=False)
    memory = Column(Integer, nullable=False)
    remote_id = Column(String, nullable=False)

    def __repr__(self):
        return f"<Machine(id={self.id}, image={self.image}, name={self.name})>, remote_id={self.remote_id}, cpu={self.cpu}, memory={self.memory}, ports={self.ports})>"

    def to_dict(self):
        return {
            "id": self.id,
            "image": self.image,
            "name": self.name,
            "ports": self.ports,
            "cpu": self.cpu,
            "memory": self.memory,
            "remote_id": self.remote_id
        }

    @classmethod
    def get_machine_by_id(cls, machine_id, session):
        return session.query(cls).filter(cls.id == machine_id).first()
