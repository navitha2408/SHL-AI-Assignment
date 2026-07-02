import requests
from bs4 import BeautifulSoup

url = "https://www.shl.com/products/assessments/skills-and-simulations/technical-skills/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

for link in soup.find_all("a", href=True):
    text = link.get_text(strip=True)
    href = link["href"]

    if "products" in href:
        print(text)
        print(href)
        print("-" * 50)