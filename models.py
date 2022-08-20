
from sqlalchemy import ForeignKey, Integer, String, Float, Date, DateTime
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship

from database import Base


class Target(Base):
    __tablename__ = "revenue_target"

    sno=Column(Integer, primary_key=True, autoincrement=True, index=True)
    branch=Column(String(100), index=True)
    target = Column(Float, index=True)
    Ach = Column(Float, unique=True, index=True)
    Archp = Column(Float, index=True)
    Archo = Column(Float, index=True)
    clustername = Column(String(100), index=True)
    status = Column(String(100), index=True)

    targets= relationship("Adm", back_populates="owner")

class Adm(Base):
    __tablename__= "adm_revenue"

    sno = Column(Integer, primary_key=True, autoincrement=True, index=True)
    unit = Column(String(100), index=True)
    total_net_revenue = Column(Integer, index=True)
    branch = Column(Integer , unique=True, index=True)
    rdate = Column(Date(), index=True)
    dateon = Column(DateTime(timezone=True))

    branch_id = Column(Integer, ForeignKey("revenue_target.sno"))
    owner = relationship("Target", back_populates="targets")



