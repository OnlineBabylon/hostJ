from flask import Flask, jsonify, render_template, request
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_journalists', methods=['GET'])
def fetch_journalists():
    query = request.args.get('query', 'bitcoin')  # Default query parameter set to 'bitcoin'
    
    language = request.args.get('language', 'en')
    page_size = 1

    # Make a request to the News API
    response = newsapi.get_everything(q=query, language=language, page_size=page_size)

    journalists_info = []

    if 'articles' in response:
        article = response['articles'][0]  # Only first article
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
                article_info.update({
                    'email': tomba_data['data']['email'],
                    'first_name': tomba_data['data']['first_name'],
                    'last_name': tomba_data['data']['last_name'],
                    'country': tomba_data['data']['country'],
                    'position': tomba_data['data']['position'],
                    'twitter': tomba_data['data']['twitter'],
                    'linkedin': tomba_data['data']['linkedin'],
                    'company': tomba_data['data']['company']
                })

                # Call Clearbit API to further enrich journalist information
                clearbit_email = tomba_data['data']['email']
                clearbit_url = f'https://person.clearbit.com/v2/combined/find?email={clearbit_email}'
                clearbit_headers = {'Authorization': f'Bearer {clearbit_key}'}
                clearbit_response = requests.get(clearbit_url, headers=clearbit_headers)

                if clearbit_response.status_code == 200:
                    clearbit_data = clearbit_response.json()
                    article_info.update({'clearbit_data': clearbit_data})

            journalists_info.append(article_info)

    return jsonify(journalists_info)

if __name__ == '__main__':
    app.run(debug=True)
