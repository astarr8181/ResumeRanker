#!/usr/bin/env python

import PyPDF2
import re
import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
from collections import Counter
import os
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
import seaborn as sns

def main():
    file = 'Combined.pdf'
    parse_promotion_packages(file)

def parse_promotion_packages(file):
    pdf = open(file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    countpage= pdf_reader.getNumPages()
    count = 0
    text = []

    while count < countpage:
        pdf = pdf_reader.getPage(count)
        t = pdf.extractText()
        count += 1
        text.append(t)
    text = str(text)

    regex = r'Employee\s*ID\s*\d*'
    emp_Ids = re.findall(regex, text)

    emp_Ids = list(set(emp_Ids))
    regex2 = r'Employee\s*ID\s*'
    lines = re.split(regex2, text)
    df = pd.DataFrame({'Lines': lines})

    regex3 = r'Position{1}'
    s= df['Lines'].str.split(regex3, 1, expand=True)
    s=s.iloc[1:]
    s.fillna(value='NA', inplace=True)

    for index, row in s.iterrows():
        filename, text = row[0] + ".txt", row[1]
        with open(filename, 'a') as f:
            f.write(text)

if __name__ == "__main__":
    main()
