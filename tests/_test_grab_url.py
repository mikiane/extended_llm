import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_text_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.extract()

    # Get text
    text = soup.get_text()

    # Break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # Break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # Drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    
    return text

def get_links_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            # Parse relative links
            full_url = urllib.parse.urljoin(url, href)
            links.append(full_url)
            
    return links

def write_content_to_file(url, filename, max_depth):
    visited_links = set()
    
    links_to_visit = [(url, 0)]
    
    with open(filename, 'w') as f:
        while links_to_visit:
            current_url, depth = links_to_visit.pop(0)
            if current_url not in visited_links:
                visited_links.add(current_url)
                try:
                    text = get_text_from_page(current_url)
                    print("get data from : " + str(current_url))
                    f.write(text + "\n")
                    
                    if depth < max_depth:
                        new_links = get_links_from_page(current_url)
                        print("get new link  : " + str(new_links))
                        links_to_visit.extend((link, depth+1) for link in new_links)
                except Exception as e:
                    print(f"Failed to process {current_url}: {e}")

# Usage
write_content_to_file('https://mikiane.com', 'mikiane.txt', 2)
