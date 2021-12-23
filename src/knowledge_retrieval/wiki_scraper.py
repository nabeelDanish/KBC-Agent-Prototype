""""
  Scrapes Wikipedia data and returns any data requested in a form that is usable by our models
"""

import wikipedia
from wikipedia import PageError


def getTopicSummary(topic, num_sentences=20):
    wikipedia.API_URL = 'https://'
    retrieved_summary = None
    try:
        print(f"[wiki_scraper]: Fetching '{topic}' summary")
        retrieved_summary = wikipedia.summary(topic, sentences=num_sentences)
        print(f"[wiki_scraper]: Successfully fetched '{topic}' summary")
    except PageError:
        print(f"[wiki_scraper]: Topic does not exist / is ambiguous")
        retrieved_summary = None

    return retrieved_summary

