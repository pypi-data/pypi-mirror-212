import re
import json
import sys
from datetime import datetime
import pytz
import requests


def fetch_airtable_data(url, output_file=None):
    # Headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/113.0"
    }

    # Create session
    session = requests.Session()

    # Get the view fetch URL and cookies
    response = session.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the HTML content
        html = response.text

        # Extract URL with params
        url_with_params_pattern = r'urlWithParams: "(.*?)"'
        url_with_params_match = re.search(url_with_params_pattern, html)
        url_with_params = url_with_params_match.group(1) if url_with_params_match else None

        # Decode Unicode characters
        decoded_url = bytes(url_with_params, "utf-8").decode("unicode_escape")

        # Extract the headers variable using regex
        match = re.search(r"var headers = ({.*?});", html, re.DOTALL)

        if match:
            headers_dict = match.group(1)
            headers_dict = {**json.loads(headers_dict),
                            'x-time-zone': datetime.now(pytz.timezone('UTC')).strftime('%Z')}
            final_resp = session.get(f"https://airtable.com{decoded_url}", headers=headers_dict)
            data = final_resp.text

            if output_file:
                with open(output_file, 'w') as f:
                    parsed_data = json.loads(data)
                    json.dump(parsed_data, f, indent=2)
                print(f"Data written to file: {output_file}")
            else:
                parsed_data = json.loads(data)
                formatted_data = json.dumps(parsed_data, indent=2)
                print(formatted_data)
        else:
            print("Headers variable not found.")

    else:
        print("Failed to retrieve HTML from URL. Status code:", response.status_code)


def main():
    if len(sys.argv) < 2:
        print("Please provide the shared view URL as a command-line argument.")
    else:
        shared_view_url = sys.argv[1]
        output_file = None

        if len(sys.argv) > 2 and sys.argv[2] == "-o":
            if len(sys.argv) > 3:
                output_file = sys.argv[3]
            else:
                print("Please provide the output file name after the -o option.")
                return

        fetch_airtable_data(shared_view_url, output_file)


if __name__ == '__main__':
    main()
