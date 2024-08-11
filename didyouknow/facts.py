from dataclasses import dataclass
import pickle
from typing import Optional

from httpx import get, HTTPError

WIKIPEDIA_RANDOM_API_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"

FACTFILE_FILENAME = "factfile.pickle"

DOWNLOAD_CHUNK_SIZE = 50

@dataclass
class Fact:
    extract_html: str
    image_source: str
    desktop_url: str
    mobile_url: str

def fact_from_wikipedia_summary(data: dict) -> Optional[Fact]:
    try:
        return Fact(data["extract_html"],
                    data["originalimage"]["source"],
                    data["content_urls"]["desktop"]["page"],
                    data["content_urls"]["mobile"]["page"])
    except KeyError:
        return None

def load() -> list[Fact]:
    try:
        with open(FACTFILE_FILENAME, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

def download():
    facts = load()
    print(f"download_facts started, {len(facts)} facts in factfile")
    while True:
        for _ in range(DOWNLOAD_CHUNK_SIZE):
            try:
                response = get(WIKIPEDIA_RANDOM_API_URL, follow_redirects=True)
                response.raise_for_status()
            except HTTPError as e:
                print(f"download_facts HTTPError {e}")
                continue
            else:
                data = response.json()
                fact = fact_from_wikipedia_summary(data)
                if fact:
                    facts.append(fact)
                print(f"download_facts downloaded {data['title']}")
        with open(FACTFILE_FILENAME, "wb") as f:
            pickle.dump(facts, f, pickle.HIGHEST_PROTOCOL)
        print("download_facts snapshot")

if __name__ == "__main__":
    download()
