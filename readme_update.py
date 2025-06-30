import feedparser
import datetime
import ssl
import re

ssl._create_default_https_context = ssl._create_unverified_context

RSS_URL = "https://zoo-tech.tistory.com/rss"
BLOG_SECTION_START = "<!-- BLOG-START -->"
BLOG_SECTION_END = "<!-- BLOG-END -->"
README_PATH = "README.md"

def get_latest_blog_posts(max_posts=3):
    feed = feedparser.parse(RSS_URL)
    posts = []
    for entry in feed.entries[:max_posts]:
        title = entry.title
        link = entry.link
        try:
            dt = datetime.datetime(*entry.published_parsed[:6])
            formatted_date = dt.strftime("%Y-%m-%d")
            posts.append(f"- <a href=\"{link}\">{title}</a> ({formatted_date})")
        except Exception as e:
            posts.append(f"- <a href=\"{link}\">{title}</a>")  
    return "\n".join(posts)

def update_readme():
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    new_blog_content = get_latest_blog_posts()
    new_section = f"{BLOG_SECTION_START}\n{new_blog_content}\n{BLOG_SECTION_END}"

    updated_content = re.sub(
        f"{BLOG_SECTION_START}.*?{BLOG_SECTION_END}",
        new_section,
        content,
        flags=re.DOTALL
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("README.md 업데이트 완료")

if __name__ == "__main__":
    update_readme()
