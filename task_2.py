# Instructions:
# Connect to a MongoDB server running on localhost.
# Create a new database named 'exercise_db' and a collection named 'exercise_collection'.
# Define the following JSON schema validation rules for the collection:
# The document must be an object.
# The 'name' field is required and must be a string.
# The 'age' field is required and must be an integer between 18 and 99.
# The 'email' field is required and must be a string containing a valid email address.
# Insert three documents into the collection, one that satisfies the validation rules and two that violate the validation rules.
# Print all the documents in the collection.
# Clean up by dropping the collection and closing the MongoDB connection.

from pymongo import MongoClient
from pymongo.errors import OperationFailure

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["shopping_db"]
collection = db["shopping_collection"]

# Define the validation rules as a dictionary
validation_rules = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "name",
                "age",
                "email",
                "address",
            ],
            "properties": {
                "name": {"bsonType": "string", "description": "Name must be a string."},
                "age": {
                    "bsonType": "int",
                    "minimum": 18,
                    "maximum": 99,
                    "description": "Age must be an integer between 18 and 99.",
                },
                "email": {
                    "bsonType": "string",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                    "description": "Email must be a valid email address.",
                },
                "address": {
                    "bsonType": "object",
                    "required": ["street", "city", "postal_code"],
                    "properties": {
                        "street": {"bsonType": "string"},
                        "city": {"bsonType": "string"},
                        "postal_code": {"bsonType": "string"},
                    },
                },
            },
        }
    }
}

# Set the validation rules for the collection
try:
    new_collection = db.create_collection(name="shopping_collection")
    db.command("collMod", new_collection.name, **validation_rules)
    print("Schema validation enabled.")
    document = {
        "name": "Albert",
        "age": 19,
        "email": "albert@gmail.com",
        "address": {"street": "Vilniaus", "city": "Vilnius", "postal_code": "LT-71671"},
    }
    result = collection.insert_one(document)
except OperationFailure as e:
    print(f"Failed to enable schema validation: {e.details['errmsg']}")


# result = collection.find({}, {"_id": 0})
# for x in result:
#     print(x)

# Clean up (optional)
# collection.drop()
client.close()
