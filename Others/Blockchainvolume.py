from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import re
import time
import glob
import numpy as np
import os
import traceback


def getlatestheight():
    url = 'https://www.blockchain.com/explorer'
    html = urlopen(url)
    bsyc = BeautifulSoup(html.read(), "lxml")
    table = bsyc.find_all('table', {'class': "table table-striped"})
    block = table[0].find_all('tr')[1].find('td').find('a').contents[0]  # get the latest block height number
    return int(block)


def getcheckpoint():  # find the latest checkpoint in the folder
    result_files = glob.glob("results*.npy")

    checkpoint = 0

    for i in result_files:
        pat = r'(\d+)'
        m = re.findall(pat, i)

        if len(m) > 0:
            if int(m[0]) > checkpoint:
                checkpoint = int(m[0])

    return checkpoint


def loadurl(url):
    try:
        html = urlopen(url)
        bsyc = BeautifulSoup(html.read(), "lxml")  # conver the htiml websit to beautifulsoup
        table_list = bsyc.findAll('table', {'class': "table table-striped"})  # find the table we want
        tc_table = table_list[0]
        tc = tc_table.find_all('td')  # find the element in the table
        list1 = []
        for i in tc:
            for c in i:
                list1.append(c)  # store all the element in the table
        volumn = float(list1[27].contents[0].replace(',', '').replace(' BTC', ''))  # get the element we want
        time = str(list1[15][0:10])
        return volumn, time
    except:
        try:
            volumn = float(list1[23].contents[0].replace(',', '').replace(' BTC',
                                                                          ''))  # the website has anti-spider function and sometimes will change the location of the element, so we just find the new location of the element we need
            time = str(list1[13][0:10])
            return volumn, time
        except:
            try:
                volumn = float(list1[31].contents[0].replace(',', '').replace(' BTC', ''))
                time = str(list1[17][0:10])
                return volumn, time
            except:
                print(url)
                volumn = float(list1[25].contents[0].replace(',', '').replace(' BTC', ''))
                time = str(list1[15][0:10])
                return volumn, time


# Delete file function
def remove(path):
    """ param <path> could either be relative or absolute. """
    if debug:
        print("Remove " + path)
    if os.path.isfile(path):
        os.remove(path)  # remove the file
    elif os.path.isdir(path):
        shutil.rmtree(path)  # remove dir and all contains


def scrap(start=1):
    # Choose the start blocks to scrap
    if start > 1:  # Continue from the last break
        results = np.load('results' + str(start) + '.npy').item()
    else:  # Start from the begining of the block
        results = dict()

    # Save the current block
    checkpoint = start

    try:
        for i in range(0, (len(urls) - start) // fact + 1):
            start_time = time.time()

            # Multiple threads for scrap
            with ThreadPoolExecutor(max_workers=max_workers) as executor:

                end = start + fact * (i + 1)
                if end > len(urls):
                    end = len(urls) + 1

                # Create threads
                futures = {executor.submit(loadurl, url) for url in urls[checkpoint:end]}

                # as_completed() gives you the threads once finished
                for f in as_completed(futures):

                    # Get the results 
                    rs = f.result()

                    if rs[1] in results.keys():
                        results[rs[1]] += rs[0]
                    else:
                        results[rs[1]] = rs[0]

                elapsed_time = time.time() - start_time

                # Calculate time elapsed for this scrap
                e = int(time.time() - start_time)

                # Everthing Okay, update the latest checkpoint
                checkpoint = end

                # Save result to file
                np.save('results' + str(checkpoint) + '.npy', results)

                # Only keep the lastest three files
                remove('results' + str(checkpoint - fact * 3) + '.npy')

                print("Range: " + str(checkpoint) + " ",
                      '{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))
    except:
        if debug:
            traceback.print_exc()
        print("Exception, re-call function main(%s)" % (str(checkpoint)))
        time.sleep(3)

        # Exception happend, restart from the last checkpoint
        scrap(checkpoint)


if __name__ == "__main__":
    urls = []
    web = 'https://www.blockchain.com/btc/block-height/'

    latestblock = getlatestheight()
    for i in range(1, latestblock):
        urls.append(web + str(i))

    # Enable/Disable exception details and some other useful debug information        
    debug = False

    # Define maxium threads for multiple scrap
    max_workers = 10

    # Define incremental blocks for multiple scrap each time
    fact = 100

    start = getcheckpoint()

    scrap(start)
