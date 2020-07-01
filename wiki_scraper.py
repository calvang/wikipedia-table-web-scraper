import csv
import json
import sys
import os
import getopt
import requests
from bs4 import BeautifulSoup

# localized stdout silencer
def disable_print(verbose):
    if not verbose:
        sys.stdout = open(os.devnull, 'w')

def main():
    # read and process command line args
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hvco:n:u:',['help','verbose','clean','output=','name=','url='])
    except getopt.GetoptError:
        print('Usage: python3 wiki_scraper.py [OPTIONS]')
        print('    Use -h for more options')
        sys.exit(2)
    verbose = False
    clean = False
    unclean_chars = [';',':',',','#','!','&','*','+','-','–','°']
    output_type = 'csv'
    output_file = 'output'
    wikipedia_url = 'https://en.wikipedia.org/wiki/User:Michael_J/County_table'
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print('Usage: python3 wiki_scraper.py [OPTIONS]')
            print('    -h,--help: open help menu')
            print('    -v,--verbose: print verbose output')
            print('    -c,--clean: remove all special characters from data')
            print('    -o,--output <type>: output data format (csv, json), default output type is csv')
            print('    -n,--name: name of the files to output to (minus file extension (will append an int if multiple')
            print('    -url,--url: address of the wikipedia page with the table, default links to https://en.wikipedia.org/wiki/User:Michael_J/County_table')
            sys.exit(2)
        elif opt in ('-v','--verbose'):
            verbose = True
        elif opt in ('-c','--clean'):
            clean = True
        elif opt in ('-o','--output'):
            output_type = arg
        elif opt in ('-n','--name'):
            output_file = arg       
        elif opt in ('-u','--url'):
            wikipedia_url = arg

    # get the html from the wikipedia page
    get_request = requests.get(wikipedia_url)
    soup = BeautifulSoup(get_request.content, 'html.parser')

    disable_print(verbose)

    name_int = 0
    # scrape each table dataset into a dictionary
    for table in soup.find_all('table'):
        table_dicts = []
        # the following line was fun to write but probably a nightmare to read
        try:
            # '''CONFIG1: table with default counties data
            # if a page didn't work, change the initial column reader to fit the page configuration
            table_cols = [str(col.find(text=True, recursive=False)).strip() + \
                    ' ' + str(col.a.string).strip() \
                    if str(col.find(text=True, recursive=False)).strip() == str(col.a.string).strip() \
                    else str(col.find(text=True)) \
                    for col in table.find_all('th')]
            
            # '''CONFIG2: works for most tables
            # table_cols = [str(col.find(text=True))
            #         for col in table.find_all('th')]
            
            print("Found table with columns:")
            for col in table_cols:
                print(col)

            # insert row data into the dictionary
            col_num = 0
            new_dict = {}
            for row in table.find_all('td'):
                row_txt = (''.join(i for i in str(row.find(text=True)).strip() if not i in unclean_chars)) \
                    if clean else str(row.find(text=True)).strip()
                new_dict[table_cols[col_num]] = row_txt
                print("Read '" + row_txt + "' from column " + str(col_num) + \
                        " with key '" + table_cols[col_num] + "'.")
                
                # wrap around columns
                col_num += 1
                if col_num == len(table_cols):
                    table_dicts.append(new_dict)
                    new_dict = {}
                    col_num = 0

            # write to output file
            if name_int > 0:
                output_file = output_file + str(name_int)
            output_file = os.path.join('.','output',output_file)
            with open(output_file + '.' + output_type, mode='w') as outfile:
                if output_type == 'csv':
                    writer = csv.DictWriter(outfile, table_cols)
                    writer.writeheader()
                    for i in table_dicts:
                        writer.writerow(i)
                elif output_type == 'json':
                    outfile.write(json.dumps(table_dicts,
                            indent=4,
                            sort_keys=True,
                            ensure_ascii=False))
                outfile.close()
            name_int += 1
        except SyntaxError:
            print("SyntaxError: invalid syntax")
        except:
            print("Error: source code may need to be configured to scrape data")

if __name__ == '__main__':
    main()