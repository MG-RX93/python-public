import os
import sys
import requests
import json
from datetime import datetime, timedelta
from query import main as get_salesforce_data


# Function to download a file from a given URL
def download_file(url, access_token, destination_folder, file_name):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        os.makedirs(destination_folder, exist_ok=True)
        file_path = os.path.join(destination_folder, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully: {file_path}")
    else:
        print(f"Failed to download file: {response.status_code}")


# Function to create key-value pairs from a record
def create_key_value_pairs(record):
    return {
        "ContentDocumentId": record["ContentDocumentId"],
        "VersionDataUrl": record["VersionDataUrl"],
        "Title": record["Title"],
        "FileExtension": record["FileExtension"],
        "CiscoAlias": record["ContentDocument"]["Owner"]["Cisco_Alias__c"],
    }


# Function to prepare file data for download
def prepare_file_data(key_value_pairs, base_download_folder):
    title = key_value_pairs["Title"]
    content_document_id = key_value_pairs["ContentDocumentId"]
    cisco_alias = key_value_pairs["CiscoAlias"]
    file_extension = key_value_pairs["FileExtension"]

    if title.lower().endswith(f".{file_extension.lower()}"):
        title = title[: -(len(file_extension) + 1)]

    folder_name = f"{title}_{cisco_alias}_{content_document_id}_{file_extension}"
    destination_folder = os.path.join(base_download_folder, folder_name)
    file_name = f"{title}.{file_extension}"

    return destination_folder, file_name


# Function to get Content Document IDs from the query result
def get_content_document_ids(query_result):
    return [record["ContentDocumentId"] for record in query_result["records"]]


# Function to process records and save metadata
def process_records(query_result, access_token, base_download_folder):
    all_key_value_pairs = []

    for record in query_result["records"]:
        key_value_pairs = create_key_value_pairs(record)
        all_key_value_pairs.append(key_value_pairs)

        destination_folder, file_name = prepare_file_data(
            key_value_pairs, base_download_folder
        )
        download_file(
            key_value_pairs["VersionDataUrl"],
            access_token,
            destination_folder,
            file_name,
        )

    metadata_file_path = os.path.join(base_download_folder, "metadata.json")
    os.makedirs(base_download_folder, exist_ok=True)

    # Read existing metadata file content and append new records
    existing_data = []
    if os.path.exists(metadata_file_path):
        with open(metadata_file_path, "r", encoding="utf-8") as f:
            existing_data = json.load(f)

    # Append new key-value pairs to existing data
    updated_data = existing_data + all_key_value_pairs

    # Save updated metadata to file
    with open(metadata_file_path, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)

    print(f"Metadata saved to {metadata_file_path}")


# Main function to control the script's flow
def main(base_download_folder, start_date, end_date):
    createdById = os.getenv("SF_DASHBOARD_UID")
    caseOrigin = os.getenv("SF_CASE_ORIGIN")
    while start_date < end_date:
        batch_end_date = start_date + timedelta(days=1)
        batch_end_date = min(batch_end_date, end_date)

        current_date_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        batch_end_date_str = batch_end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

        # SOQL query with date range
        soql_query_with_dates = f"""
        SELECT ContentDocumentId
        FROM ContentDocumentLink
        WHERE LinkedEntityId IN (
            SELECT Id FROM Case
            WHERE Origin = '{caseOrigin}'
            AND CreatedDate >= {current_date_str}
            AND CreatedDate < {batch_end_date_str}
        )
        AND ContentDocumentId IN (
            SELECT Id FROM ContentDocument
            WHERE CreatedById != '{createdById}'
            AND SharingPrivacy = 'P'
            AND CreatedDate >= {current_date_str}
            AND CreatedDate < {batch_end_date_str}
        )
        ORDER BY ContentDocument.CreatedDate ASC
        """

        try:
            query_result, access_token = get_salesforce_data(soql_query_with_dates)
            content_document_ids = get_content_document_ids(query_result)
        except Exception as e:
            print(f"An error occurred while running the SOQL query: {e}")
            sys.exit(1)

        # Check if content_document_ids is not empty before proceeding
        if content_document_ids:
            formatted_ids = "', '".join(content_document_ids)
            soql_ids = f"'{formatted_ids}'"

            try:
                cv_query = f"SELECT Id, VersionDataUrl, Title, FileExtension, ContentDocumentId, ContentDocument.Owner.Cisco_Alias__c FROM ContentVersion WHERE ContentDocumentId IN ({soql_ids})"
                cv_query_result, access_token = get_salesforce_data(cv_query)
            except Exception as e:
                print(f"An error occurred while running the SOQL query: {e}")
                sys.exit(1)

            process_records(cv_query_result, access_token, base_download_folder)

        start_date = batch_end_date  # Move to the next batch


# Entry point for the script execution
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python download_script.py <BASE_DOWNLOAD_FOLDER> <START_DATE> <END_DATE>"
        )
        sys.exit(1)

    base_download_folder = sys.argv[1]
    start_date = datetime.fromisoformat(sys.argv[2])
    end_date = datetime.fromisoformat(sys.argv[3])
    main(base_download_folder, start_date, end_date)

