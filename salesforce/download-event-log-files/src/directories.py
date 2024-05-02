import os
import sys
from dotenv import load_dotenv  # pip install python-dotenv

# Load environment variables from .env file
load_dotenv()


def create_directory_structure(
    base_dir, financial_year, quarter, sprint_name, event_types
):
    # Expand the user's home directory (~) if used in the base_dir
    base_dir = os.path.expanduser(base_dir)

    for original_event_type, directory_name in event_types.items():
        # Construct the full directory path for each event type
        full_dir_path = os.path.join(
            base_dir, financial_year, quarter, sprint_name, directory_name
        )

        # Create the directory structure
        os.makedirs(full_dir_path, exist_ok=True)

        print(f"Directory created: {full_dir_path}")


# Check if the correct number of arguments is provided
if len(sys.argv) != 4:
    print("Usage: python create_directories.py <FinancialYear> <Quarter> <SprintName>")
    sys.exit(1)

# Parse the command line arguments
financial_year = sys.argv[1]
quarter = sys.argv[2]
sprint_name = sys.argv[3]

# Define your base directory
base_directory = os.getenv("EVENT_LOG_BASE_DIR")

# Event types mapping
event_types_mapping = {
    "ApexExecution": "APEX_EXECUTION",
    "ApexTrigger": "APEX_TRIGGER",
    "FlowExecution": "FLOW_EXECUTION",
    "ApexUnexpectedException": "APEX_UNEXPECTED_EXCEPTION",
    "LightningPageView": "LIGHTNING_PAGE_VIEW",
    "API": "API",
    # Add more event type mappings here as needed
}

# Create the directory structure for each event type
create_directory_structure(
    base_directory, financial_year, quarter, sprint_name, event_types_mapping
)
