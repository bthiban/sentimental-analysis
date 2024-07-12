import praw
import csv
from datetime import datetime
import os

SECRET = ''
APP_ID = ''
User_Agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'

reddit = praw.Reddit(client_id=APP_ID, client_secret=SECRET, user_agent=User_Agent)

submission = reddit.submission(id='tci9st')

# Replace 'post_id' with the actual post ID.

submission.comments.replace_more(limit=None)  # This line ensures you get all comments, not just the top-level ones.

# for comment in submission.comments.list():
#     print(comment.body)

# Open a new CSV file to write into
with open('data/reddit_comments.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write the header row
    writer.writerow(["text", "author", "score", "date"])

    for top_level_comment in submission.comments:
        if len(top_level_comment.body) > 100:
            author_name = top_level_comment.author.name
            comment_date = datetime.utcfromtimestamp(top_level_comment.created_utc).strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([top_level_comment.body, author_name, top_level_comment.score, comment_date])

        if len(top_level_comment.replies) > 0:
            top_level_comment.replies.replace_more(limit=0)  # Optionally expand all replies
            for reply in top_level_comment.replies.list():
                # Check if the reply's author exists and the reply length > 100
                if len(reply.body) > 100:
                    reply_author_name = reply.author.name
                    reply_date = datetime.utcfromtimestamp(reply.created_utc).strftime('%Y-%m-%d %H:%M:%S')
                    writer.writerow([reply.body, reply_author_name, reply.score, reply_date])







#%%
