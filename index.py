#%%
import praw
import pprint
from praw.models import MoreComments

SECRET='tVMkzBSW60HM2kJSHnce1C0b2kZwag'
APP_ID='NN0AUPTrPOSiuYqnuW5rAA'

url = 'https://www.reddit.com/r/helpit/comments/1bhqhl9/my_husband_is_so_negative//'

reddit = praw.Reddit(
    client_id=APP_ID,
    client_secret=SECRET,
    user_agent="Comment Extraction",
)

submission = reddit.submission(url=url)

print(submission)

# :::::::::::::::: TOP LEVEL COMMENTS ::::::::::::::::
# for top_level_comment in submission.comments:
#     print(top_level_comment.body)

for top_level_comment in submission.comments:
    if isinstance(top_level_comment, MoreComments):
        continue

    print(top_level_comment.body)
#%%
