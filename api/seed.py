import pandas as pd

rwandan_provinces = [
    {"id": 1, "province_name": "Kigali"},
    {"id": 2, "province_name": "North"},
    {"id": 3, "province_name": "South"},
    {"id": 4, "province_name": "East"},
    {"id": 5, "province_name": "West"},
]

rwandan_districts = [
    {"id": 1, "province_id": 1, "district_name": "Gasabo"},
    {"id": 2, "province_id": 1, "district_name": "Kicukiro"},
    {"id": 3, "province_id": 1, "district_name": "Nyarugenge"},
    {"id": 4, "province_id": 2, "district_name": "Musanze"},
    {"id": 5, "province_id": 2, "district_name": "Burera"},
    {"id": 6, "province_id": 2, "district_name": "Gakenke"},
    {"id": 7, "province_id": 2, "district_name": "Rulindo"},
    {"id": 8, "province_id": 2, "district_name": "Gicumbi"},
    {"id": 9, "province_id": 3, "district_name": "Gisagara"},
    {"id": 10, "province_id": 3, "district_name": "Huye"},
    {"id": 11, "province_id": 3, "district_name": "Kamonyi"},
    {"id": 12, "province_id": 3, "district_name": "Muhanga"},
    {"id": 13, "province_id": 3, "district_name": "Nyamagabe"},
    {"id": 14, "province_id": 3, "district_name": "Nyanza"},
    {"id": 15, "province_id": 3, "district_name": "Nyaruguru"},
    {"id": 16, "province_id": 3, "district_name": "Ruhango"},
    {"id": 17, "province_id": 4, "district_name": "Bugesera"},
    {"id": 18, "province_id": 4, "district_name": "Gatsibo"},
    {"id": 19, "province_id": 4, "district_name": "Kayonza"},
    {"id": 20, "province_id": 4, "district_name": "Kirehe"},
    {"id": 21, "province_id": 4, "district_name": "Ngoma"},
    {"id": 22, "province_id": 4, "district_name": "Nyagatare"},
    {"id": 23, "province_id": 4, "district_name": "Rwamagana"},
    {"id": 24, "province_id": 5, "district_name": "Karongi"},
    {"id": 25, "province_id": 5, "district_name": "Ngororero"},
    {"id": 26, "province_id": 5, "district_name": "Nyabihu"},
    {"id": 27, "province_id": 5, "district_name": "Nyamasheke"},
    {"id": 28, "province_id": 5, "district_name": "Rubavu"},
    {"id": 29, "province_id": 5, "district_name": "Rusizi"},
    {"id": 30, "province_id": 5, "district_name": "Rutsiro"},
]

def load_filtered_egg_production_data(file_path: str = "../model/filtered_egg_production_data.csv"):
    df = pd.read_csv(file_path)
    print(f"seed/loaded filtered egg production data with shape {df.shape}")

    # household data
    households = df[['hhid', 'province', 'district', 'clust', 'owner', 'weight', 's11q2_0', 's11q2_1']]
    # merge duplicates based on hhid and average weight for duplicates
    households = households.groupby(['hhid', 'province', 'district', 'clust', 'owner', 's11q2_0', 's11q2_1'], as_index=False).agg({'weight': 'mean'})

    households = households.rename(columns={
        'hhid': 'id',
        'weight': 'household_weight',
        's11q2_0': 'yield_field',
        's11q2_1': 'produced_eggs_last_six_months'
    })
    households["id"] = households["id"].astype(int)
    households['clust'] = households['clust'].astype(int)
    households['yield_field'] = households['yield_field'].astype(bool)
    households['produced_eggs_last_six_months'] = households['produced_eggs_last_six_months'].astype(bool)
    province_name_to_id = {prov['province_name']: prov['id'] for prov in rwandan_provinces}
    district_name_to_id = {dist['district_name']: dist['id'] for dist in rwandan_districts}
    households['province'] = households['province'].map(province_name_to_id)
    households['district'] = households['district'].map(district_name_to_id)
    households = households.rename(columns={
        'province': 'province_id',
        'district': 'district_id',
    })
    households["owner"] = households["owner"].astype(str)
    households["province_id"] = households["province_id"].astype(int)
    households["district_id"] = households["district_id"].astype(int)

    # eggs productions data
    egg_productions = df[['hhid', 's11q2_2', 's11q2_3', 's11q2_4', 's11q2_5', 's11q2_6', 's11q2_7', 's11q2_8', 's11q2_9']]
    egg_productions = egg_productions.rename(columns={
        'hhid': 'household_id',
        's11q2_2': 'month',
        's11q2_3': 'laying_hens',
        's11q2_4': 'eggs_produced',
        's11q2_5': 'eggs_consumed',
        's11q2_6': 'eggs_sold',
        's11q2_7': 'egg_unit_price',
        's11q2_8': 'hatched_eggs',
        's11q2_9': 'eggs_for_other_usages'
    })
    egg_productions["household_id"] = egg_productions["household_id"].astype(int)
    egg_productions["laying_hens"] = egg_productions["laying_hens"].astype(int)
    egg_productions["eggs_produced"] = egg_productions["eggs_produced"].astype(int)
    egg_productions["eggs_consumed"] = egg_productions["eggs_consumed"].astype(int)
    egg_productions["eggs_sold"] = egg_productions["eggs_sold"].astype(int)
    egg_productions['month'] = egg_productions['month'].str.strip()

    # fill missing egg_unit_price with 0
    egg_productions["egg_unit_price"] = egg_productions["egg_unit_price"].fillna(0)
    egg_productions["egg_unit_price"] = egg_productions["egg_unit_price"].astype(int)

    egg_productions["hatched_eggs"] = egg_productions["hatched_eggs"].astype(int)
    egg_productions["eggs_for_other_usages"] = egg_productions["eggs_for_other_usages"].astype(int)

    # create unique id int for egg production based on index, month to int and household_id
    egg_productions['id'] = (egg_productions.index + 1).astype(int)

    egg_productions = egg_productions[['id', 'household_id', 'month', 'laying_hens', 'eggs_produced', 'eggs_consumed', 'eggs_sold', 'egg_unit_price', 'hatched_eggs', 'eggs_for_other_usages']]

    return {
        "households": households.to_dict(orient='records'),
        "egg_productions": egg_productions.to_dict(orient='records'),
    }