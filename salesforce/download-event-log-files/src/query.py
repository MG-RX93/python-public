import sys
import requests
import os
from dotenv import load_dotenv  # pip install python-dotenv
from auth import get_access_token

# Load environment variables from .env file
load_dotenv()


def run_soql_query(query):
    access_token, instance_url = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    version_number = os.getenv("SF_VERSION_NUMBER")

    # Adjust the version number as per your Salesforce API version
    query_url = f"{instance_url}/services/data/v{version_number}/query/"

    response = requests.get(query_url, headers=headers, params={"q": query})
    if response.status_code == 200:
        return response.json(), access_token
    else:
        raise Exception(f"Query failed: {response.text}")


def main(query_file):
    with open(query_file, "r") as file:
        soql_query = file.read().strip()

    # Run the SOQL query to get the results
    query_result, access_token = run_soql_query(soql_query)

    # Extract record IDs from the query result
    data = [
        (record["Id"], record["LogDate"], record["EventType"])
        for record in query_result["records"]
    ]

    # Return both the record IDs and the access token
    return data, access_token


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <PATH_TO_QUERY_FILE>.soql")
        sys.exit(1)

    query_file = sys.argv[1]

    try:
        record_ids = main(query_file)
        print(record_ids)
    except FileNotFoundError:
        print(f"The file {query_file} does not exist.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
