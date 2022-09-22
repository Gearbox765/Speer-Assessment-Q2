import pandas as pd
import requests
from bs4 import BeautifulSoup


BASE_URL = 'https://en.wikipedia.org'


def get_all_links_from_wiki_article(wiki_link):
    response = requests.get(wiki_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = {BASE_URL + a['href'] for a in soup.find(id='bodyContent').find_all('a', href=True) if a['href'].startswith('/wiki/')}
    return list(links)


def deep_scrape_wiki_links(start_page, depth=1):
    # Check to make sure that the depth argument is a number from 1 to 20
    if depth not in range(1, 21):
        raise ValueError('Argument depth must a number from 1 to 20')

    visited_links = []  # Create a visited links list to make sure you're not scraping the same urls
    all_links = set()  # Make all_links a set to avoid duplicate values (sets don't allow duplicate values)
    start_links = get_all_links_from_wiki_article(start_page)  # Get links to start scraping from.
    visited_links.append(start_links)  # Add the first link to visted links so it doesn't get scraped again.
    all_links.update(start_links)  # Add the initial scraped links to the all_links set to started scraping those.
    for cycle in range(1, depth + 1):  # For each cycle...
        unvisited_links = [link for link in all_links if link not in visited_links]  # Get all of the UNVISTED links inside of all_links
        for i, link in enumerate(unvisited_links, 1):  # Iterate over the unvisted links... enumurate(iterable, start) just allows us to get the loop index.
            print(f'Cycle {cycle}: Scraping link {i} of {len(unvisited_links)}')  # Log current scraping position
            new_links = get_all_links_from_wiki_article(link)  # Obtain links from unvisted_link
            all_links.update(new_links)  # Add new_links to update
            visited_links.append(link)  # Add visited link to visited_links list
        print(f'CYCLE {cycle} Complete. Total Links so far: {len(all_links)}')  # Log a cmplete cycle.
    return list(all_links)

    


if __name__ == '__main__':
    wiki_link = 'https://en.wikipedia.org/wiki/Egg_as_food'
    all_links = deep_scrape_wiki_links(wiki_link, depth=3)
    data = pd.DataFrame({'Links': all_links})  # Create a single column DataFrame (Python version of a table) to store all links
    data.to_csv('links.csv', index=False)  # Write that data to a CSV named 'links.csv'. index=False is to not have an index column in result file.