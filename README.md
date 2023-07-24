# AWS-CloudTrail-Timeline

This tool is designed to help analyze AWS events and generate useful insights in the form of a mindmap and timeline. It enables you to investigate resource access and services used by a specific user.

## Prerequisites

Before using this tool, please ensure you have the following:

- Python installed on your system
- AWS credentials properly configured for accessing relevant AWS services

## Installation

1. Clone the repository: `git clone https://github.com/aleduc-cyb/AWS-CloudTrail-Timeline.git`
2. Change to the project directory: `cd AWS-CloudTrail-Timeline`
3. Install required dependencies: `pip install -r requirements.txt`
4. Install Graphviz: https://www.graphviz.org/download/

## Usage

The tool provides several options to customize the analysis. Here are the available command-line arguments:

- `-m`, `--mindmap`: Print a mindmap with information regarding resources accessed.
- `-t`, `--timeline`: Print a timeline with information regarding services used.
- `-u`, `--username`: Name of the user to investigate.
- `-qd`, `--qradar_data`: Fetch new data in QRadar.
- `-fd`, `--file_data`: Fetch data from a file.
- `-if`, `--input_file`: File from which to fetch data. (Default: data_backup.json)
- `-sd`, `--store_data`: Whether to store data fetched from QRadar in a file.

### Examples

1. To generate a mindmap for a specific user from QRadar:
`python main.py -m -u <username> -qd`

2. To print a timeline of services used by a specific user from file data:
`python main.py -t -u <username> -fd <filename>`

## Contributing

If you would like to contribute to this project or report any issues, please open an issue or submit a pull request on the GitHub repository.

Happy AWS event analysis!