import requests


def fetch_wine_reviews(wine_id, vintage_year, page_number):

     # Define the user agent header
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
    }

    # Define the API URL with parameters
    vivino_url = f"https://www.vivino.com/api/wines/{wine_id}/reviews?per_page=50&year={vintage_year}&page={page_number}"

    # Fetch data from the API and parse it as JSON
    api_data = requests.get(vivino_url, headers=headers).json()

    return api_data


if __name__ == "__main__":
    # Example usage
    wine_id = 153843
    vintage_year = 2016
    page_number = 1

    reviews = fetch_wine_reviews(wine_id, vintage_year, page_number)
    print(reviews)