import requests
from bs4 import BeautifulSoup

def fetch_wine_details(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract wine details
        wines = []
        product_elements = soup.find_all('li', class_='product-item')
        
        for product in product_elements:
            # Get wine name
            name = product.find('a', class_='product-item-link').get_text(strip=True)
            
            # Get wine type (e.g., vin rouge), volume, and country
            details = product.find('div', class_='product-item-details')
            wine_type = "vin rouge"  # Assuming all are red wine as per page filter
            volume_country = details.find('div', class_='product-item-attribute').get_text(strip=True)
            volume, country = volume_country.split('|')[0].strip(), volume_country.split('|')[-1].strip()

            # Get SAQ code
            saq_code = product.get('data-product-sku')

            # Get price
            price = product.find('span', class_='price').get_text(strip=True)

            # Get rating/score if available
            score = product.find('div', class_='rating-result')
            score = score.get_text(strip=True) if score else "N/A"

            # Get product link
            link = product.find('a', class_='product-item-link')['href']

            # Collect all details in a dictionary
            wine_info = {
                'Wine Name': name,
                'Wine Type': wine_type,
                'Volume': volume,
                'Country': country,
                'SAQ Code': saq_code,
                'Price': price,
                'Score': score,
                'Product Link': link
            }
            
            wines.append(wine_info)

        return wines

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

# Example usage
url = 'https://www.saq.com/fr/produits/vin/vin-rouge?availability=Online&pays_origine=France&price=30-6289'
wine_details = fetch_wine_details(url)
for wine in wine_details:
    print(wine)
