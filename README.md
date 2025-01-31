# Google Image Scraper

## Description
This Python script allows you to scrape images from Google Images based on a specified search query and save them to your local machine. It utilizes Selenium and the Firefox headless web browser to automate the image retrieval process.

**Purpose:** The primary goal of this project is to create a dataset for training machine learning and artificial intelligence models in an automated manner.

## Usage

### Docker
1. Run (and pull, if necessary) the following image, replacing the options as you need:
```bash
docker run -v /path/in/host/output:/app/output --rm caribeedu/google-image-scraper:latest python google_image_scraper.py --query-terms '<query-term>' --pages 1 --output-path /app
```

### Local

1. Clone this repository to your local machine:
```bash
git clone https://github.com/caribeedu/Google-Image-Scraper.git
```
2. Navigate to the project folder:
```bash
cd Google-Image-Scraper
```
3. Install the required Python packages:
```bash
pip install -r requirements.txt
```
4. Run the script:
```bash
python google_image_scraper.py --query-terms 'apple' 'banana' --pages 5 --output-path ./
```

Images matching your query will be downloaded and saved to folder with the same query term name, inside of the `output` folder (will be created if don't exists), which is relative to the `output-path` argument.

## Help

For more information use:
```bash
python google_image_scraper.py --help
```

## Dependencies
- Python 3.x with PIP
- Requests
- Selenium
- Pillow (PIL)
- Firefox
