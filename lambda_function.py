import json
import os
import urllib.request
import urllib.error

def lambda_handler(event, context):
    """
    Fetch current temperature for New York City from OpenWeatherMap API
    """
    try:
        # Get API key from environment variable
        api_key = os.environ.get('API_KEY')
        
        if not api_key:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'error': 'API_KEY environment variable not set'
                })
            }
        
        # NYC coordinates
        city = "New York"
        country_code = "US"
        
        # OpenWeatherMap API endpoint
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=imperial"
        
        # Make API request
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        # Extract temperature data
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description']
        
        # Prepare response
        result = {
            'city': f"{city}, {country_code}",
            'temperature': f"{temperature}°F",
            'feels_like': f"{feels_like}°F",
            'temp_min': f"{temp_min}°F",
            'temp_max': f"{temp_max}°F",
            'humidity': f"{humidity}%",
            'description': description.title(),
            'timestamp': data['dt']
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result, indent=2)
        }
        
    except urllib.error.HTTPError as e:
        error_message = f'API request failed with status {e.code}'
        if e.code == 401:
            error_message = 'Invalid API key. Please check your OpenWeatherMap API key.'
        return {
            'statusCode': e.code,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': error_message
            })
        }
    except urllib.error.URLError as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': f'Network error: {str(e)}'
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': f'Internal error: {str(e)}',
                'error_type': type(e).__name__
            })
        }
