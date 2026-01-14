"""
Update README.md with current day, date, and a random famous quote.
Runs via GitHub Actions daily.
"""

import datetime
import re
import requests


def get_random_quote():
    """Fetch a random quote from ZenQuotes API."""
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and len(data) > 0:
            quote = data[0].get("q", "Stay curious!")
            author = data[0].get("a", "Unknown")
            return quote, author
    except Exception as e:
        print(f"Error fetching quote: {e}")
    
    # Fallback quotes if API fails
    fallback_quotes = [
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
        ("Stay hungry, stay foolish.", "Steve Jobs"),
        ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
        ("First, solve the problem. Then, write the code.", "John Johnson"),
        ("The best error message is the one that never shows up.", "Thomas Fuchs"),
    ]
    import random
    return random.choice(fallback_quotes)


def get_current_datetime():
    """Get current day name and formatted date."""
    now = datetime.datetime.now(datetime.timezone.utc)
    day_name = now.strftime("%A")  # e.g., "Wednesday"
    date_str = now.strftime("%B %d, %Y")  # e.g., "January 14, 2026"
    return day_name, date_str


def update_readme():
    """Update README.md with dynamic content."""
    day_name, date_str = get_current_datetime()
    quote, author = get_random_quote()
    
    # Create the dynamic content block
    dynamic_content = f"""<!-- DAILY_CONTENT_START -->
### 📅 Today is **{day_name}, {date_str}**

> 💬 *"{quote}"*
> 
> — **{author}**

<sub>🔄 Auto-updated daily by GitHub Actions</sub>
<!-- DAILY_CONTENT_END -->"""

    # Read the current README
    with open("README.md", "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Replace content between markers
    pattern = r"<!-- DAILY_CONTENT_START -->.*?<!-- DAILY_CONTENT_END -->"
    if re.search(pattern, readme_content, re.DOTALL):
        new_content = re.sub(pattern, dynamic_content, readme_content, flags=re.DOTALL)
    else:
        # If markers don't exist, add them at the beginning after the title
        lines = readme_content.split("\n")
        insert_pos = 1  # After the first line
        for i, line in enumerate(lines):
            if line.startswith("#"):
                insert_pos = i + 1
                break
        lines.insert(insert_pos, "\n" + dynamic_content + "\n")
        new_content = "\n".join(lines)

    # Write the updated README
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print(f"✅ README updated!")
    print(f"   Day: {day_name}, {date_str}")
    print(f"   Quote: \"{quote}\" — {author}")


if __name__ == "__main__":
    update_readme()
