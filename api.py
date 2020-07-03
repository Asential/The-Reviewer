import requests

def imp(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "VyHPbwWOz82BqhxqAbPMbg", "isbns": isbn})
    if res.status_code != 200:
      raise Exception("ERROR: API request unsuccessful.")
    return res.json()

