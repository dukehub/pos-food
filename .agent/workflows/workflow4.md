---
description: plugin kitchen
---

ajouter le model kitchen dans le plugin floor_plan:

class Kitchen(Base): """Zone de production (Bar, Cuisine Chaude, Pizza).""" tablename = "kitchens"

id = Column(String(36), primary_key=True, default=uuid_str)
name = Column(String, nullable=False)

devices = relationship("Device", secondary=kitchen_devices, lazy="selectin")
products = relationship("Product", back_populates="kitchen")

kitchen_devices = Table(
"kitchen_devices",
Base.metadata,
Column("kitchen_id", ForeignKey("kitchens.id", ondelete="CASCADE"), primary_key=True),
Column("device_id", ForeignKey("device.id", ondelete="CASCADE"), primary_key=True),
)
