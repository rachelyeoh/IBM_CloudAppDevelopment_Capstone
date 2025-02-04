import requests
import json
# import related models here
from requests.auth import HTTPBasicAuth
from .models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    # Call get method of requests library with URL and parameters
    if 'apikey' in kwargs:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs, auth=HTTPBasicAuth('apikey',kwargs['apikey']))
    else:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    response = requests.post(url, params=kwargs, json=json_payload)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, dealerId=kwargs["dealer_id"])
    if json_result:
        reviews = json_result["reviews"]
        for review in reviews:
            if review["_id"][0] == "_":
                continue
            review_obj = DealerReview(dealership=review["dealership"], name=review["name"], 
                            purchase=review["purchase"], review=review["review"], 
                            purchase_date=review["purchase_date"], car_make=review["car_make"], 
                            car_model=review["car_model"], car_year=review["car_year"], 
                            sentiment=analyze_review_sentiments(review["review"]))
            results.append(review_obj)

    return {"reviews": results, "dealership_name": json_result["dealership_name"]}

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    response = get_request("https://api.us-south.natural-language-understanding.watson.cloud.ibm.com" \
                            "/instances/661ca984-be0b-4f15-bb58-a37618a465f1/v1/analyze", text=text, 
                            version="2021-08-01", features=["sentiment"], 
                            apikey="3aELsipOmt9M6fyBpCCbeovS4J-42bfXBGBH2l-wJx8U")
    print(response)
    return response["sentiment"]["document"]["label"]