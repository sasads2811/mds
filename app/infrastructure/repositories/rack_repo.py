import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.infrastructure.db.models.rack_model import RackModel
from app.domain.rack.entity import Rack


class RackRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_rack_by_id(self, rack_id: uuid.UUID) -> Rack:
        q = select(RackModel).where(RackModel.id == rack_id)

        result = self.session.execute(q)

        result = result.scalars().first()

        return result

    def get_all(self):
        q = select(RackModel)

        result = self.session.execute(q)

        return result.scalars().all()

    def create(self, rack: Rack) -> Rack:
        model = RackModel(
            name=rack.name,
            description=rack.description,
            serial_number=rack.serial_number,
            max_power_watts=rack.max_power_watts,
            total_units=rack.total_units,
        )

        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        rack.id = model.id

        return rack

    def save(self, rack: Rack) -> Rack:
        result = self.session.get(RackModel, rack.id)

        result.name = rack.name
        result.description = rack.description
        result.serial_number = rack.serial_number
        result.total_units = rack.total_units
        result.max_power_watts = rack.max_power_watts

        self.session.commit()
        self.session.refresh(result)

        return rack
