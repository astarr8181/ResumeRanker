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
    file = 'Resumes.pdf'
    parse_resumes(file)


def parse_resumes(file):
    # parses the pdf starting at page 3. The first three pages provided by HD are irrelevant.
    pdf = open(file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf)
    countpage = pdf_reader.getNumPages()
    count = 3
    text = []

    while count < countpage:
        pdf = pdf_reader.getPage(count)
        t = pdf.extractText()
        count += 1
        text.append(t)
    text = str(text)

    #creates a deduplicated list of all applicant ids found in the resumes.
    regex = r'Applicant\s*ID:\d{8}'
    App_Ids = re.findall(regex, text)
    App_Ids = list(set(App_Ids))

    #strips Applicant ID header off of ID
    for i in App_Ids:
        file = i.strip('Applicant ID:')

    #splits text by Applicant ID. Creates a row for ID and text.
    regex2 = r'Applicant\s*ID:'
    lines = re.split(regex2, text)
    df = pd.DataFrame({'Lines': lines})

    s = df['Lines'].str.split('Sponsoring\s*Career\s*Service:', expand=True)
    s.columns = ['Candidate_Id', 'Text']
    s = s.iloc[1:]

    #outputs a .txt file for each candidate id containing text associated with their resume and coverletter.
    for index, row in s.iterrows():
        filename, text = row['Candidate_Id'] + ".txt", row['Text']
        with open(filename, 'a') as f:
            f.write(text)


if __name__ == "__main__":
    file = 'Resumes.pdf'
    parse_resumes(file)
