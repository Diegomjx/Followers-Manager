import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = os.getenv("GITHUB_USERNAME")

HEADERS = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github.v3+json"}

# Get the list of followers
def get_followers():
    url = f"https://api.github.com/users/{USERNAME}/followers"
    response = requests.get(url, headers=HEADERS)
    return [user["login"] for user in response.json()] if response.status_code == 200 else []

# Get the list of users you are following
def get_following():
    url = f"https://api.github.com/users/{USERNAME}/following"
    response = requests.get(url, headers=HEADERS)
    return [user["login"] for user in response.json()] if response.status_code == 200 else []

# Follow users who follow you
def follow_users(followers):
    for user in followers:
        url = f"https://api.github.com/user/following/{user}"
        response = requests.put(url, headers=HEADERS)
        if response.status_code in [204, 200]:
            print(f"Following {user}")

# Unfollow users who don't follow you back
def unfollow_users(following, followers):
    not_following_back = set(following) - set(followers)
    for user in not_following_back:
        url = f"https://api.github.com/user/following/{user}"
        response = requests.delete(url, headers=HEADERS)
        if response.status_code in [204, 200]:
            print(f"Unfollowed {user}")

# Run script
followers = get_followers()
following = get_following()

follow_users(followers)
unfollow_users(following, followers)

