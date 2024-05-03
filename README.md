# python-public
Python projects

## Directory structure for packaged python projects
```text
monorepo_name/                           # Root directory of your monorepo
│
├── .git/                                # Git repository metadata (created by Git)
├── .gitignore                           # Gitignore file to specify patterns of files/directories to ignore
├── .github/                             # GitHub-specific configuration files and workflows
│   ├── workflows/                       # Contains GitHub Actions workflow files
│   │   ├── ci_project1.yml              # Continuous integration workflow for project1
│   │   ├── ci_project2.yml              # Continuous integration workflow for project2
│   │   └── ...                          # Other workflow files (e.g., release, documentation, etc.)
│   ├── ISSUE_TEMPLATE/                  # Issue templates for standardizing GitHub issues
│   │   └── bug_report.md                # Template for reporting bugs
│   ├── PULL_REQUEST_TEMPLATE.md         # Pull request template for standardizing PR descriptions
│   └── ...  
├── README.md                            # Top-level README providing overall info about the monorepo
│
├── project1/                            # Directory for the first Python project/package
│   ├── LICENSE                          # License file for project1 specifying the terms of its use
│   ├── README.md                        # Detailed info about project1, how to install, use, etc.
│   ├── setup.py                         # Setup script for installing project1 as a package
│   │                                     (or pyproject.toml for projects using PEP 517/518 standards)
│   ├── requirements.txt                 # List of dependencies needed for project1
│   ├── src/                             # Source code directory for project1
│   │   ├── __init__.py                  # Empty file to make src a Python package
│   │   ├── module/                      # A module within the project1
│   │   │   ├── __init__.py              # Initializes the module
│   │   │   ├── submodule/               # A submodule within the module
│   │   │   │   ├── __init__.py          # Initializes the submodule
│   │   │   │   └── ...                  # Files within the submodule
│   │   │   └── ...                      # Other files within the module
│   │   ├── main.py                      # Main module of project1, often the entry point of the application
│   │   └── ...                          # Other Python modules and packages
│   ├── tests/                           # Test suite for project1
│   │   ├── __init__.py                  # Empty file to make tests a Python package
│   │   ├── test_main.py                 # Test cases for the main module
│   │   └── ...                          # Other test modules and packages
│   ├── docs/                            # Documentation for project1
│   │   └── ...                          # Documentation files like Sphinx docs, markdown, etc.
│   ├── scripts/                         # Scripts related to project1 such as deployment scripts, utility scripts, etc.
│   │   └── ...                          # Script files
│   └── ...                              # Additional directories/files
│
├── project2/                            # Directory for the second Python project/package
│   ├── LICENSE                          # License file for project2
│   ├── README.md                        # Detailed info about project2
│   ├── setup.py                         # Setup script for installing project2 as a package
│   │                                     (or pyproject.toml)
│   ├── requirements.txt                 # List of dependencies needed for project2
│   ├── src/                             # Source code directory for project2
│   │   ├── __init__.py                  # Empty file to make src a Python package
│   │   ├── module/                      # A module within the project2
│   │   │   ├── __init__.py              # Initializes the module
│   │   │   ├── submodule/               # A submodule within the module
│   │   │   │   ├── __init__.py          # Initializes the submodule
│   │   │   │   └── ...                  # Files within the submodule
│   │   │   └── ...                      # Other files within the module
│   │   ├── main.py                      # Main module of project2
│   │   └── ...                          # Other Python modules and packages
│   ├── tests/                           # Test suite for project2
│   │   ├── __init__.py                  # Empty file to make tests a Python package
│   │   ├── test_main.py                 # Test cases for the main module
│   │   └── ...                          # Other test modules and packages
│   ├── docs/                            # Documentation for project2
│   │   └── ...                          # Documentation files like Sphinx docs, markdown, etc.
│   ├── scripts/                         # Scripts related to project2 such as deployment scripts, utility scripts, etc.
│   │   └── ...                          # Script files
│   └── ...                              # Additional directories/files
│
└── shared_resources/                    # (Optional) Shared code or resources across projects
    ├── __init__.py                      # Empty file to make shared_resources a Python package
    ├── shared_module.py                 # A shared module that can be used by multiple projects
    └── ...                              # Other shared modules, libraries, or resources


```

