import praw
import csv
import os
from datetime import datetime

SECRET = ''
APP_ID = ''
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'

reddit = praw.Reddit(client_id=APP_ID, client_secret=SECRET, user_agent=User_Agent)

# Delete existing output file (if it exists)
try:
    os.remove('./data/reddit_comments.csv')
    print(f"Deleted existing file: {'./data/reddit_comments.csv'}")
except FileNotFoundError:
    pass  # Ignore if file doesn't exist

# List of post IDs you want to process
post_ids = [
    '19677mk',
    'saw718',
    '17ubiji',
    'y01u9v',
    '2zsxyz', # ~ 350 comments
    'dmxmdb', # ~ 400 comments
    'suuvon', # ~ 100 comments
    'jksu9z' # ~ 1000+ comments
]

# Check if the file already exists to decide on writing the header
file_exists = os.path.isfile('./data/reddit_comments.csv')

# Open the CSV file in append mode
with open('./data/reddit_comments.csv', mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header only if the file does not exist
    if not file_exists:
        writer.writerow(["text", "author", "score", "datetime"])

    for post_id in post_ids:
        print(f"Fetching data for {post_id}")
        submission = reddit.submission(id=post_id)
        submission.comments.replace_more(limit=0)  # Expand all comments

        for top_level_comment in submission.comments:
            # Conditions for top-level comments
            if top_level_comment.author and len(top_level_comment.body) > 25:
                author_name = top_level_comment.author.name if top_level_comment.author else "Deleted User"
                comment_date = datetime.utcfromtimestamp(top_level_comment.created_utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                writer.writerow([top_level_comment.body, author_name, top_level_comment.score, comment_date])

            # Processing replies
            if len(top_level_comment.replies) > 0:
                top_level_comment.replies.replace_more(limit=0)
                for reply in top_level_comment.replies.list():
                    if reply.author and len(reply.body) > 25:
                        reply_author_name = reply.author.name if reply.author else "Deleted User"
                        reply_date = datetime.utcfromtimestamp(reply.created_utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                        writer.writerow([reply.body, reply_author_name, reply.score, reply_date])
# %%
