from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine
import seed

models.Base.metadata.create_all(bind=engine)

# app with FastAPI + redocs
app = FastAPI(
    title="Rwandan Egg Production API",
    description="API for managing Rwandan egg production data including provinces, districts, households, and egg production records.",
    version="1.0.0",
    docs_url="/swagger-ui",
    openapi_url="/openapi.json",
    redoc_url="/docs"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/dataset/seed/")
def seed_dataset(db: Session = Depends(get_db)):
    # select all provinces, districts, households, egg productions
    provinces = db.query(models.Province).all()
    districts = db.query(models.District).all()
    households = db.query(models.Household).all()
    egg_productions = db.query(models.EggProduction).all()

    # seed provinces
    for province in seed.rwandan_provinces:
        # existing province from all provinces variable
        db_province = next((p for p in provinces if p.id == province["id"]), None)
        if db_province:
            db_province.province_name = province["province_name"]
        else:
            db_province = models.Province(**province)
            db.add(db_province)
    # Seed districts
    for district in seed.rwandan_districts:
        db_district = next((d for d in districts if d.id == district["id"]), None)
        if db_district:
            db_district.district_name = district["district_name"]
            db_district.province_id = district["province_id"]
        else:
            db_district = models.District(**district)
            db.add(db_district)
    dataset = seed.load_filtered_egg_production_data()
    # seed households
    for household in dataset['households']:
        db_household = next((h for h in households if h.id == household["id"]), None)
        if db_household:
            db_household.province_id = household["province_id"]
            db_household.district_id = household["district_id"]
            db_household.clust = household["clust"]
            db_household.owner = household["owner"]
            db_household.household_weight = household["household_weight"]
            db_household.yield_field = household["yield_field"]
            db_household.produced_eggs_last_six_months = household["produced_eggs_last_six_months"]
        else:
            db_household = models.Household(**household)
            db.add(db_household)

    # seed egg productions
    for egg_production in dataset['egg_productions']:
        db_egg_production = next((e for e in egg_productions if e.id == egg_production["id"]), None)
        if db_egg_production:
            db_egg_production.household_id = egg_production["household_id"]
            db_egg_production.month = egg_production["month"]
            db_egg_production.laying_hens = egg_production["laying_hens"]
            db_egg_production.eggs_produced = egg_production["eggs_produced"]
            db_egg_production.eggs_consumed = egg_production["eggs_consumed"]
            db_egg_production.eggs_sold = egg_production["eggs_sold"]
            db_egg_production.egg_unit_price = egg_production["egg_unit_price"]
            db_egg_production.hatched_eggs = egg_production["hatched_eggs"]
            db_egg_production.eggs_for_other_usages = egg_production["eggs_for_other_usages"]
        else:
            db_egg_production = models.EggProduction(**egg_production)
            db.add(db_egg_production)

    db.commit()
    return {
        "data_count": {
            "provinces": len(seed.rwandan_provinces),
            "districts": len(seed.rwandan_districts),
            "households": len(dataset['households']),
            "egg_productions": len(dataset['egg_productions']),
        },
        "dataset_seeded": True,
        "message": "Dataset seeded successfully"
    }

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

@app.get("/egg-production/", response_model=List[schemas.EggProductionData])
def read_egg_productions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    provinces = db.query(models.Province).all()
    districts = db.query(models.District).all()
    households = db.query(models.Household).all()
    # order by id desc
    egg_productions = db.query(models.EggProduction).order_by(text("id desc")).offset(skip).limit(limit).all()
    result_list = []
    for ep in egg_productions:
        household = next((h for h in households if h.id == ep.household_id), None)
        district = next((d for d in districts if d.id == household.district_id), None) if household else None
        province = next((p for p in provinces if p.id == district.province_id), None) if district else None
        ep_data = {
            "id": ep.id,
            "household_id": ep.household_id,
            "month": ep.month,
            "laying_hens": ep.laying_hens,
            "eggs_produced": ep.eggs_produced,
            "eggs_consumed": ep.eggs_consumed,
            "eggs_sold": ep.eggs_sold,
            "egg_unit_price": ep.egg_unit_price,
            "hatched_eggs": ep.hatched_eggs,
            "eggs_for_other_usages": ep.eggs_for_other_usages,
            "household": {
                "province_id": household.province_id,
                "district_id": household.district_id,
                "clust": household.clust,
                "owner": household.owner,
                "household_weight": household.household_weight,
                "yield_field": household.yield_field,
                "produced_eggs_last_six_months": household.produced_eggs_last_six_months
            },
            "district": {
                "district_name": district.district_name,
                "province_id": district.province_id
            },
            "province": {
                "province_name": province.province_name
            }
        }
        result_list.append(schemas.EggProductionData(**ep_data))
    return result_list

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