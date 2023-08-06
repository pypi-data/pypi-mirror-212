ENV = "PRODUCTION"

if ENV == "PRODUCTION":
    HOST = "https://api-develop.solidityscan.com/external/private"
else:
    HOST="http://localhost:5002/private"
