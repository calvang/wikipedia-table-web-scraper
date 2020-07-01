import csv
import json
import sys
import os
import contextlib
import getopt
import requests
from bs4 import BeautifulSoup

# localized stdout silencer
def disable_print(verbose):
    if not verbose:
        f = open(os.devnull, "w") 
        contextlib.redirect_stdout(f)

def main():
    # read and process command line args
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hvco:',['help=','verbose=','clean=','output='])
    except getopt.GetoptError:
        print('Usage: python3 wiki_scraper.py [OPTIONS] -o <type>')
        print('    Use -h for more options')
        sys.exit(2)
    verbose = False
    clean = False
    output_type = 'csv'
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print('Usage: python3 wiki_scraper.py [OPTIONS] -o (--output)')
            print('    -h,--help: open help menu')
            print('    -v,--verbose: print verbose output')
            print('    -c,--clean: remove all special characters from data')
            print('    -o,--output <type>: output data format (csv, json), default output type is csv')
            sys.exit(2)
        elif opt in ('-v','--verbose'):
            verbose = True
        elif opt in ('-c','--clean'):
            clean = True        

    wikipedia_url = 'https://en.wikipedia.org/wiki/User:Michael_J/County_table'

    # get the html from the wikipedia page
    get_request = requests.get(wikipedia_url)
    soup = BeautifulSoup(get_request.content, 'html.parser')

    disable_print(verbose)

    # scrape each table dataset into a dictionary
    for table in soup.find_all('table'):
        table_dict = {}
        # the following line was fun to write but probably a nightmare to read
        table_cols = [str(col.find(text=True, recursive=False)).strip() + \
                ' ' + str(col.a.string).strip() \
                if str(col.find(text=True, recursive=False)).strip() == str(col.a.string).strip() \
                else str(col.find(text=True)) \
                for col in table.find_all('th')]
        
        print("Found table with columns:")
        for col in table_cols:
            print(col)
        
        # insert row data into the dictionary
        col_num = 0
        for row in table.find_all('td'):
            row_txt = str(row.find(text=True)).strip()
            table_dict[table_cols[col_num]] = row_txt
            print("Read '" + row_txt + "' from column " + str(col_num) + \
                    " with key '" + table_cols[col_num] + "'.")
            
            # wrap around columns
            col_num += 1
            if col_num == len(table_cols[col_num]):
                col_num = 0

if __name__ == '__main__':
    main()