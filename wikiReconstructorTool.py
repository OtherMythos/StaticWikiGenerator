#!/usr/bin/python3

from pathlib import Path
from WikiPageParser import *
from WikiPageHtmlGenerator import *
import argparse

def main():
    helpText = '''Test to try and reconstruct a wiki from a yaml file.'''

    parser = argparse.ArgumentParser(description = helpText)
    #position argument
    parser.add_argument("-i", "--input", help="Input directory containing pages.")
    parser.add_argument("-o", "--output", help="Output directory to place the finished files into.")
    args = parser.parse_args()

    if args.input is None:
        print("No input directory provided")
        return
    inputDirpath = Path(args.input).absolute().resolve()
    if args.output is None:
        print("No output directory provided")
        return
    outputDirpath = Path(args.output).absolute().resolve()

    if not inputDirpath.exists() or not inputDirpath.is_dir():
        print("No valid input directory was found.")
        return

    par = WikiPageParser()
    htmlGen = WikiPageHtmlGenerator()
    par.processDirectory(str(inputDirpath))
    par.outputToDirectory(str(outputDirpath), htmlGen)
    htmlGen.writeStyleSheet(outputDirpath / Path("styles.css"))
    htmlGen.writeJavascript(outputDirpath / Path("script.js"), par.totalPages)

main()
