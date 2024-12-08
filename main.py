import time
import schedule
import os
from fetch_articles import fetch_arxiv_articles
from summarize_articles import summarize_articles_to_md
from create_video import create_video_summary
from youtube import process_and_upload_videos_youtube

def job():
    articles = fetch_arxiv_articles()

    summarize_articles_to_md(articles)

    # Read the summarized articles from the markdown file
    summarized_articles = []
    with open("arxiv_summary.md", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for i in range(2, len(lines), 4):  # Skip the title and empty lines
            summary = lines[i].strip().replace("**Summary:** ", "")
            link = lines[i + 2].strip().replace("**References:** ", "").replace(")", "")
            summarized_articles.append({"summary": summary, "link": link})


    create_video_summary(summarized_articles)
    process_and_upload_videos_youtube()


    files_to_delete = ["arxiv_summary.md", "arxiv_summary.mp4", "audio.mp3"]

    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            print(f"{file} has been deleted.")
        else:
            print(f"{file} does not exist.")



schedule.every().day.at("10:00").do(job)

if __name__ == "__main__":

    while True:
        schedule.run_pending()
        time.sleep(1)