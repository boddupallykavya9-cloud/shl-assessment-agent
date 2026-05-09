import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

assessment_links = []

# SCRAPE MULTIPLE CATALOG PAGES
for start in range(0, 240, 12):

    catalog_url = (
        f"https://www.shl.com/solutions/products/product-catalog/?start={start}&type=1"
    )

    print(f"\nFetching catalog page: {catalog_url}")

    response = requests.get(catalog_url, headers=headers)

    print("Status:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")

    for link in links:

        href = link.get("href")

        if href and "/products/product-catalog/view/" in href:

            full_url = BASE_URL + href

            assessment_links.append(full_url)

    time.sleep(1)

# REMOVE DUPLICATES
assessment_links = list(set(assessment_links))

print(f"\nFound {len(assessment_links)} assessments")

assessments = []

# SCRAPE EACH ASSESSMENT PAGE
for url in assessment_links:

    try:

        print(f"Scraping: {url}")

        page = requests.get(url, headers=headers)

        page_soup = BeautifulSoup(page.text, "html.parser")

        # TITLE
        title_tag = page_soup.find("h1")

        title = (
            title_tag.text.strip()
            if title_tag
            else "N/A"
        )

        # GET PARAGRAPHS
        paragraphs = page_soup.find_all("p")

        clean_paragraphs = []

        for p in paragraphs:

            text = p.text.strip()

            if text:
                clean_paragraphs.append(text)

        # DESCRIPTION
        description = ""

        for text in clean_paragraphs:

            if (
                "test" in text.lower()
                or "assessment" in text.lower()
                or "solution" in text.lower()
            ):

                if len(text) > 50:

                    description = text
                    break

        # DEFAULT TEST TYPE
        test_type = "Unknown"

        assessment = {
            "name": title,
            "url": url,
            "description": description,
            "test_type": test_type
        }

        assessments.append(assessment)

        time.sleep(1)

    except Exception as e:

        print(f"Error scraping {url}")
        print(e)

# SAVE JSON
with open(
    "data/assessments.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        assessments,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nSaved assessments.json")