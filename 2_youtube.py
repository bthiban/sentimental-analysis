from googleapiclient.discovery import build
import csv
import os

def get_comments(video_id):
    youtube = build('youtube', 'v3', developerKey='')

    results = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText"
    ).execute()

    comments = []
    for item in results["items"]:
        comments.append(
            {
                "comment": get_comment_props(item=item, entity='textDisplay'),
                "author": get_comment_props(item=item, entity='authorDisplayName'),
                "datetime": get_comment_props(item=item, entity='publishedAt'),
                "likes": get_comment_props(item=item, entity='likeCount')
            }
        )

    next_page_token = results.get('nextPageToken')
    while next_page_token:
        next_page_results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            pageToken=next_page_token
        ).execute()

        for item in next_page_results["items"]:
            comments.append(
                {
                    "comment": get_comment_props(item=item, entity='textDisplay'),
                    "author": get_comment_props(item=item, entity='authorDisplayName'),
                    "datetime": get_comment_props(item=item, entity='publishedAt'),
                    "likes": get_comment_props(item=item, entity='likeCount')
                }
            )

        next_page_token = next_page_results.get('nextPageToken')

    return comments


def get_comment_props(item, entity):
    return item['snippet']['topLevelComment']['snippet'][entity]


if __name__ == "__main__":

    output_file = "data/youtube_comments.csv"
    # Delete existing output file (if it exists)
    try:
        os.remove(output_file)
        print(f"Deleted existing file: {output_file}")
    except FileNotFoundError:
        pass  # Ignore if file doesn't exist

    """
    1. https://www.youtube.com/watch?v=Wi1nHfly9I4&ab_channel=HubNut Nissan LEAF. Is it still relevant? EV Review and test drive
    2. https://www.youtube.com/watch?v=r4uPrdevg_w&ab_channel=KelleyBlueBook 2023 Nissan Leaf | Review & Road Test
    3. https://www.youtube.com/watch?v=8B2_hZmZc3c&ab_channel=TFLEV The Early Nissan Leaf Is A Very Cheap EV - But Here’s Why You Should Never Buy One!
    4. https://www.youtube.com/watch?v=4hE2EdLj6N4&ab_channel=TimWilliams Is the Nissan Leaf A Good EV Option In 2023?
    5. https://www.youtube.com/watch?v=M46Kc_3Qfas&ab_channel=DrJake%27sVeryBritishReviews Saving £3k/yr trading my Diesel for a 2020 Nissan Leaf EV Car!
    6. https://www.youtube.com/watch?v=Ruxpr2yIsBE&ab_channel=HighPeakAutos Should You Buy a NISSAN LEAF? (Test Drive & Review 2021 59KWh)
    7. https://www.youtube.com/watch?v=H8SELcl8r-o&ab_channel=carwow New Nissan Leaf 2018 - is this the end of fossil fuels? | Top10s 
    8. https://www.youtube.com/watch?v=Ur47okU3eUk&ab_channel=carwow  Are used EVs a rip-off?! 
    """

    video_ids = [
        "Wi1nHfly9I4",
        "r4uPrdevg_w",
        "8B2_hZmZc3c",
        "4hE2EdLj6N4",
        "M46Kc_3Qfas",
        "Ruxpr2yIsBE",
        "H8SELcl8r-o",
        "Ur47okU3eUk"
    ]

    print(f"Number of videos in the list {len(video_ids)}")

    with open("data/youtube_comments.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["text", "author", "score", "datetime"])

        for video_id in video_ids:
            print(f"Fetching data for {video_id}")
            comments = get_comments(video_id)
            for comment in comments:
                if len(comment["comment"]) > 25:  # Check comment length
                    comment_data = [comment["comment"], comment["author"], comment["likes"], comment["datetime"]]
                    writer.writerow(comment_data)

    print("Done writing comments to CSV")
