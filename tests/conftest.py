# --- conftest.py is a special (reserved name) file that you can use to provide access to a set of fixtures
# --- that can be accessed by test files without importing them.


# --- Import the required modules:
from app.auth.oauth2 import create_access_token
from app.config import settings
from app.database import get_db, Base
from app.main import app
from app.models import models
from fastapi.testclient import TestClient
from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# --- Create a constant that will be used to point to and pass the user details to our database:
SQLALCHEMY_DATABASE_URL = f"{settings.database_type}://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
print(SQLALCHEMY_DATABASE_URL)

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


@fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@fixture
def authorised_client(fastapi_client, token):
    fastapi_client.headers = {
        **fastapi_client.headers,
        "authorization": f"Bearer {token}"
    }
    return fastapi_client


@fixture
def test_posts(test_user, session):
    # --- Define a variable with a list of dictionaries that 
    posts_data = [{"title": "One",
                   "content": "Content for One.",
                   "owner_id": test_user["id"]
                   },
                  {"title": "Two",
                   "content": "Content for Two.",
                   "owner_id": test_user["id"]
                   },
                  {"title": "Three",
                   "content": "Content for Three.",
                   "owner_id": test_user["id"]
                   }
                  ]
    
    # --- This function will covert the info in each post in post_data 
    # --- into a Post model that can be used to insert into the posts table:
    def create_post_model(post):
        return models.Post(**post)
    
    # --- Use map (iterate over a list without a for loop) to transform 
    # --- the posts_data list into a map of post model compatible data:
    posts_map = map(create_post_model, posts_data)
    
    # --- Convert the map to a list:
    posts = list(posts_map)
    
    # print(posts)
    # --- Commit the data to the posts table:
    session.add_all(posts)
    session.commit()
    
    # --- Get all of the posts in the posts table:
    posts_query = session.query(models.Post).all()
    
    return posts_query