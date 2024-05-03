#!/bin/bash

# Check if a package name was provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <PackageName>"
    exit 1
fi

# Assign the first argument to the variable 'package_name'
package_name="$1"

# Define the path to the setup.py file
setup_file="setup.py"

# Check if the setup.py file already exists
if [ ! -f "$setup_file" ]; then
    # The file doesn't exist, so create it with content including the package name
    cat > "$setup_file" <<EOL
from setuptools import setup, find_packages

setup(
    name='$package_name',
    version='0.1.0',
    packages=find_packages(),
    # Add additional fields as necessary
)
EOL
    echo "setup.py file has been created with the package name '$package_name'."
else
    # The file already exists
    echo "setup.py file already exists."
fi


# Run command from Project root
pip install -e .

: <<'END_COMMENT'
from setuptools import setup, find_packages

setup(
    name='your_package_name',
    version='0.1',
    packages=find_packages(),
)
END_COMMENT