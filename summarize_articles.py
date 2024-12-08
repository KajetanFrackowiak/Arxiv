from transformers import pipeline


def compile_summary(articles):
    content = "# Daily Highlights from arxiv\n\n"
    for article in articles:
        content += f"**Summary:** {article['summary']}\n\n**References:** {article['link']}\n\n"
    return content

def summarize_articles_to_md(articles, output_file="arxiv_summary.md"):
    # Initialize the summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)

    # Summarize each article and store the summaries
    summarized_articles = []
    for article in articles:
        abstract = article["abstract"]
        # Adjust max_length based on input length
        max_length = min(60, len(abstract) // 2)
        summary = summarizer(abstract, max_length=max_length, min_length=30, do_sample=False)[0]["summary_text"]
        summarized_articles.append({"summary": summary, "link": article["link"]})

    # Compile the summaries into markdown content
    content = compile_summary(summarized_articles)

    with open(output_file, "w") as f:
        f.write(content)
