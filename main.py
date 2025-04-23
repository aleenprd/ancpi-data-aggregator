import os
import argparse
from datetime import datetime
from time import time, sleep
from google.cloud import storage
from ancpi_aggregator import Scraper


def parse_args():
    parser = argparse.ArgumentParser(description="Scrape ANCPI data.")
    parser.add_argument(
        "--mode",
        default="scrape",
        choices=["scrape", "upload"],
        help="Mode of operation: scrape or upload",
        required=False,
    )
    parser.add_argument(
        "--start_year",
        type=int,
        required=False,
        default=2024,
        help="Start year for scraping",
        choices=range(2000, datetime.now().year + 1),
    )
    parser.add_argument(
        "--end_year",
        type=int,
        required=False,
        default=2025,
        help="End year for scraping",
        choices=range(2000, datetime.now().year + 1),
    )
    parser.add_argument(
        "--start_month",
        type=int,
        required=False,
        default=1,
        help="Start month for scraping (1-12)",
        choices=range(1, 13),
    )
    parser.add_argument(
        "--end_month",
        type=int,
        required=False,
        default=12,
        help="End month for scraping (1-12)",
        choices=range(1, datetime.now().month),
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="data",
        help="Directory to save the scraped data",
    )
    parser.add_argument(
        "--sleep_time",
        type=int,
        default=3,
        required=False,
        choices=range(1, 10),
        help="Sleep time between pages in seconds",
    )
    parser.add_argument(
        "--bucket_name",
        type=str,
        default="ancpi-aggregator",
        help="Google Cloud Storage bucket name for uploading files",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clean and transform the scraped data after download"
    )
    
    parser.add_argument(
        "--transform_output_dir",
        type=str,
        default="transformed_data",
        help="Directory to save the transformed data",
    )
    
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"Arguments: {args}")

    if args.mode == "scrape":
        if not os.path.exists(args.output_dir):
            print(f"Creating output directory: {args.output_dir}")
            os.makedirs(args.output_dir)

        print("Initializing scraper...")
        scraper = Scraper()

        print("Generating monthly URLs...")
        month_urls = scraper.get_month_urls(
            (args.start_year, args.start_month, args.end_year, args.end_month)
        )

        print("Fetching files...")
        for url in month_urls:
            print(f"Scraping URL: {url}")

            soup = scraper.get_soup(url)
            if soup is None:
                print(f"Failed to fetch URL: {url}")
                continue
            attachments = scraper.get_attachment_urls(soup)

            for attachment in attachments:
                title, link = attachment["title"], attachment["link"]
                title = title.replace(" ", "_").lower()

                dir = url.split("/")[-1]
                if not os.path.exists(os.path.join(args.output_dir, dir)):
                    os.makedirs(os.path.join(args.output_dir, dir))

                filepath = os.path.join(args.output_dir, dir, f"{title}.xlsx")

                scraper.download_file(link, filepath)

            sleep(args.sleep_time)

    elif args.mode == "upload":
        print("Uploading files to Google Cloud Storage...")
        client = storage.Client()
        bucket = client.get_bucket(args.bucket_name)

        dirs = os.listdir(args.output_dir)
        for dir in dirs:
            print(f"Processing directory: {dir}")
            files = os.listdir(os.path.join(args.output_dir, dir))
            for file in files:
                if file.endswith(".xlsx"):
                    local_path = os.path.join(args.output_dir, dir, file)
                    blob_path = f"{dir}/{file}"
                    blob = bucket.blob(blob_path)
                    blob.upload_from_filename(local_path)


if __name__ == "__main__":
    start_time = time()
    main()
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
