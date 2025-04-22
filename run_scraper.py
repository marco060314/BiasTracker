import subprocess
import json
import os
import sys

def run_scraper(target_url):
    # Ensure scrapy settings or working dir is correctly located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    result = subprocess.run(
        [
            sys.executable, "-m", "scrapy",
            "crawl", "article",
            "-a", f"url={target_url}"
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