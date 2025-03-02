#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from dotenv import load_dotenv
from fastapi import FastAPI
import requests
import json
from datetime import datetime


# In[2]:


# Load environment variables
load_dotenv()

credentials = {
    "CLIENT_ID": os.environ.get('CLIENT_ID'),
    "CLIENT_SECRET": os.environ.get('CLIENT_SECRET'),
    "ACCESS_TOKEN_1": os.environ.get('ACCESS_TOKEN'),
    "ACCESS_TOKEN_2": os.environ.get('ACCESS_TOKEN_2'),
    "USER_1": os.environ.get('USER_1'),
    "USER_2": os.environ.get('USER_2')
}


# In[28]:


## CODE FOR TESTING
#url = "https://www.linkedin.com/oauth/v2/introspectToken"

#data = {
#    "token": credentials['ACCESS_TOKEN_2'],
#    "client_id": credentials['CLIENT_ID'],  # Your LinkedIn app's client ID
#    "client_secret": credentials['CLIENT_SECRET']  # Your LinkedIn app's client secret
#}

#headers = {
#    "Content-Type": "application/x-www-form-urlencoded"
#}

#response = requests.post(url, headers=headers, data=data)

#print(response.status_code, response.json())
#url = "https://api.linkedin.com/v2/userinfo"
#headers = {"Authorization": f"Bearer {credentials['ACCESS_TOKEN_2']}"}
#response = requests.get(url, headers=headers)
#print(response.status_code, response.json())


# In[29]:


# Define the path to your JSON file
json_file_path = os.path.join('data', 'scheduled_posts.json')

# Load the JSON data
with open(json_file_path, 'r', encoding='utf-8') as file:
    scheduled_posts = json.load(file)

#print(scheduled_posts)


# In[13]:


def create_linkedin_post(user_urn, access_token, post_text):
    url = "https://api.linkedin.com/v2/ugcPosts"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }
    
    post_data = {
        "author": user_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    response = requests.post(url, headers=headers, json=post_data)
    
    if response.status_code == 201:
        return response.json()  # Return the response if successful
    else:
        raise Exception(f"Error creating post: {response.status_code} - {response.text}")
# Example usage:
#create_linkedin_post(credentials['USER_1'], credentials['ACCESS_TOKEN_1'], "Hello LinkedIn! This is an automated post using the LinkedIn API.")
#create_linkedin_post(credentials['USER_2'], credentials['ACCESS_TOKEN_2'], "Hello LinkedIn! This is another automated post!")


# In[10]:


# Function to check and post on the current date
def check_and_post():
    today = datetime.now().date().isoformat()
    for user_id, posts in scheduled_posts.items():
        for post in posts:
            if post["date"] == today:
                content = post["content"]
                # Ensure content is a string, even if it's a list
                if isinstance(content, list):
                    content = "\n".join(
                        content[:1] +  # Keep the first item unchanged (e.g., "Test Post:")
                        [line if not line.startswith("- ") else f"• {line[2:]}" for line in content[1:]]
                    )
                access_token = credentials['ACCESS_TOKEN_1'] if user_id == "USER_1" else credentials['ACCESS_TOKEN_2']
                user_urn = credentials['USER_1'] if user_id == "USER_1" else credentials['USER_2']
                try:
                    create_linkedin_post(user_urn, access_token, content)
                    return f"Success: Post created for {user_id} on {today}"
                except Exception as e:
                    return f"Failure: Error posting for {user_id} on {today} - {e}"
    return "No posts scheduled for today"


# In[27]:


log_file = os.path.join('data', 'scheduler_log.txt')

def log_message(message):
    with open(log_file, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")

try:
    for user_id, posts in scheduled_posts.items():
        for post in posts:
            try:
                today = datetime.now().date().isoformat()
                if post["date"] == today:
                    content = post["content"]
                    
                    # Ensure content is a string, even if it's a list
                    if isinstance(content, list):
                        content = "\n".join(
                            content[:1] +  
                            [line if not line.startswith("- ") else f"• {line[2:]}" for line in content[1:]]
                        )

                    access_token = credentials['ACCESS_TOKEN_1'] if user_id == "USER_1" else credentials['ACCESS_TOKEN_2']
                    user_urn = credentials['USER_1'] if user_id == "USER_1" else credentials['USER_2']

                    response = create_linkedin_post(user_urn, access_token, content)
                    
                    log_message(f"Success: Posted for {user_id}")

            except Exception as post_error:
                description = "Run local copy to get full error log"
                log_message(f"Error posting for {user_id}: {description}")
                
except Exception as e:
    log_message(f"Failure: Exception occurred - {e}")

