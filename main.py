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
    followers = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{USERNAME}/followers?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        followers.extend([user["login"] for user in data])
        page += 1
    return followers

# Get all users you are following using pagination
def get_following():
    following = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{USERNAME}/following?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            break
        data = response.json()
        if not data:
            break
        following.extend([user["login"] for user in data])
        page += 1
    return following

# Follow users who follow you
def follow_users(followers):
    for user in followers:
        url = f"https://api.github.com/user/following/{user}"
        response = requests.put(url, headers=HEADERS)
        if response.status_code in [204, 200]:
            print(f"Following {user}")

# Unfollow users who don't follow you back
def unfollow_users(following, followers):
    optional = " "
    print(f"Following: {len(following)}")
    print(f"Followers: {len(followers)}")

    not_following_back = set(following) - set(followers)

    for user in not_following_back:
        url = f"https://api.github.com/user/following/{user}"

        if optional != "O":  # Evitar preguntar en cada iteración si "O" fue seleccionado antes
            optional = input(f"Do you want to unfollow {user}?\n[Y]: Yes, [N]: No, [O]: Unfollow all ").strip().upper()

        if optional in ["Y", "O"]:
            response = requests.delete(url, headers=HEADERS)
            if response.status_code in [204, 200]:
                print(f"Unfollowed {user}")
            else:
                print(f"Failed to unfollow {user}: {response.status_code} - {response.text}")

while True:
    print("OPTIONS")
    print("1. Follow users who follow you")
    print("2. Unfollow users who don't follow you back")
    print("3. Show followers")
    print("4. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        followers = get_followers()
        follow_users(followers)
    elif choice == "2":
        followers = get_followers()
        following = get_following()
        unfollow_users(following, followers)
    elif choice == "3":
        followers = get_followers()
        print(followers)
    elif choice == "4":
        break
