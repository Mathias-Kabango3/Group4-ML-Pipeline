from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base

class Province(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, index=True)
    province_name = Column(String, nullable=False)
    
    districts = relationship("District", back_populates="province")
    households = relationship("Household", back_populates="province")

class District(Base):
    __tablename__ = "districts"

    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(Integer, ForeignKey("provinces.id"))
    district_name = Column(String, nullable=False)
    
    province = relationship("Province", back_populates="districts")
    households = relationship("Household", back_populates="district")

class Household(Base):
    __tablename__ = "households"

    id = Column(Integer, primary_key=True, index=True)
    province_id = Column(Integer, ForeignKey("provinces.id"))
    district_id = Column(Integer, ForeignKey("districts.id"))
    clust = Column(Integer, nullable=False)
    owner = Column(String, nullable=False)
    household_weight = Column(Float, nullable=False)
    yield_field = Column(Boolean, name="yield", nullable=False)
    produced_eggs_last_six_months = Column(Boolean, nullable=False)
    
    province = relationship("Province", back_populates="households")
    district = relationship("District", back_populates="households")
    eggs_production = relationship("EggProduction", back_populates="household")

class EggProduction(Base):
    __tablename__ = "eggs_production"

    id = Column(Integer, primary_key=True, index=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    month = Column(String, nullable=False)
    laying_hens = Column(Integer, nullable=False)
    eggs_produced = Column(Integer, nullable=False)
    eggs_consumed = Column(Integer, nullable=False)
    eggs_sold = Column(Integer, nullable=False)
    egg_unit_price = Column(Integer, nullable=False)
    hatched_eggs = Column(Integer, nullable=False)
    eggs_for_other_usages = Column(Integer, nullable=False)
    
    household = relationship("Household", back_populates="eggs_production")