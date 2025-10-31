from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Province CRUD operations
@app.post("/provinces/", response_model=schemas.Province)
def create_province(province: schemas.ProvinceCreate, db: Session = Depends(get_db)):
    db_province = models.Province(**province.model_dump())
    db.add(db_province)
    db.commit()
    db.refresh(db_province)
    return db_province

@app.get("/provinces/", response_model=List[schemas.Province])
def read_provinces(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    provinces = db.query(models.Province).offset(skip).limit(limit).all()
    return provinces

@app.get("/provinces/{province_id}", response_model=schemas.Province)
def read_province(province_id: int, db: Session = Depends(get_db)):
    province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    return province

@app.put("/provinces/{province_id}", response_model=schemas.Province)
def update_province(province_id: int, province: schemas.ProvinceCreate, db: Session = Depends(get_db)):
    db_province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if db_province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    for key, value in province.model_dump().items():
        setattr(db_province, key, value)
    db.commit()
    db.refresh(db_province)
    return db_province

@app.delete("/provinces/{province_id}")
def delete_province(province_id: int, db: Session = Depends(get_db)):
    province = db.query(models.Province).filter(models.Province.id == province_id).first()
    if province is None:
        raise HTTPException(status_code=404, detail="Province not found")
    db.delete(province)
    db.commit()
    return {"message": "Province deleted"}

# District CRUD operations
@app.post("/districts/", response_model=schemas.District)
def create_district(district: schemas.DistrictCreate, db: Session = Depends(get_db)):
    db_district = models.District(**district.model_dump())
    db.add(db_district)
    db.commit()
    db.refresh(db_district)
    return db_district

@app.get("/districts/", response_model=List[schemas.District])
def read_districts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    districts = db.query(models.District).offset(skip).limit(limit).all()
    return districts

@app.get("/districts/{district_id}", response_model=schemas.District)
def read_district(district_id: int, db: Session = Depends(get_db)):
    district = db.query(models.District).filter(models.District.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@app.put("/districts/{district_id}", response_model=schemas.District)
def update_district(district_id: int, district: schemas.DistrictCreate, db: Session = Depends(get_db)):
    db_district = db.query(models.District).filter(models.District.id == district_id).first()
    if db_district is None:
        raise HTTPException(status_code=404, detail="District not found")
    for key, value in district.model_dump().items():
        setattr(db_district, key, value)
    db.commit()
    db.refresh(db_district)
    return db_district

@app.delete("/districts/{district_id}")
def delete_district(district_id: int, db: Session = Depends(get_db)):
    district = db.query(models.District).filter(models.District.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    db.delete(district)
    db.commit()
    return {"message": "District deleted"}

# Household CRUD operations
@app.post("/households/", response_model=schemas.Household)
def create_household(household: schemas.HouseholdCreate, db: Session = Depends(get_db)):
    db_household = models.Household(**household.model_dump())
    db.add(db_household)
    db.commit()
    db.refresh(db_household)
    return db_household

@app.get("/households/", response_model=List[schemas.Household])
def read_households(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    households = db.query(models.Household).offset(skip).limit(limit).all()
    return households

@app.get("/households/{household_id}", response_model=schemas.Household)
def read_household(household_id: int, db: Session = Depends(get_db)):
    household = db.query(models.Household).filter(models.Household.id == household_id).first()
    if household is None:
        raise HTTPException(status_code=404, detail="Household not found")
    return household

@app.put("/households/{household_id}", response_model=schemas.Household)
def update_household(household_id: int, household: schemas.HouseholdCreate, db: Session = Depends(get_db)):
    db_household = db.query(models.Household).filter(models.Household.id == household_id).first()
    if db_household is None:
        raise HTTPException(status_code=404, detail="Household not found")
    for key, value in household.model_dump().items():
        setattr(db_household, key, value)
    db.commit()
    db.refresh(db_household)
    return db_household

@app.delete("/households/{household_id}")
def delete_household(household_id: int, db: Session = Depends(get_db)):
    household = db.query(models.Household).filter(models.Household.id == household_id).first()
    if household is None:
        raise HTTPException(status_code=404, detail="Household not found")
    db.delete(household)
    db.commit()
    return {"message": "Household deleted"}

# Egg Production CRUD operations
@app.post("/egg-production/", response_model=schemas.EggProduction)
def create_egg_production(egg_production: schemas.EggProductionCreate, db: Session = Depends(get_db)):
    db_egg_production = models.EggProduction(**egg_production.model_dump())
    db.add(db_egg_production)
    db.commit()
    db.refresh(db_egg_production)
    return db_egg_production

@app.get("/egg-production/", response_model=List[schemas.EggProduction])
def read_egg_productions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    egg_productions = db.query(models.EggProduction).offset(skip).limit(limit).all()
    return egg_productions

@app.get("/egg-production/{egg_production_id}", response_model=schemas.EggProduction)
def read_egg_production(egg_production_id: int, db: Session = Depends(get_db)):
    egg_production = db.query(models.EggProduction).filter(models.EggProduction.id == egg_production_id).first()
    if egg_production is None:
        raise HTTPException(status_code=404, detail="Egg production record not found")
    return egg_production

@app.put("/egg-production/{egg_production_id}", response_model=schemas.EggProduction)
def update_egg_production(egg_production_id: int, egg_production: schemas.EggProductionCreate, db: Session = Depends(get_db)):
    db_egg_production = db.query(models.EggProduction).filter(models.EggProduction.id == egg_production_id).first()
    if db_egg_production is None:
        raise HTTPException(status_code=404, detail="Egg production record not found")
    for key, value in egg_production.model_dump().items():
        setattr(db_egg_production, key, value)
    db.commit()
    db.refresh(db_egg_production)
    return db_egg_production

@app.delete("/egg-production/{egg_production_id}")
def delete_egg_production(egg_production_id: int, db: Session = Depends(get_db)):
    egg_production = db.query(models.EggProduction).filter(models.EggProduction.id == egg_production_id).first()
    if egg_production is None:
        raise HTTPException(status_code=404, detail="Egg production record not found")
    db.delete(egg_production)
    db.commit()
    return {"message": "Egg production record deleted"}