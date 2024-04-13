from flask import Flask, jsonify, request
from flask_cors import CORS
from newsapi import NewsApiClient
import requests

app = Flask(__name__)
CORS(app)

# Initialize NewsApiClient with your API key
newsapi = NewsApiClient(api_key='0589da1f0c104d66aa335b53862b01d9')
tomba_key = 'ta_348se2nh5um6rvdwn257755866ct4p2uphz3l'
tomba_secret = 'ts_5e7f9eb0-9e93-4067-8ba8-d578f5bd15e3'
clearbit_key = 'sk_3fe7103510df59785b16404c322ba542'

@app.route('/fetch_journalists', methods=['GET'])
def fetch_journalists():
    query = request.args.get('query')
    language = request.args.get('language', 'en')
    page_size = 1

    # Make a request to the News API
    response = newsapi.get_everything(q=query, language=language, page_size=page_size)

    journalists_info = []

    if 'articles' in response:
        article = response['articles'] 
        # [0]  # Only first article
        if 'author' in article and article['author'] is not None:
            article_info = {
                'author': article['author'],
                'publication': article['source']['name'],
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'urlToImage': article['urlToImage'],
                'publishedAt': article['publishedAt']
            }

            # Call Tomba API to enrich author information
            tomba_params = {'url': article['url']}
            tomba_headers = {'content-type': 'application/json', 'X-Tomba-Key': tomba_key, 'X-Tomba-Secret': tomba_secret}
            tomba_url = 'https://api.tomba.io/v1/author-finder'
            tomba_response = requests.get(tomba_url, params=tomba_params, headers=tomba_headers)

            if tomba_response.status_code == 200:
                tomba_data = tomba_response.json()
                if 'email' in tomba_data['data'] and tomba_data['data']['email']:
                    clearbit_email = tomba_data['data']['email']
                    clearbit_url = f'https://person.clearbit.com/v2/combined/find?email={clearbit_email}'
                    clearbit_headers = {'Authorization': f'Bearer {clearbit_key}'}
                    clearbit_response = requests.get(clearbit_url, headers=clearbit_headers)

                    if clearbit_response.status_code == 200:
                        clearbit_data = clearbit_response.json()
                        person_data = {
                            'Name': clearbit_data.get('person', {}).get('name', {}).get('fullName'),
                            'Given Name': clearbit_data.get('person', {}).get('name', {}).get('givenName'),
                            'Family Name': clearbit_data.get('person', {}).get('name', {}).get('familyName'),
                            'Email': clearbit_data.get('person', {}).get('email'),
                            'Location': clearbit_data.get('person', {}).get('location'),
                            'Time Zone': clearbit_data.get('person', {}).get('timeZone'),
                            'Bio': clearbit_data.get('person', {}).get('bio'),
                            'Avatar': clearbit_data.get('person', {}).get('avatar'),
                            'Employment': clearbit_data.get('person', {}).get('employment', {}).get('name'),
                            'Title': clearbit_data.get('person', {}).get('employment', {}).get('title'),
                            'Linkedin': clearbit_data.get('person', {}).get('linkedin', {}).get('handle'),
                            'Twitter': clearbit_data.get('person', {}).get('twitter', {}).get('handle'),
                            'Facebook': clearbit_data.get('person', {}).get('facebook', {}).get('handle'),
                            'Github': clearbit_data.get('person', {}).get('github', {}).get('handle')
                        }
                        company_data = {
                            'Name': clearbit_data.get('company', {}).get('name'),
                            'Legal Name': clearbit_data.get('company', {}).get('legalName'),
                            'Domain': clearbit_data.get('company', {}).get('domain'),
                            'Description': clearbit_data.get('company', {}).get('description'),
                            'Location': clearbit_data.get('company', {}).get('location'),
                            'Time Zone': clearbit_data.get('company', {}).get('timeZone'),
                            'Logo': clearbit_data.get('company', {}).get('logo'),
                            'Phone': clearbit_data.get('company', {}).get('phone'),
                            'Facebook': clearbit_data.get('company', {}).get('facebook', {}).get('handle'),
                            'Linkedin': clearbit_data.get('company', {}).get('linkedin', {}).get('handle'),
                            'Twitter': clearbit_data.get('company', {}).get('twitter', {}).get('handle'),
                            'Alexa US Rank': clearbit_data.get('company', {}).get('metrics', {}).get('alexaUsRank'),
                            'Alexa Global Rank': clearbit_data.get('company', {}).get('metrics', {}).get('alexaGlobalRank'),
                            'Traffic Rank': clearbit_data.get('company', {}).get('metrics', {}).get('trafficRank'),
                            'Employees': clearbit_data.get('company', {}).get('metrics', {}).get('employees'),
                            'Employees Range': clearbit_data.get('company', {}).get('metrics', {}).get('employeesRange'),
                            'Estimated Annual Revenue': clearbit_data.get('company', {}).get('metrics', {}).get('estimatedAnnualRevenue')
                        }
                        article_info.update({'Person': person_data, 'Company': company_data})
                    else:
                        clearbit_error = clearbit_response.json()
                        article_info.update({'Clearbit Error': clearbit_error})
                else:
                    tomba_error = "Tomba API did not return a valid email address."
                    article_info.update({'Tomba Error': tomba_error})

            journalists_info.append(article_info)

    return jsonify(journalists_info)

if __name__ == '__main__':
    app.run(debug=True)
