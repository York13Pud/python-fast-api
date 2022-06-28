# from pytest import mark

# # --- Define a function to create a number of posts:
# @mark.parametrize("title, content, published, status_code", [
#     ("wrongemail@gmail.com", "password123", 403),
#     ("wrongemail@gmail.com", "wrongpassword", 403),
#     ("wrongemail@gmail.com", "wrongpassword", 403),
#     ("wrongemail@gmail.com", None, 422),
#     (None, "password123", 422)
# ])


# def test_post_articles(authorised_client, title, content, published, status_code):
#     res = authorised_client.post("/login", 
#                     data={"title": title,
#                         "content": content,
#                         "published": published
#                         })
    
#     assert res.status_code == status_code


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
def test_get_one_post_not_logged_in(fastapi_client, test_posts):
    res = fastapi_client.get("/post/1/")
    res_message = res.json()
    
    assert res_message["Post"]["id"] == 1
    assert res.status_code == 200
    
# --- Define a test to check if the user can retrieve a single posts.
# --- HTTP 200 is expected to pass the test:
def test_get_one_post_logged_in(authorised_client, test_posts):
    res = authorised_client.get("/post/1/")
    res_message = res.json()
    
    assert res_message["Post"]["id"] == 1
    assert res.status_code == 200