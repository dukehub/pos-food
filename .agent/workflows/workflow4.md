---
description: plugin kitchen
---

ajouter le model kitchen dans le plugin floor_plan:
class Kitchen(Base): """Zone de production (Bar, Cuisine Chaude, Pizza).""" tablename = "kitchens"

id = Column(Integer, primary_key=True, index=True)
name = Column(String, nullable=False)

# Chaque cuisine a son propre template de ticket

ticket_template_id = Column(Integer, ForeignKey("ticket_templates.id"), nullable=True)

template = relationship("TicketTemplate", back_populates="kitchens")
printers = relationship("Printer", secondary=kitchen_printers, back_populates="kitchens")
products = relationship("Product", back_populates="kitchen")
