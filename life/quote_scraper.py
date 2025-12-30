import requests

url = "https://raw.githubusercontent.com/JamesFT/Database-Quotes-JSON/master/quotes.json"
data = requests.get(url).json()

with open("quotes.txt", "w", encoding="utf-8") as f:
    for q in data:
        f.write(f"{q['quoteText']} — {q['quoteAuthor'] or 'Unknown'}\n")

print(len(data))
