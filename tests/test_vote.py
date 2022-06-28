from pytest import mark
from time import sleep

post_id = 1

# --- Define a test to check if an authorised user can vote and un-vote a posts.
# --- HTTP 201, 409 and 201 (in that order) are expected to pass the test:

def test_vote_post_authorised_user(authorised_client, test_posts, test_user):
    url = "/vote/"
    vote_actions = [(1,201,"vote added successfully."),
                    (1,409,f"User has already voted on post {post_id}."),
                    (0,201,"vote removed successfully.")]

    for action in vote_actions:
        vote_post = authorised_client.post(url, json = {"user_id": test_user["id"],
                                                        "post_id": post_id,
                                                        "dir": action[0]})

        assert vote_post.status_code == action[1]

    
# --- Define a test to check if an authorised user can vote on a non-existent post.
# --- HTTP 404 is expected to pass the test:
def test_vote_post_not_exist_authorised_user(authorised_client, test_posts, test_user):
    url = "/vote/"
    vote_post = authorised_client.post(url, json = {"user_id": test_user["id"],
                                                    "post_id": 100,
                                                    "dir": 1})
    
    assert vote_post.status_code == 404
    

# --- Define a test to check if an unauthorised user can vote and un-vote a posts.
# --- HTTP 401 is expected to pass the test:
def test_vote_post_unauthorised_user(fastapi_client, test_posts, test_user):
    url = "/vote/"
    vote_post = fastapi_client.post(url, json = {"user_id": test_user["id"],
                                                    "post_id": post_id,
                                                    "dir": 1})
    
    assert vote_post.status_code == 401

    
# --- Define a test to check if an unauthorised user can vote on a non-existent post.
# --- HTTP 404 is expected to pass the test:
def test_vote_post_not_exist_unauthorised_user(fastapi_client, test_posts, test_user):
    url = "/vote/"
    vote_post = fastapi_client.post(url, json = {"user_id": test_user["id"],
                                                    "post_id": 100,
                                                    "dir": 1})
    
    assert vote_post.status_code == 401