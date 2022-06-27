# --- conftest.py is a special (reserved name) file that you can use to provide access to a set of fixtures
# --- that can be accessed by test files without importing them.


# --- Import the required modules:
from app.config import settings
from app.database import get_db, Base
from app.main import app
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# --- Create a constant that will be used to point to and pass the user details to our database:
SQLALCHEMY_DATABASE_URL = f"{settings.database_type}://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"


# --- Create an engine to connect to the database:
engine = create_engine(SQLALCHEMY_DATABASE_URL)


# --- Create a session to the database:
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @fixture(scope="module")
# --- All of the will run before any of the tests and anything after the yields will run once the tests are completed:
# --- scope in the @fixture will allow the fixture to persist as the module, rather than the defaul of function.
# --- In effect, the tables are deleted and created once, rather than multiple times.

# --- Running with a scope of function will mean it is run each time the function is ran.
# --- If the scope was not set to module, the user would be created and then the table deleted, then the table is
# --- recreated but the user would not. This would mean any tests made with the user (login) would fail.

# --- Ideally, don't change the scope as it can make test become dependant on others passing without any control.
@fixture()
def session():
    # --- Run before any of the tests        
    # --- Drop the tables in the test database:
    Base.metadata.drop_all(bind = engine)
    # --- Create the tables in the test database:
    Base.metadata.create_all(bind = engine)
    
    # --- Execute the connection to the database and close it when finished:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture()
def fastapi_client(session):
    # --- Run before any of the tests
    # --- Basically returns a pytest client to interact with
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    # --- This will override the get_db variable with the override_get_db to use a testing DB instead.
    app.dependency_overrides[get_db] = override_get_db
    
    # --- Return a new FastAPI test client
    yield TestClient(app)
    
    
@fixture
def test_user(fastapi_client):
    user_data = {"email": "sam@sam.sam", 
                 "password": "password123454648945456sddsfdffhgh4"}
    
    res = fastapi_client.post("/user/", json=user_data)

    assert res.status_code == 201
    
    # --- Add the users password to the dictionary:
    new_user = res.json()
    new_user["password"] = user_data["password"]
    
    return new_user