# AmarillasBot

## Description

`AmarillasBot` is an automated script developed in Python using Selenium to extract information about nutritionists listed on the Páginas Amarillas website. The bot navigates through the different result pages, collects relevant data, and saves this information in an Excel file. This script is useful for collecting and organizing data on nutritionists, including their names, locations, phone numbers, addresses, websites, and descriptions.

## Features

- Automates web navigation and data extraction using Selenium.
- Handles cookie banners and pagination.
- Collects data such as name, location, phone number, address, website, and description.
- Saves the collected data in an Excel file for easy access and analysis.

## Requirements

- Python 3.x
- Selenium
- pandas
- Chrome WebDriver

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/yourusername/AmarillasBot.git
    ```
2. Install the required packages:
    ```sh
    pip install selenium pandas
    ```
3. Download the Chrome WebDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/) and ensure it is in your PATH.

## Usage

Run the script using Python:
```sh
python amarillas_bot.py
