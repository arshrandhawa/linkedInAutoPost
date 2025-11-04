#!/usr/bin/env python
# coding: utf-8

import os
from dotenv import load_dotenv
from fastapi import FastAPI
import requests
import json
from datetime import datetime
import traceback


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

# Define log file paths
log_file = os.path.join('data', 'scheduler_log.txt')
debug_log_file = os.path.join('data', 'debuglog.txt')

def log_message(message):
    """Log to scheduler_log.txt"""
    with open(log_file, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")

def debug_log(message, error=None):
    """Log to debuglog.txt with detailed information"""
    with open(debug_log_file, "a") as log:
        if error:
            log.write(f"{datetime.now()} - {message}\n")
            log.write(f"  Error: {error}\n")
            log.write(f"  Traceback: {traceback.format_exc()}\n")
        else:
            log.write(f"{datetime.now()} - {message}\n")
        log.write("---\n")

# Load JSON data with debug logging
try:
    json_file_path = os.path.join('data', 'scheduled_posts.json')
    debug_log(f"Attempting to load JSON from: {json_file_path}")
    
    with open(json_file_path, 'r', encoding='utf-8') as file:
        scheduled_posts = json.load(file)
    
    debug_log(f"✅ JSON loaded successfully")
    debug_log(f"USER_1 posts count: {len(scheduled_posts.get('USER_1', []))}")
    debug_log(f"USER_2 posts count: {len(scheduled_posts.get('USER_2', []))}")
    
except FileNotFoundError as e:
    debug_log(f"❌ JSON file not found", e)
except json.JSONDecodeError as e:
    debug_log(f"❌ JSON parsing error", e)
except Exception as e:
    debug_log(f"❌ Unexpected error loading JSON", e)


def create_linkedin_post(user_urn, access_token, post_text):
    """Create a LinkedIn post"""
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
    
    debug_log(f"Posting to LinkedIn with user_urn: {user_urn}")
    
    response = requests.post(url, headers=headers, json=post_data)
    
    debug_log(f"Response status code: {response.status_code}")
    debug_log(f"Response body: {response.text}")
    
    if response.status_code == 201:
        debug_log(f"✅ Post created successfully")
        return response.json()
    else:
        raise Exception(f"Error creating post: {response.status_code} - {response.text}")


# Main posting logic
try:
    today = datetime.now().date().isoformat()
    debug_log(f"Starting posting check for date: {today}")
    debug_log(f"Credentials loaded - USER_1: {credentials['USER_1']}, USER_2: {credentials['USER_2']}")
    
    post_count = 0
    
    for user_id, posts in scheduled_posts.items():
        debug_log(f"Processing {user_id} with {len(posts)} posts")
        
        for idx, post in enumerate(posts):
            try:
                post_date = post.get("date")
                debug_log(f"  Post {idx}: date={post_date}, today={today}, match={post_date == today}")
                
                if post_date == today:
                    debug_log(f"  ✅ Date match found for {user_id}")
                    post_count += 1
                    
                    content = post.get("content", [])
                    debug_log(f"  Content type: {type(content)}, length: {len(content)}")
                    
                    # Ensure content is a string, even if it's a list
                    if isinstance(content, list):
                        debug_log(f"  Converting content from list to string")
                        content = "\n".join(
                            content[:1] +  
                            [line if not line.startswith("- ") else f"• {line[2:]}" for line in content[1:]]
                        )
                    
                    debug_log(f"  Final content length: {len(content)} characters")
                    debug_log(f"  First 100 chars: {content[:100]}")
                    
                    access_token = credentials['ACCESS_TOKEN_1'] if user_id == "USER_1" else credentials['ACCESS_TOKEN_2']
                    user_urn = credentials['USER_1'] if user_id == "USER_1" else credentials['USER_2']
                    
                    debug_log(f"  Using access_token: {access_token[:20]}...")
                    debug_log(f"  Using user_urn: {user_urn}")
                    
                    response = create_linkedin_post(user_urn, access_token, content)
                    
                    debug_log(f"✅ Success: Posted for {user_id}")
                    log_message(f"Success: Posted for {user_id}")
                    
            except Exception as post_error:
                debug_log(f"❌ Error posting for {user_id} on post {idx}", post_error)
                log_message(f"Error posting for {user_id}: {str(post_error)}")
    
    debug_log(f"Posting check completed. Total posts matching today: {post_count}")
    if post_count == 0:
        debug_log(f"⚠️ No posts scheduled for today ({today})")
        log_message(f"No posts scheduled for today ({today})")
                
except Exception as e:
    debug_log(f"❌ Failure: Exception occurred in main loop", e)
    log_message(f"Failure: Exception occurred - {str(e)}")