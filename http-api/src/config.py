import os
from dotenv import load_dotenv

load_dotenv()

RUNNING_IN_DOCKER = os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true"

class Config:
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "9000"))
    TESTING = os.getenv("TESTING", "false").lower() == "true"

    VM_SERVICE_URL = os.getenv("VM_SERVICE_DOCKER_URL") if RUNNING_IN_DOCKER else os.getenv("VM_SERVICE_LOCAL_URL")
    DATABASE_URL = os.getenv("POSTGRES_DOCKER_URL") if RUNNING_IN_DOCKER else os.getenv("POSTGRES_LOCAL_URL")
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
