import os
import time
import json
import requests

github_api_token = "YOUR-GITHUB-API-TOKEN"

def fetch_issue_or_pr_thread(repo_name, number):
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'Bearer {github_api_token}'
    }
    
    issue_url = f'https://api.github.com/repos/{repo_name}/issues/{number}'
    comments_url = f'https://api.github.com/repos/{repo_name}/issues/{number}/comments'
    
    issue_response = requests.get(issue_url, headers=headers)
    comments_response = requests.get(comments_url, headers=headers)
    
    if issue_response.status_code == 200 and comments_response.status_code == 200:
        issue_data = issue_response.json()
        comments_data = comments_response.json()
        
        # Combine issue or pull request details with its comments
        thread = {
            "issue": issue_data,
            "comments": comments_data
        }
        
        return thread
    else:
        print(f"Failed to fetch data: Issue response status code: {issue_response.status_code}, Comments response status code: {comments_response.status_code}")
        return None

def get_repo_path(repo_name):
    return f'data/{repo_name.replace("/", "-")}'

def save_issues_to_file(repo_name, number):
    thread = fetch_issue_or_pr_thread(repo_name, number)

    if not thread:
        print(f"[ERROR] Failed to fetch thread {repo_name}/{number}")
        return
    
    thread_folder_path = get_repo_path(repo_name)

    if not os.path.exists(thread_folder_path):
        os.makedirs(thread_folder_path)
    
    thread_path = f'{thread_folder_path}/thread_{number}.json'

    with open(thread_path, 'w') as f:
        json.dump(thread, f, indent=2)

    print(f"Saved thread to {thread_path}")


if __name__ == "__main__":
    repo_name = 'microsoft/fluentui' # Repository to download threads from
    thread_folder_path = get_repo_path(repo_name)

    if not os.path.exists(thread_folder_path):
        os.makedirs(thread_folder_path)

    thread_files = os.listdir(thread_folder_path)
    thread_numbers = [int(f.split('_')[1].split('.')[0]) for f in thread_files]

    last_downloaded_thread_number = max(thread_numbers) if thread_numbers else 0
    last_thread_number = 27040 # Last thread number in the repository

    print(f"Last thread number: {last_downloaded_thread_number}")

    for i in range(last_downloaded_thread_number + 1, last_thread_number + 1):
        save_issues_to_file(repo_name, i)
        time.sleep(1)
