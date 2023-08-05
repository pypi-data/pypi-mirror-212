import requests

def get_project_stats(projectId):
    response = requests.get(f"https://api.scratch.mit.edu/projects/{projectId}")
    print(f"Getting statistics from https://scratch.mit.edu/projects/{projectId}. This can take up a few seconds.")

    stats = response.json()
    if response.status_code == 200:
        print(f"Sucessfully got project {projectId}")
    else:
        print(f"ERROR 404: project {projectId} does not exist. Please verify project ID.")

    print("---------------------------RESULTS---------------------------------")

    if response.status_code == 200:
        title = stats["title"]
        views = stats["stats"]["views"]
        loves = stats["stats"]["loves"]
        favs = stats["stats"]["favorites"]
        author = stats["author"]["username"]
        author = stats["author"]["username"]
        
        print("Title:", title, "By:", author)
        print("Views:", views)
        print("Loves:", loves)
        print("Favs:", favs)
        print("Author:", author)
    else:
        print(response.status_code)


def get_user_stats(username):
    response = requests.get(f"https://api.scratch.mit.edu/users/{username}")
    print(f"Getting statistics from user {username}. This can take up a few seconds.")

    stats = response.json()
    if response.status_code == 200:
        print(f"Sucessfully got user {username}")
    else:
        print(f"ERROR 404: User {username} does not exist. Please verify username.")

    print("---------------------------RESULTS---------------------------------")

    if response.status_code == 200:
        country = stats["profile"]["country"]
        profileId = stats["profile"]["id"]
        joiningDate = str(stats["history"]["joined"])[:4]
        
        print("Country:", country)
        print("Profile ID:", profileId)
        print("Joining year:", joiningDate)
    else:
        print(response.status_code)