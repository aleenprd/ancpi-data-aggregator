# ANCPI Data Aggregator

A Python tool for scraping and aggregating data from the National Agency for Cadastre and Land Registration of Romania (ANCPI) website.

## Features

- Extract and download attachments (Excel files, PDFs, etc.) from ANCPI's monthly statistical reports
- Filter by date ranges (year and month)
- Save files to customizable output directories
- Provides a simple command-line interface

## Dev Requirements

- Python 3.12 or higher

## Cloud Storage Requirements
Authenticate to your Google Cloud project using OAuth:
- Install [gcloud cli](https://cloud.google.com/sdk/docs/install#mac) for **your platform**.
- Authenticate using `gcloud init` and `gcloud auth application-default login`.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/aleenprd/ancpi-data-aggregator
cd ancpi-data-aggregator
```

2. Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows
```

3. Install the dependencies:

```bash
pip install -e .
```

## Usage

### Command Line Interface

Run the scraper with default settings:

```bash
python main.py
```

Customize the scraping parameters:

```bash
python main.py --start_year 2023 --end_year 2025 --start_month 6 --end_month 3 --output_dir data
```

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--mode` | Mode of the application (scrape or upload). | scrape |
| `--start_year` | Starting year for data collection | 2024 |
| `--end_year` | Ending year for data collection | 2025 |
| `--start_month` | Starting month (1-12) | 1 |
| `--end_month` | Ending month (1-12) | Current month |
| `--output_dir` | Directory to save downloaded files | data |
| `--bucket_name` | The name of cloud storage bucket. | ancpi-aggregator |

## Project Structure

```
ancpi-data-aggregator/
├── ancpi_aggregator/       # Main package
│   └── scraping/          
│       └── scraper.py      # Scraping functionality
├── data/                   # Default output directory (created at runtime)
├── main.py                 # CLI entry point
├── pyproject.toml          # Project metadata and dependencies
└── README.md               # This file

```

## How It Works

1. The tool constructs URLs for ANCPI's monthly statistical pages based on the specified date range
2. It parses each page to find downloadable attachments
3. Attachments are downloaded to your specified output directory
4. Files are organized by month and year

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.