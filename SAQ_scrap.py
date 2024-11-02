import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode, urljoin


# this will return the total number of pages in the search result
def start_setup(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def build_saq_url(
    base_url="https://www.saq.com/fr/produits/vin/",
    category="vin-rouge",
    availability=None,
    country=None,
    min_price=None,
    max_price=None,
    page=None,
    millesime=None,
    limit=None,
):
    # Define query parameters as a dictionary, only adding those that are not None
    params = {}
    if availability:
        params["availability"] = availability
    if country:
        params["pays_origine"] = country
    if min_price is not None and max_price is not None:
        params["price"] = f"{min_price}-{max_price}"
    elif min_price is not None:
        params["price"] = f"{min_price}-"
    elif max_price is not None:
        params["price"] = f"-{max_price}"
    elif millesime is not None:
        params["millesime_produit"] = millesime
    if page:
        params["p"] = page
    if limit:
        params["product_list_limit"] = limit

    # Construct the query string
    query_string = urlencode(params)
    # Combine base URL with the category path and query string
    if category:
        full_url = urljoin(
            base_url, f"{category}?{query_string}" if query_string else category
        )
    else:
        full_url = urljoin(base_url, f"?{query_string}" if query_string else "")

    return full_url


# for a page with the URL we will try to find the number of pages for all results
def get_total_pages(soup):
    # Find the pagination element indicating the total number of pages
    pagination = soup.find("ul", class_="items pages-items")
    if pagination:
        # Find the last page number in the pagination
        last_page_link = pagination.find_all("li", class_="item")[-1]
        total_pages = int(last_page_link.get_text(strip=True))
        return total_pages
    else:
        return 1  # If no pagination is found, there may be only 1 page


def fetch_wine_details(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract wine details
        wines = []
        product_elements = soup.find_all("li", class_="product-item")

        for product in product_elements:
            # Get wine name
            name_element = product.find("a", class_="product-item-link")
            name = name_element.get_text(strip=True) if name_element else "N/A"

            # Get wine type (e.g., vin rouge), volume, and country
            details = product.find("div", class_="product-item-details")
            wine_type = "vin rouge"  # Assuming all are red wine as per page filter

            # Check for volume and country information
            volume_country = (
                details.find("div", class_="product-item-attribute")
                if details
                else None
            )
            if volume_country:
                volume_country_text = volume_country.get_text(strip=True)
                volume, country = (
                    volume_country_text.split("|")[0].strip(),
                    volume_country_text.split("|")[-1].strip(),
                )
            else:
                volume, country = "N/A", "N/A"

            # Get SAQ code
            saq_code = product.get("data-product-sku", "N/A")

            # Get price
            price_element = product.find("span", class_="price")
            price = price_element.get_text(strip=True) if price_element else "N/A"

            # Get rating/score if available
            score_element = product.find("div", class_="rating-result")
            score = score_element.get_text(strip=True) if score_element else "N/A"

            # Get product link
            link = name_element["href"] if name_element else "N/A"

            # Collect all details in a dictionary
            wine_info = {
                "Wine Name": name,
                "Wine Type": wine_type,
                "Volume": volume,
                "Country": country,
                "SAQ Code": saq_code,
                "Price": price,
                "Score": score,
                "Product Link": link,
            }

            wines.append(wine_info)

        return wines

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []


if __name__ == "__main__":
    # Example usage
    url = "https://www.saq.com/fr/produits/vin/vin-rouge?availability=Online&pays_origine=France&price=30-6289&product_list_limit=96"
    url2 = "https://www.saq.com/fr/produits/vin/vin-rouge?availability=Online&p=2&pays_origine=France&price=30-6289&product_list_limit=96"
    # page2
    wine_details = fetch_wine_details(url)
    for wine in wine_details:
        print(wine)
