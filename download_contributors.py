import requests
import pandas as pd

def fetch_commit_authors(owner, repo, token):
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    query = """
    query($owner: String!, $name: String!, $since: GitTimestamp!, $after: String) {
      repository(owner: $owner, name: $name) {
        defaultBranchRef {
          target {
            ... on Commit {
              history(first: 100, after: $after, since: $since) {
                pageInfo {
                  endCursor
                  hasNextPage
                }
                edges {
                  node {
                    author {
                      email
                      name
                      user {
                        login
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    has_next_page = True
    after_cursor = None
    all_authors = {}

    while has_next_page:
      print(f"Fetching commits after cursor {after_cursor}")
      variables = {
          "owner": owner,
          "name": repo,
          "after": after_cursor,
          "since": since
      }

      print(f"Querying GitHub API for {owner}/{repo} repository")

      response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
      if response.status_code == 200:
          result = response.json()
          history = result['data']['repository']['defaultBranchRef']['target']['history']
          for edge in history['edges']:
              node = edge['node']
              author_email = node['author']['email']
              author_name = node['author']['name']
              author_login = node['author']['user']['login'] if node['author']['user'] else None
              if author_email not in all_authors:
                  all_authors[author_email] = {
                      "name": author_name,
                      "login": author_login,
                      "email": author_email
                  }
          after_cursor = history['pageInfo']['endCursor']
          has_next_page = history['pageInfo']['hasNextPage']
      else:
          raise Exception(f"Query failed with code {response.status_code}: {response.text}")

    return all_authors

# Usage
owner = "apache"  # Replace with the owner of the repository
repo = "superset"  # Replace with the name of the repository
repo_name = f"{owner}_{repo}"
token = "YOUR_GITHUB_API_TOKEN"  # Replace
since = "2024-01-01T00:00:00Z"  # Start date in ISO 8601 format

authors = fetch_commit_authors(owner, repo, token)


# create empty dataframe to store the data with column names as repo_name, author_login, author_name, author_email
df = pd.DataFrame(columns=['repo_name', 'author_login', 'author_name', 'author_email'])

for email, author in authors.items():
  print(f"Login: {author['login']}, Name: {author['name']}, Email: {author['email']}")
  
  author_data = {
      'repo_name': repo,
      'author_login': author['login'],
      'author_name': author['name'],
      'author_email': author['email']
  }

  # print(author_data)
  df = pd.concat([df, pd.DataFrame([author_data])], ignore_index=True)
  df.to_csv(f'{repo_name}_contributors.csv', index=False)