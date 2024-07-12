import pandas as pd
import os

# Define file paths
reddit_comments = "./data/reddit_comments.csv"
youtube_comments = "./data/youtube_comments.csv"
output_file = "./data/social_media.csv"

# Delete existing output file (if it exists)
try:
    os.remove(output_file)
    print(f"Deleted existing file: {output_file}")
except FileNotFoundError:
    pass  # Ignore if file doesn't exist

# Read dataframes
df1 = pd.read_csv(reddit_comments)
df2 = pd.read_csv(youtube_comments)

# Append dataframes
combined_df = pd.concat([df1, df2], ignore_index=True)  # Combine and ignore original indices

# Save combined data to new CSV
combined_df.to_csv(output_file, index=False)

print(f"Data from {reddit_comments} and {youtube_comments} appended to {output_file}")

