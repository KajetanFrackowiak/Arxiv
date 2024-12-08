import requests
from bs4 import BeautifulSoup

def fetch_arxiv_articles():
    url = "https://arxiv.org/list/cs/new"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for entry in soup.find_all("dd")[:3]:  # Limit to 3 articles
        title_tag = entry.find_previous_sibling("dt")
        title_div = title_tag.find("div", class_="list-title mathjax") if title_tag else None
        title = title_div.text.strip().replace("Title:", "") if title_div else "No Title"
        abstract_tag = entry.find("p")
        abstract = abstract_tag.text.strip() if abstract_tag else "No Abstract"

        link_tag = title_tag.find("a", href=True)
        if link_tag:
            link = "https://arxiv.org" + link_tag["href"]
        else:
            link = "No Link"
        articles.append({"title": title, "abstract": abstract, "link": link})
    return articles