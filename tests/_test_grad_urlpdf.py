import requests
from bs4 import BeautifulSoup
import urllib.parse
import pdfplumber
import os
import io

URL = "https://arbevel.com/fr/"
DEPTH = 4
OUTPUTFILE = "../datas/arbevel.txt"
DOMAIN = 'arbevel.com'  # Specify the domain

def get_text_from_page(url):
    response = requests.get(url)
    content_type = response.headers.get('content-type')

    if 'html' in content_type:
        print("HTML file found\n")

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
    elif 'pdf' in content_type:
        # Download the PDF file
        print("PDF file found\n")
        pdf_content = io.BytesIO(response.content)
        with pdfplumber.open(pdf_content) as pdf:
            # Extract text from each page
            return "\n".join(page.extract_text() for page in pdf.pages)

    else:
        print(f"Unsupported content type: {content_type} \n")
        return ''

def get_links_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            # Parse relative links
            print(f"Parsing {url} \n")
            full_url = urllib.parse.urljoin(url, href)
            links.append(full_url)
            
    return links

from urllib.parse import urlparse


def write_content_to_file(url, filename, max_depth, valid_domain):
    visited_links = set()
    
    links_to_visit = [(url, 0)]
    
    with open(filename, 'w') as f:
        while links_to_visit:
            current_url, depth = links_to_visit.pop(0)
            if current_url not in visited_links:
                visited_links.add(current_url)

                # Check if the domain of the current URL matches the specified DOMAIN
                domain = urlparse(current_url).netloc
                if domain != valid_domain:
                    print(f"Skipping {current_url} because it is not in the domain {valid_domain}")
                    continue
                
                try:
                    text = get_text_from_page(current_url)
                    print("get data from : " + str(current_url) + "\n")
                    f.write(text + "\n")
                    
                    if depth < max_depth:
                        new_links = get_links_from_page(current_url)
                        print("get new link  : " + str(new_links)+ "\n")
                        links_to_visit.extend((link, depth+1) for link in new_links)
                except Exception as e:
                    print(f"Failed to process {current_url}: {e}"+ "\n")


# Usage
write_content_to_file(str(URL), str(OUTPUTFILE), int(DEPTH), str(DOMAIN))
