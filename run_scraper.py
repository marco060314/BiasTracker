import subprocess
import json
import os
import sys

def run_scraper(target_url):
    # Ensure you're in the directory with scrapy.cfg
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    result = subprocess.run(
        [
            sys.executable, "-m", "scrapy",
            "crawl", "article",         # ← spider name
            "-a", f"url={target_url}"  # ← pass the URL as an argument
        ],
        capture_output=True,
        text=True
    )

    lines = result.stdout.strip().splitlines()
    try:
        return json.loads(lines[-1])
    except Exception:
        print("Full Scrapy output:\n", result.stdout)
        return {"error": "Failed to parse JSON", "raw_output": result.stdout}

#print(run_scraper("https://www.foxnews.com/media/supreme-court-consider-whether-parents-can-opt-out-kids-reading-lgbtq-books-classroom"))