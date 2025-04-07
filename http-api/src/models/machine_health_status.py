from src.models import Base

from datetime import datetime
from datetime import timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Index, desc
from sqlalchemy.orm import relationship, backref

class MachineHealthStatus(Base):
    __tablename__ = 'machine_health_statuses'
    __table_args__ = (
        Index('idx_machine_id_created_at', 'machine_id', 'created_at'),
    )

    # future improvements:
    # consider archiving old heartbeats from this table
    # TimescaleDB for scaling or similar

    id = Column(Integer, primary_key=True, autoincrement=True)
    machine_id = Column(Integer, ForeignKey('machines.id'), nullable=False, index=True)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)

    machine = relationship('Machine', backref=backref('health_statuses', lazy=True))

    def __repr__(self):
        return f"<MachineHealthStatus(id={self.id}, machine_id={self.machine_id}, status={self.status})>, updated_at={self.updated_at}, created_at={self.created_at})>"

    def to_dict(self):
        return {
            "id": self.id,
            "machine_id": self.machine_id,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def latest_heartbeat_by_machine_id(cls, machine_id, session):
        heartbeat = (
            session.query(cls)
            .filter(cls.machine_id == machine_id)
			.order_by(desc(cls.created_at))
            .first()
        )
        return heartbeat

    @classmethod
    def all_heartbeats_by_machine_id(cls, machine_id, session):
        heartbeats = (
            session.query(cls)
            .filter(cls.machine_id == machine_id)
            .order_by(desc(cls.id))
        )
        return heartbeats
