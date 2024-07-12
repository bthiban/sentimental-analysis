import praw
import csv
import os
from datetime import datetime


# API credentials and User-Agent configuration
SECRET = ''
APP_ID = ''
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'

# Initialize a Reddit instance with the above credentials
reddit = praw.Reddit(client_id=APP_ID, client_secret=SECRET, user_agent=User_Agent)

# Delete existing output file if it exists to start fresh
try:
    os.remove('./data/reddit_comments.csv')
    print(f"Deleted existing file: {'./data/reddit_comments.csv'}")
except FileNotFoundError:
    pass  # Ignore if the file doesn't exist, proceed with script

# List of Reddit post IDs to fetch comments from
post_ids = [
    '19677mk', 'saw718', '17ubiji', 'y01u9v', '2zsxyz', # ~ 350 comments
    'dmxmdb', # ~ 400 comments
    'suuvon', # ~ 100 comments
    'jksu9z' # ~ 1000+ comments
]

# Check if the output CSV file already exists
file_exists = os.path.isfile('./data/reddit_comments.csv')

# Open the CSV file in append mode to add new data without overwriting existing data
with open('./data/reddit_comments.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the CSV header if the file does not already exist
    if not file_exists:
        writer.writerow(["text", "author", "score", "datetime"])

    # Loop through each post ID to fetch comments
    for post_id in post_ids:
        print(f"Fetching data for {post_id}")
        submission = reddit.submission(id=post_id)

        # Expand all more comments if there are any, limit=0 to replace all
        submission.comments.replace_more(limit=0)

        # Process each top-level comment
        for top_level_comment in submission.comments:
            # Ensure comment has an author and the body length is greater than 25 characters
            if top_level_comment.author and len(top_level_comment.body) > 25:
                author_name = top_level_comment.author.name if top_level_comment.author else "Deleted User"
                comment_date = datetime.utcfromtimestamp(top_level_comment.created_utc).strftime('%Y-%m-%dT%H:%M:%SZ')

                # Write the comment data to the CSV file
                writer.writerow([top_level_comment.body, author_name, top_level_comment.score, comment_date])

            # Process replies to top-level comments
            if len(top_level_comment.replies) > 0:
                top_level_comment.replies.replace_more(limit=0)
                for reply in top_level_comment.replies.list():
                    # Check conditions similar to top-level comments
                    if reply.author and len(reply.body) > 25:
                        reply_author_name = reply.author.name if reply.author else "Deleted User"
                        reply_date = datetime.utcfromtimestamp(reply.created_utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                        writer.writerow([reply.body, reply_author_name, reply.score, reply_date])
