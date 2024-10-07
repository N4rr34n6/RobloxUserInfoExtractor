import requests
import json
from bs4 import BeautifulSoup
import random
import time
import csv
import argparse

def get_user_agent():
    # List of user agents to randomize requests
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    ]
    return random.choice(user_agents)

def request_with_retries(url, headers, max_retries=None):
    retries = 0
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 429:
            wait_time = int(response.headers.get('Retry-After', 5))
            time.sleep(wait_time)
            retries += 1
        else:
            if max_retries and retries >= max_retries:
                return None
            retries += 1
            time.sleep(5)

def search_by_username(username):
    url = f"https://users.roblox.com/v1/users/search?keyword={username}&limit=10"
    headers = {'User-Agent': get_user_agent()}
    response = request_with_retries(url, headers)
     
    if response.status_code == 200:
        data = response.json()
        if data['data']:
            return data['data'][0]['id']
   
    return None

def get_previous_usernames(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}/username-history?limit=100&sortOrder=Asc"
    headers = {'User-Agent': get_user_agent()}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return [entry['name'] for entry in data['data']]
    
    return []

def get_groups(user_id):
    url = f"https://groups.roblox.com/v2/users/{user_id}/groups/roles"
    headers = {'User-Agent': get_user_agent()}
    response = requests.get(url, headers=headers)
    
    groups = []
    if response.status_code == 200:
        data = response.json()
        for group in data['data']:
            groups.append({
                'name': group['group']['name'],
                'link': f"https://www.roblox.com/groups/{group['group']['id']}",
                'members': group['group']['memberCount']
            })
    
    return groups

def get_about_me(user_id):
    url = f"https://www.roblox.com/users/{user_id}/profile"
    headers = {'User-Agent': get_user_agent()}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        about_me = soup.find('span', class_='profile-about-content-text linkify')
        if about_me:
            return about_me.text.strip()
        else:
            about_me_div = soup.find('div', class_='profile-about-content')
            if about_me_div:
                about_me_span = about_me_div.find('span')
                if about_me_span:
                    return about_me_span.text.strip()
    
    return "Not available"

def get_entity_list(user_id, entity_type):
    entities = set()  
    cursor = ""
    
    while True:
        url = f"https://friends.roblox.com/v1/users/{user_id}/{entity_type}?limit=100&cursor={cursor}"
        headers = {'User-Agent': get_user_agent()}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            for entity in data['data']:
                entities.add((entity['name'], f"https://www.roblox.com/users/{entity['id']}/profile"))
            
            cursor = data.get('nextPageCursor')
            if not cursor:
                break  
        else:
            break
        
        time.sleep(1)  
    
    return [{'name': name, 'url': url} for name, url in entities]

def get_user_info(identifier):
    if identifier.isdigit():
        user_id = identifier
    else:
        user_id = search_by_username(identifier)
   
    if not user_id:
        return None
   
    user_url = f"https://users.roblox.com/v1/users/{user_id}"
    headers = {'User-Agent': get_user_agent()}
    user_response = requests.get(user_url, headers=headers)
   
    if user_response.status_code == 200:
        user_data = user_response.json()
       
        friends_url = f"https://friends.roblox.com/v1/users/{user_id}/friends/count"
        friends_response = requests.get(friends_url, headers=headers)
        friends_count = friends_response.json()['count'] if friends_response.status_code == 200 else 0
       
        followers_url = f"https://friends.roblox.com/v1/users/{user_id}/followers/count"
        followings_url = f"https://friends.roblox.com/v1/users/{user_id}/followings/count"
        followers_response = requests.get(followers_url, headers=headers)
        followings_response = requests.get(followings_url, headers=headers)
        followers_count = followers_response.json()['count'] if followers_response.status_code == 200 else 0
        followings_count = followings_response.json()['count'] if followings_response.status_code == 200 else 0
       
        previous_usernames = get_previous_usernames(user_id)
        groups = get_groups(user_id)
        about_me = get_about_me(user_id)
        friends = get_entity_list(user_id, "friends")
        followers = get_entity_list(user_id, "followers")
        followings = get_entity_list(user_id, "followings")
        
        return {
            'user_id': user_id,
            'alias': user_data['name'],
            'display_name': user_data['displayName'],
            'description': user_data.get('description', ''),
            'is_banned': user_data.get('isBanned', False),
            'has_verified_badge': user_data.get('hasVerifiedBadge', False),
            'friends': friends_count,
            'followers': followers_count,
            'following': followings_count,
            'join_date': user_data['created'],
            'previous_usernames': previous_usernames,
            'groups': groups,
            'about_me': about_me,
            'friends_list': friends,
            'followers_list': followers,
            'following_list': followings
        }
   
    return None

def export_to_csv(data, filename):
    # Export data to a CSV file with specified filename
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter='|')
        for row in data:
            writer.writerow(row)

def main():
    # Parse command line arguments for user identifier
    parser = argparse.ArgumentParser(description='Get information about a Roblox user.')
    parser.add_argument('identifier', help='Roblox username or ID')
    args = parser.parse_args()

    user_info = get_user_info(args.identifier)
   
    if user_info:
        print(f"User ID: {user_info['user_id']}")
        print(f"Alias: {user_info['alias']}")
        print(f"Display Name: {user_info['display_name']}")
        print(f"Description: {user_info['description']}")
        print(f"Banned: {'Yes' if user_info['is_banned'] else 'No'}")
        print(f"Verified Badge: {'Yes' if user_info['has_verified_badge'] else 'No'}")
        print(f"Friends: {user_info['friends']}")
        print(f"Followers: {user_info['followers']}")
        print(f"Following: {user_info['following']}")
        print(f"Join Date: {user_info['join_date']}")
        print(f"Previous Usernames: {', '.join(user_info['previous_usernames']) if user_info['previous_usernames'] else 'None detected'}")
        print(f"\nAbout Me: {user_info['about_me']}")
        
        print("\nGroups:")
        groups_data = [['Name', 'Link', 'Members']]
        for group in user_info['groups']:
            print(f"- {group['name']} ({group['members']} members)")
            print(f"  Link: {group['link']}")
            groups_data.append([group['name'], group['link'], str(group['members'])])
        
        export_to_csv(groups_data, 'groups.csv')
        print("\nGroup information exported to 'groups.csv'")

        for list_type in ['friends', 'followers', 'following']:
            entity_data = user_info[f"{list_type}_list"]
            list_data = [[list_type.capitalize(), 'Link']]
            for entity in entity_data:
                list_data.append([entity['name'], entity['url']])
            export_to_csv(list_data, f"{list_type}.csv")
            print(f"{list_type.capitalize()} list exported to '{list_type}.csv'")
        
    else:
        print("User not found.")

if __name__ == '__main__':
    main()
