import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        """
        Initialize the Scraper class.
        """
        self.base_url = "https://www.ancpi.ro/statistica"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

    months_ro = [
        "ianuarie",  # January
        "februarie",  # February
        "martie",  # March
        "aprilie",  # April
        "mai",  # May
        "iunie",  # June
        "iulie",  # July
        "august",  # August
        "septembrie",  # September
        "octombrie",  # October
        "noiembrie",  # November
        "decembrie",  # December
    ]

    def get_soup(self, url: str) -> BeautifulSoup | None:
        """
        Scrape the content from the given URL and get a soup.

        :param url: The URL to scrape.
        :return: The scraped content as a BeautifulsoupObject. 
        If an error occurs, return None.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad responses
            return BeautifulSoup(response.text, "html.parser")

        except requests.RequestException as e:
            print(f"An error occurred while scraping: {e}")
            return None

    def get_attachment_urls(self, soup: BeautifulSoup) -> dict[str, str]:
        """
        Find all URLs associated with the Excel files.

        :param soup: The BeautifulSoup object containing the HTML content.
        :return: A dict of file names and their URLs.
        """
        table = soup.find("div", class_="download-attachments")
        if not table:
            raise ValueError("No attachment icons found in the provided soup.")

        links = table.find_all("a", href=True)
        if not links:
            raise ValueError("No links found in the provided soup.")

        return [{"title": _.get("title"), "link": _.get("href")} for _ in links]

    def get_month_urls(self, range_params: tuple) -> list[str]:
        """
        Construct URLs for months within the specified range.

        :param range_params: Can be:
            - (start_year, end_year): For all months in these years
            - (start_year, start_month_idx, end_year, end_month_idx): For specific month ranges
            where month_idx is 0-based (0=January, 11=December)
        :return: List of constructed URLs for each month in the range.
        """
        urls = []

        if len(range_params) == 2:
            # Simple year range
            start_year, end_year = range_params
            return [
                f"{self.attachment_url}-{month}-{year}"
                for year in range(start_year, end_year + 1)
                for month in self.months_ro
            ]

        elif len(range_params) == 4:
            # Specific month range
            start_year, start_month_idx, end_year, end_month_idx = range_params

            if start_year > end_year:
                raise ValueError("Start year must be less than or equal to end year.")
            if (end_month_idx < 1 or end_month_idx > 12) or (
                start_month_idx < 1 or start_month_idx > 12
            ):
                raise ValueError("Month indexes must be between 1 and 12.")
            if start_year == end_year and start_month_idx > end_month_idx:
                raise ValueError(
                    "Start month index must be less than or equal to end month index for the same year."
                )

            for year in range(start_year, end_year + 1):
                # Determine month range for current year
                if year == start_year and year == end_year:
                    # Same year - use both start and end month
                    month_start, month_end = start_month_idx, end_month_idx
                elif year == start_year:
                    # First year - start at specified month, end at December
                    month_start, month_end = start_month_idx, 11
                elif year == end_year:
                    # Last year - start at January, end at specified month
                    month_start, month_end = 0, end_month_idx
                else:
                    # Middle year - include all months
                    month_start, month_end = 0, 11

                # Generate URLs for months in this year
                for month_idx in range(month_start - 1, month_end - 1):
                    month_name = self.months_ro[month_idx]
                    urls.append(f"{self.base_url}-{month_name}-{year}")

        return urls

    def download_file(self, url: str, path: str) -> None:
        """
        Download the file from the given URL and save it to the specified directory.

        :param url: The URL of the file to download.
        :param path: The directory and filename where the file will be saved.
        """
        try:
            response = requests.get(url, headers=self.headers, allow_redirects=True)
            response.raise_for_status()  # Raise an error for bad responses
    
            with open(path, "wb") as file:
                file.write(response.content)
            print(f"Downloaded: {path}")

        except requests.RequestException as e:
            print(f"An error occurred while downloading {url}: {e}")
