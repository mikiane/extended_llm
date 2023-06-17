

import os
import argparse
from PyPDF2 import PdfMerger, PdfReader

def merge_pdfs(root_dir, output_file):
    merger = PdfMerger()

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".pdf"):
                merger.append(PdfReader(os.path.join(subdir, file)))
                print("merging \n")


    merger.write(output_file)
    merger.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge all pdf files in a directory into one')
    parser.add_argument('directory', help='Directory to search for pdf files')
    parser.add_argument('output', help='Output file name')

    args = parser.parse_args()

    merge_pdfs(args.directory, args.output)
