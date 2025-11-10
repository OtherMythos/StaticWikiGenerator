#!/usr/bin/python3

import argparse
import re
from pathlib import Path
import sqlite3

def writePage(targetOutput, title, text):
    #Write the values out.
    targetPath = title + ".txt"
    finalPath = targetOutput / Path(targetPath)
    print("writing page: %s" % finalPath)
    with open(finalPath, 'w') as out:
        out.write(text)

def main():
    helpText = '''Produce a list of text files from a sqlite database.'''

    parser = argparse.ArgumentParser(description = helpText)

    parser.add_argument('inputFile', metavar='I', type=str, nargs='?', help='A path to an input sqlite file.')
    parser.add_argument('outputDirectory', metavar='O', type=str, nargs='?', help='The path of where to put the found pages.')

    args = parser.parse_args()

    targetPath = args.inputFile
    if(targetPath is None):
        print("Please provide an input database file path.")
        return
    targetOutput = args.outputDirectory
    if(targetOutput is None):
        print("Please provide an output directory path.")
        return
    targetPath = Path(targetPath)
    if not targetPath.exists() or not targetPath.is_file():
        print("Error reading input database file")
        return
    targetOutputPath = Path(targetOutput)
    if not targetOutputPath.exists() or not targetOutputPath.is_dir():
        print("Provided output directory does not exist.")
        return


    #Read the values from the table.
    conn = sqlite3.connect(str(targetPath))
    c = conn.cursor()

    #Gather all the text in the database.
    c.execute('SELECT * FROM page')
    foundIds = []
    for row in c:
        if '/' in row[2]:
            continue
        foundIds.append( (row[2], row[9]) )


    for i in foundIds:
        c.execute('select * from slots where slot_revision_id = %s' % i[1])
        for slot in c:
            #Should only be the one.
            c.execute('select * from text where old_id = %s' % slot[2])
            for text in c:
                writePage(targetOutputPath, i[0], text[1])
            break

    return

    foundPages = []
    for i in foundIds:
        #Loop through slots, find entry number 3 for a match, take the first id.
        #Go through pages and find the entry 10?, should be the page.
        c.execute('SELECT * FROM slots')
        for slot in c:
            if i[0] == slot[2]:
                #print("Found id with value %i" % slot[0])
                #print(slot)
                c.execute('SELECT * FROM page')
                for page in c:
                    #print(page)
                    if page[9] == slot[0]:
                        print("Found page with id %s" % page[2])
                        foundPages.append(page[2])

    if not foundPages:
        print("No pages flagged for deletion found")
        return

    #close the connection
    conn.close()

if __name__ == "__main__":
    main()

