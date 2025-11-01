from pydantic import BaseModel
from typing import List, Optional

class ProvinceBase(BaseModel):
    province_name: str

class ProvinceCreate(ProvinceBase):
    pass

class Province(ProvinceBase):
    id: int
    
    class Config:
        from_attributes = True

class DistrictBase(BaseModel):
    district_name: str
    province_id: int

class DistrictCreate(DistrictBase):
    pass

class District(DistrictBase):
    id: int
    
    class Config:
        from_attributes = True

class HouseholdBase(BaseModel):
    province_id: int
    district_id: int
    clust: int
    owner: str
    household_weight: float
    yield_field: bool
    produced_eggs_last_six_months: bool

class HouseholdCreate(HouseholdBase):
    pass

class Household(HouseholdBase):
    id: int
    
    class Config:
        from_attributes = True

class EggProductionBase(BaseModel):
    household_id: int
    month: str
    laying_hens: int
    eggs_produced: int
    eggs_consumed: int
    eggs_sold: int
    egg_unit_price: int
    hatched_eggs: int
    eggs_for_other_usages: int

class EggProductionCreate(EggProductionBase):
    pass

class EggProduction(EggProductionBase):
    id: int
    
    class Config:
        from_attributes = True

class EggProductionData(EggProduction):
    household: HouseholdBase
    district: DistrictBase
    province: ProvinceBase

    class Config:
        from_attributes = True