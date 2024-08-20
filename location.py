from flask import Flask, request, jsonify, render_template_string
import regex as re
import requests

app = Flask(__name__)

def get_final_url(short_url):
    # Send a request to the short URL and allow redirects
    response = requests.get(short_url, allow_redirects=True)
    # Return the final URL after redirection
    return response.url

def extract_lat_lng_from_url(url):
    # Decode URL encoding to ensure '+' signs are correctly interpreted
    url = requests.utils.unquote(url)

    # Regex patterns to match different coordinate formats in the URL
    patterns = [
        r'[@/](-?\d+\.\d+),(\+?-?\d+\.\d+)[,?]',  # Match @lat,lng
        r'(-?\d+\.\d+),(-?\d+\.\d+)'     # Match lat,lng anywhere in the URL
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            # Extract latitude and longitude from the match groups
            lat, lng = match.groups()
            return float(lat), float(lng)

    # No coordinates found
    return None, None


# Route for the HTML form
@app.route('/')
def index():
    form_html = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>URL Expander and Coordinates Extractor</title>
      </head>
      <body>
        <div style="margin: 50px;">
          <h1>Enter a Short URL</h1>
          <form action="/expand_and_extract" method="post">
            <label for="short_url">Short URL:</label><br><br>
            <input type="text" id="short_url" name="short_url" style="width: 300px;"><br><br>
            <input type="submit" value="Submit">
          </form>
        </div>
      </body>
    </html>
    '''
    return render_template_string(form_html)

# Route that handles the form submission
@app.route('/expand_and_extract', methods=['POST'])
def expand_and_extract():
    short_url = request.form['short_url']
    if not short_url:
        return "No URL provided", 400

    # Get the final URL
    final_url = get_final_url(short_url)

    # Extract latitude and longitude
    lat, lng = extract_lat_lng_from_url(final_url)

    if lat is None or lng is None:
        return f"<p>Final URL: {final_url}</p><p>No coordinates found in the URL.</p>", 404

    # Return the result as an HTML response
    result_html = f'''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Results</title>
      </head>
      <body>
        <div style="margin: 50px;">
          <h2>Results</h2>
          <p><strong>Final URL:</strong> {final_url}</p>
          <p><strong>Latitude:</strong> {lat}</p>
          <p><strong>Longitude:</strong> {lng}</p>
        </div>
      </body>
    </html>
    '''
    return render_template_string(result_html)

if __name__ == '__main__':
    app.run(debug=False)
