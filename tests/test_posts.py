from app.schemas import PostResponse
from pytest import mark


# --- Define a function to get all of the posts
# --- HTTP 200 is expected to pass the test:
def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/post/")
        
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200


# --- Define a test to check if the user is not logged in when retrieving a users posts.
# --- HTTP 401 is expected to pass the test:
def test_unauthorised_get_my_posts(fastapi_client, test_posts):
    res = fastapi_client.get("/post/my-posts/")
    res_message = res.json()
    
    assert res_message["detail"] == "Not authenticated"
    assert res.status_code == 401


# --- Define a test to check if the user can retrieve a single posts.
# --- HTTP 200 is expected to pass the test:
def test_get_one_post(fastapi_client, test_posts):
    res = fastapi_client.get("/post/1/")
    res_message = res.json()
    
    assert res_message["Post"]["id"] == 1
    assert res.status_code == 200


# --- Define a test to check if a single posts does not exist.
# --- HTTP 404 is expected to pass the test:
def test_get_one_post_not_exist(fastapi_client, test_posts):
    post_id = 100
    res = fastapi_client.get(f"/post/{post_id}/")
    res_message = res.json()
    
    assert res_message["detail"] == f"Post ID {post_id} not found"
    assert res.status_code == 404


# --- Define a test to check if the user can retrieve a single posts.
# --- HTTP 200 is expected to pass the test:
def test_get_one_post_logged_in(authorised_client, test_posts):
    res = authorised_client.get("/post/1/")
    res_message = res.json()
    
    assert res_message["Post"]["id"] == 1
    assert res.status_code == 200
    

# --- Define a test to see if an authorised user can create a series of posts.
# --- HTTP 200 is expected to pass the test:

@mark.parametrize("title, content, published", [("Fourth", "Fourth content.", True),
                                     ("Fifth", "Fifth content.", True),
                                     ("Sixth", "Sixth content.", False),
                                     ])

def test_create_post(authorised_client, test_posts, title, content, published):
    res = authorised_client.post("/post/", json = {"title": title,
                                                   "content": content,
                                                   "published": published })
    
    created_post = PostResponse(**res.json())
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert res.status_code == 201


# --- Define a test to see if an unauthorised user can create a series of posts.
# --- HTTP 401 is expected to pass the test:
def test_create_post_unauthorised(fastapi_client, test_posts):
    res = fastapi_client.post("/post/", json = {"title": "Not authorised",
                                                   "content": "Not authorised content",
                                                   "published": False })

    res_message = res.json()
    
    assert res_message["detail"] == "Not authenticated"
    assert res.status_code == 401


# --- Define a test to check if an authorised user can delete a single posts.
# --- HTTP 204, followed by 404 are expected to pass the test:
def test_delete_post_authorised_user(authorised_client, test_posts):
    url = "/post/1"
    delete_post = authorised_client.delete(url)
    check_url = authorised_client.get(url)
    
    assert delete_post.status_code == 204  
    assert check_url.status_code == 404
 

# --- Define a test to check if an unauthorised user can delete a single posts.
# --- HTTP 204, followed by 404 are expected to pass the test:
def test_delete_post_unauthorised_user(fastapi_client, test_posts):
    url = "/post/1"
    delete_post = fastapi_client.delete(url)
    res_message = delete_post.json()
    
    assert res_message["detail"] == "Not authenticated"
    assert delete_post.status_code == 401
    

# --- Define a test to check if an authorised user can delete a single posts.
# --- HTTP 204, followed by 404 are expected to pass the test:
def test_delete_post_not_exist_authorised_user(authorised_client, test_posts):
    url = "/post/100"
    delete_post = authorised_client.delete(url)
    
    assert delete_post.status_code == 404