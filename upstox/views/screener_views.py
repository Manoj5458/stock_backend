
from bs4 import BeautifulSoup
from django.http import HttpResponse, JsonResponse
import requests
from django.views.decorators.csrf import csrf_exempt  # Import csrf_exempt
import json

def fetch_screener_data(request, company_name):
    base_url = 'https://www.screener.in/company/'
    company_url = f'{base_url}{company_name}/consolidated/'

    # Send a GET request and handle potential errors
    response = requests.get(company_url)
    if response.status_code != 200:
        print('Error fetching data. Check company name or website.')
        return HttpResponse('Error fetching data. Check company name or website.', status=response.status_code)

    # Parse the HTML response
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize a dictionary to store the extracted data
    data = {}

    # Extract basic information (Market Cap, Current Price, etc.)
    for li in soup.find_all('li', class_='flex flex-space-between'):
        name = li.find('span', class_='name').get_text(strip=True)
        value = li.find('span', class_='number').get_text(strip=True)

        if name == 'High / Low':
            high_low_values = [val.get_text(strip=True) for val in li.find_all('span', class_='number')]
            data[name] = f'₹ {high_low_values[0]} / ₹ {high_low_values[1]}'
        else:
            data[name] = value

    # Extract Net Profit data (Quarterly and Yearly)
    tr_tags = soup.find_all('tr', class_='strong')

    # Initialize placeholders for quarterly and yearly data
    quarterly_data, yearly_data = [], []

    # Loop through the table rows and extract quarterly and yearly Net Profit
    for tr in tr_tags:
        # Find the 'Net Profit' label
        button_text = tr.find('button', class_='button-plain')
        if button_text and 'Net Profit' in button_text.get_text(strip=True):
            td_tags = tr.find_all('td')
            data_list = [td.get_text(strip=True) for td in td_tags]

            if not quarterly_data:
                quarterly_data = data_list[1:]  # Exclude 'Net Profit+' label
            else:
                yearly_data = data_list[1:]  # Exclude 'Net Profit' label

    # Add extracted data to the dictionary
    data['Net Profit Quarterly'] = quarterly_data
    data['Net Profit Yearly'] = yearly_data

    # Return the data as a JSON response
    return JsonResponse(data)

@csrf_exempt  # Disable CSRF protection for this view
def screener(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            company_name = body.get("searchValue", "")
            if not company_name:
                return JsonResponse({"error": "Company name is required"}, status=400)
            return fetch_screener_data(request, company_name)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"}, status=400)
    return JsonResponse({"error": "Invalid request method"}, status=405)