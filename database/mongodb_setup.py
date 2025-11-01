from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
client = MongoClient(MONGO_URI)
db = client['egg_production']

# Create collections
provinces = db['provinces']
districts = db['districts']
households = db['households']
eggs_production = db['eggs_production']
audit_log = db['audit_log']

# Create indexes
districts.create_index('province_id')
households.create_index('province_id')
households.create_index('district_id')
eggs_production.create_index('household_id')
audit_log.create_index('table_name')

# Define schemas 
province_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['province_name'],
        'properties': {
            'province_name': {
                'bsonType': 'string',
                'description': 'Name of the province'
            }
        }
    }
}

district_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['province_id', 'district_name'],
        'properties': {
            'province_id': {
                'bsonType': 'objectId',
                'description': 'Reference to province'
            },
            'district_name': {
                'bsonType': 'string',
                'description': 'Name of the district'
            }
        }
    }
}

household_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['province_id', 'district_id', 'clust', 'owner', 'household_weight', 'yield', 'produced_eggs_last_six_months'],
        'properties': {
            'province_id': {
                'bsonType': 'objectId',
                'description': 'Reference to province'
            },
            'district_id': {
                'bsonType': 'objectId',
                'description': 'Reference to district'
            },
            'clust': {
                'bsonType': 'int',
                'description': 'Cluster number'
            },
            'owner': {
                'bsonType': 'string',
                'description': 'Name of household owner'
            },
            'household_weight': {
                'bsonType': 'double',
                'description': 'Weight of the household'
            },
            'yield': {
                'bsonType': 'bool',
                'description': 'Whether household has yield'
            },
            'produced_eggs_last_six_months': {
                'bsonType': 'bool',
                'description': 'Egg production in last 6 months'
            }
        }
    }
}

eggs_production_schema = {
    '$jsonSchema': {
        'bsonType': 'object',
        'required': ['household_id', 'month', 'laying_hens', 'eggs_produced', 'eggs_consumed', 'eggs_sold', 'egg_unit_price', 'hatched_eggs', 'eggs_for_other_usages'],
        'properties': {
            'household_id': {
                'bsonType': 'objectId',
                'description': 'Reference to household'
            },
            'month': {
                'bsonType': 'string',
                'description': 'Month of production'
            },
            'laying_hens': {
                'bsonType': 'int',
                'minimum': 0,
                'description': 'Number of laying hens'
            },
            'eggs_produced': {
                'bsonType': 'int',
                'minimum': 0,
                'description': 'Total eggs produced'
            },
            'eggs_consumed': {
                'bsonType': 'int',
                'minimum': 0,
                'description': 'Eggs consumed'
            },
            'eggs_sold': {
                'bsonType': 'int',
                'minimum': 0,
                'description': 'Eggs sold'
            },
            'egg_unit_price': {
                'bsonType': 'int',
                'minimum': 0,
                'description': 'Price per egg'
            },
            'hatched_eggs': {
                'bsonType': 'int',
                'minimum': 0,
                'description': 'Eggs used for hatching'
            },
            'eggs_for_other_usages': {
                'bsonType': 'int',
                'minimum': 0,
                'description': 'Eggs used for other purposes'
            }
        }
    }
}

# Apply schemas
db.command('collMod', 'provinces', validator=province_schema)
db.command('collMod', 'districts', validator=district_schema)
db.command('collMod', 'households', validator=household_schema)
db.command('collMod', 'eggs_production', validator=eggs_production_schema)

print("MongoDB collections and schemas set up successfully!")