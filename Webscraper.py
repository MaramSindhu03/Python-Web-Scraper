import requests
from bs4 import BeautifulSoup

def fetch_webpage(url):
    """
    Fetches the HTML content of a webpage.
    
    Parameters:
        url (str): The URL of the webpage to fetch.
        
    Returns:
        str: The HTML content of the webpage if successful, None otherwise.
    """
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Raise an error if the response status is not 200 (OK)
        response.raise_for_status()
        
        # Return the HTML content of the page
        return response.content
    
    except requests.RequestException as e:
        # Print an error message if there's a problem with the request
        print(f"Error fetching the page: {e}")
        return None

def extract_content(html_content):
    """
    Parses the HTML content to extract title, headings, hyperlinks, and image URLs.
    
    Parameters:
        html_content (str): The HTML content of the webpage.
        
    Returns:
        dict: A dictionary containing extracted title, headings, links, and images.
    """
    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract the title of the page
    title = soup.title.string if soup.title else "No title found"
    
    # Extract headings (h1, h2, h3)
    headings = {
        'h1': [h1.get_text(strip=True) for h1 in soup.find_all('h1')],
        'h2': [h2.get_text(strip=True) for h2 in soup.find_all('h2')],
        'h3': [h3.get_text(strip=True) for h3 in soup.find_all('h3')]
    }
    
    # Extract all hyperlinks (anchor tags)
    links = [(a.get_text(strip=True), a.get('href')) for a in soup.find_all('a', href=True)]
    
    # Extract all image URLs (img tags)
    images = [img.get('src') for img in soup.find_all('img') if img.get('src')]
    
    return {
        "title": title,
        "headings": headings,
        "links": links,
        "images": images
    }

def print_extracted_data(data):
    """
    Displays the extracted title, headings, links, and images in a readable format.
    
    Parameters:
        data (dict): A dictionary containing extracted content.
    """
    # Print the title of the page
    print(f"Title: {data['title']}\n")
    
    # Print headings
    print("Headings:")
    for level, texts in data['headings'].items():
        for text in texts:
            print(f"  {level}: {text}")
    
    # Print hyperlinks
    print("\nLinks:")
    for text, url in data['links']:
        print(f"  Text: '{text}' - URL: {url}")
    
    # Print image URLs
    print("\nImages:")
    for img_url in data['images']:
        print(f"  {img_url}")

def main():
    """
    Main function that coordinates fetching, parsing, and displaying webpage data.
    """
    # Get the URL from the user
    url = input("Enter the URL to scrape: ")
    
    # Fetch the HTML content from the provided URL
    html_content = fetch_webpage(url)
    
    # Proceed if the webpage content was successfully fetched
    if html_content:
        # Parse the HTML content to extract data
        extracted_data = extract_content(html_content)
        
        # Display the extracted data
        print_extracted_data(extracted_data)

if __name__ == "__main__":
    main()
