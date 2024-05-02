import sys
import subprocess
import os
from dotenv import load_dotenv
from query import main as get_salesforce_data

# Load environment variables from .env file
load_dotenv()

# Load configurations from .env file
domain_name = os.getenv("SF_DOMAIN_NAME")
api_version = os.getenv("SF_VERSION_NUMBER")
output_directory = os.getenv("OUTPUT_DIRECTORY")
current_sprint_directory = os.getenv("CURRENT_SPRINT_DIRECTORY")

# Define the mapping for event types
EVENT_TYPE_MAPPING = {
    "ApexExecution": "APEX_EXECUTION",
    "ApexTrigger": "APEX_TRIGGER",
    "FlowExecution": "FLOW_EXECUTION",
    "ApexUnexpectedException": "APEX_UNEXPECTED_EXCEPTION",
    "LightningPageView": "LIGHTNING_PAGE_VIEW",
    "API": "API",
    # Add more event type mappings here as needed
}


def download_event_log_files(query_file):
    data, access_token = get_salesforce_data(query_file)

    for record_id, log_date, event_type in data:
        # Format the date to match the desired output
        formatted_date = log_date.split("T")[0]  # Extract date part before 'T'

        # Replace invalid characters for file names if needed
        valid_event_type = event_type.replace("/", "_")

        if valid_event_type in EVENT_TYPE_MAPPING:
            converted_event_type = EVENT_TYPE_MAPPING[valid_event_type]
        else:
            print(
                f"Warning: Unmapped event type '{valid_event_type}'. Using default conversion."
            )
            converted_event_type = valid_event_type.upper()

        # Construct the output directory dynamically based on the current sprint directory and valid_event_type
        dynamic_output_directory = os.path.join(
            current_sprint_directory, converted_event_type
        )

        # Ensure the dynamically created output directory exists
        os.makedirs(os.path.expanduser(dynamic_output_directory), exist_ok=True)

        # Construct the output file name using the formatted date and event type
        output_file_name = f"{formatted_date}_{valid_event_type}.csv"

        # Construct the URL to download the EventLogFile
        download_url = f"https://{domain_name}/services/data/v{api_version}/sobjects/EventLogFile/{record_id}/LogFile"

        # Specify the output file path, ensuring directories in the path are expanded properly
        output_file = os.path.expanduser(
            f"{dynamic_output_directory}/{output_file_name}"
        )

        # Construct the cURL command with authorization header and output file path
        curl_command = [
            "curl",
            download_url,
            "-H",
            f"Authorization: Bearer {access_token}",
            "-H",
            "X-PrettyPrint:1",
            "-o",
            output_file,
        ]

        # Enhance the print statement for better readability
        curl_command_str = (
            " ".join(curl_command[:2])
            + " "
            + " ".join([f'"{arg}"' if " " in arg else arg for arg in curl_command[2:]])
        )
        print(curl_command_str)

        # Execute the cURL command
        try:
            subprocess.run(
                curl_command,
                check=True,
                stdout=subprocess.PIPE,
                universal_newlines=True,
            )
            print(f"Downloaded {record_id} to {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {record_id}: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <PATH_TO_QUERY_FILE>.soql")
        sys.exit(1)

    query_file = sys.argv[1]
    download_event_log_files(query_file)
