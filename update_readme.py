"""
Update README.md with current day, date, weather, joke, and tech news.
Runs via GitHub Actions daily.
"""

import datetime
import re
import random
import requests
import sys

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
    
    fallback_quotes = [
        ("The only way to do great work is to love what you do.", "Steve Jobs"),
        ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
        ("Code is like humor. When you have to explain it, it's bad.", "Cory House"),
    ]
    return random.choice(fallback_quotes)

def get_weather():
    """Fetch current weather for Eindhoven (latitude=51.44, longitude=5.47)."""
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=51.44&longitude=5.47&current=temperature_2m,weather_code&timezone=Europe%2FAmsterdam"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data.get("current", {})
        temp = current.get("temperature_2m", "N/A")
        code = current.get("weather_code", 0)
        
        # WMO Weather interpretation codes (http://www.nodc.noaa.gov/archive/arc0021/0002199/1.1/data/0-data/HTML/WMO-CODE/WMO4677.HTM)
        weather_icons = {
            0: "☀️ Clear sky",
            1: "🌤️ Mainly clear",
            2: "⛅ Partly cloudy",
            3: "☁️ Overcast",
            45: "🌫️ Fog", 48: "🌫️ Depositing rime fog",
            51: "🌧️ Drizzle", 53: "🌧️ Drizzle", 55: "🌧️ Drizzle",
            61: "🌧️ Rain", 63: "🌧️ Rain", 65: "🌧️ Rain",
            71: "🌨️ Snow", 73: "🌨️ Snow", 75: "🌨️ Snow",
            80: "🌧️ Rain showers", 81: "🌧️ Rain showers", 82: "🌧️ Rain showers",
            95: "⛈️ Thunderstorm", 96: "⛈️ Thunderstorm", 99: "⛈️ Thunderstorm"
        }
        condition = weather_icons.get(code, "Unknown")
        return f"{temp}°C - {condition}"
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "Weather unavailable"

def get_joke():
    """Fetch a random programming joke."""
    try:
        response = requests.get("https://official-joke-api.appspot.com/jokes/programming/random", timeout=10)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            data = data[0]
        return data.get("setup", ""), data.get("punchline", "")
    except Exception as e:
        print(f"Error fetching joke: {e}")
        return "Why do programmers prefer dark mode?", "Because light attracts bugs."

def get_tech_news():
    """Fetch top 5 tech stories from Hacker News."""
    try:
        # Get top stories IDs
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10)
        ids = response.json()[:5]
        
        stories = []
        for id in ids:
            item_resp = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{id}.json", timeout=5)
            item = item_resp.json()
            title = item.get("title", "No title")
            url = item.get("url", f"https://news.ycombinator.com/item?id={id}")
            stories.append(f"- [{title}]({url})")
        return "\n".join(stories)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return "- Failed to fetch news"

def get_current_datetime():
    """Get current day name and formatted date."""
    now = datetime.datetime.now(datetime.timezone.utc)
    day_name = now.strftime("%A")
    date_str = now.strftime("%B %d, %Y")
    return day_name, date_str

def update_readme():
    """Update README.md with dynamic dashboard content."""
    day_name, date_str = get_current_datetime()
    quote, author = get_random_quote()
    weather_info = get_weather()
    joke_setup, joke_punchline = get_joke()
    news_content = get_tech_news()

    # Create the dynamic dashboard
    dynamic_content = f"""<!-- DAILY_CONTENT_START -->
### 📅 Today is **{day_name}, {date_str}**

<table>
<tr>
<td width="50%" valign="top">

### 🌤️ Eindhoven Weather
**{weather_info}**

### 🤣 Daily Joke
*{joke_setup}*
**{joke_punchline}**

### 💬 Quote
> "{quote}"
> — **{author}**

</td>
<td width="50%" valign="top">

### 📰 Top 5 Tech News
{news_content}

</td>
</tr>
</table>

<sub>Auto-updated daily by GitHub Actions</sub>
<!-- DAILY_CONTENT_END -->"""

    # Read the current README
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            readme_content = f.read()
    except FileNotFoundError:
        print("README.md not found.")
        return

    # Replace content between markers
    pattern = r"<!-- DAILY_CONTENT_START -->.*?<!-- DAILY_CONTENT_END -->"
    if re.search(pattern, readme_content, re.DOTALL):
        new_content = re.sub(pattern, dynamic_content, readme_content, flags=re.DOTALL)
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ README updated successfully with new dashboard!")
    else:
        print("❌ Could not find content markers in README.md")

if __name__ == "__main__":
    update_readme()
