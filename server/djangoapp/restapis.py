import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 \
    import Features, SentimentOptions

def get_request(url, **kwargs):
    
    api_key = kwargs.get("api_key")
    try:
        if api_key:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        print("Some error is occured")

    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    print(json_payload)
    try:
        requests.post(url, params=kwargs, json=json_payload)

    except:
            print("Some error is occured")


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer["doc"]
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"], state=dealer_doc["state"])
            results.append(dealer_obj)

    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    json_result = get_request(url, id=id)

    if json_result:
        reviews = json_result["data"]["docs"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                    name=dealer_review["name"],
                                    purchase=dealer_review["purchase"],
                                    review=dealer_review["review"],
                                    purchase_date=dealer_review["purchase_date"],
                                    car_make=dealer_review["car_make"],
                                    car_model=dealer_review["car_model"],
                                    car_year=dealer_review["car_year"])
            
            sentiment = analyze_review_sentiments(review_obj.review)
            review_obj.sentiment = sentiment
            results.append(review_obj)
    
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text

def analyze_review_sentiments(text): 

    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/7655942e-e08f-4aa7-bd55-1bbd59fd40f9" 
    api_key = "XxLHUQmavlTrH_nWhHD_06iT0e7c2J9DV6VD29CFdHpE" 

    authenticator = IAMAuthenticator(api_key) 

    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2022-04-07',authenticator=authenticator) 

    natural_language_understanding.set_service_url(url) 

    try:
        response = natural_language_understanding.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 

        label=json.dumps(response, indent=2) 

        label = response['sentiment']['document']['label'] 
    
    except:
        label = 'neutral'

    return(label) 


