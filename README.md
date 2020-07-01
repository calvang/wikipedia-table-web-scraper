# Wikipedia Table Web Scraper
Simple web scraper using Beautiful Soup for collect data into .csv and .json files.

### Description:
Created to scrape data from wikipedia for county centroids. I ended up updating some features so that it can run on many different Wikipedia tables.

### Installation
Set up your virtual environment and activate it:
`python3 -m venv env`
`source env/bin/activate`
Install packages:
`pip install -r requirements.txt`

### Usage
To run this script:
```
python3 wiki_scraper.py [OPTIONS]
    -h,--help: open help menu
    -v,--verbose: print verbose output
    -c,--clean: remove all special characters from data
    -o,--output <type>: output data format (csv, json), default output type is csv
    -n,--name: name of the files to output to (minus file extension (will append an int if multiple
    -url,--url: address of the wikipedia page with the table, default links to https://en.wikipedia.org/wiki/User:Michael_J/County_table
```