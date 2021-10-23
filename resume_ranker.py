#!/usr/bin/env python
import spacy
from spacy.matcher import PhraseMatcher
from collections import Counter
import pandas as pd
import os
import numpy as np
import os
from os import listdir
from os.path import isfile, join
from io import StringIO
import seaborn as sns


path= '/Resumes/'
nlp = spacy.load('en')
keywords = pd.read_csv('Keywords.csv')
final_output = pd.DataFrame()

for file in os.listdir(path):
    candidate = os.path.splitext(file)[0]
    f = open(file, 'r')
    raw = str(f.read()).lower()
    doc = nlp(raw)

    words = [nlp(text) for text in keywords['Criteria'].dropna(axis = 0)]
    matcher = PhraseMatcher(nlp.vocab)
    matcher.add('Key_words', None, *words)
    matches = matcher(doc)

    d = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        rule_id = nlp.vocab.strings[match_id]
        span = doc[start : end] # get the matched slice of the doc
        d.append((rule_id, span.text))
        key_words = "\n".join(f'{i[0]} {i[1]} ({j})' for i,j in Counter(d).items())

    df = pd.read_csv(StringIO(key_words),names = ['Keywords_List'])
    df1 = pd.DataFrame(df.Keywords_List.str.split(' ',1).tolist(),columns = ['Subject','Keyword'])
    df2 = pd.DataFrame(df1.Keyword.str.split('(',1).tolist(),columns = ['Keyword', 'Count'])
    df3 = pd.concat([df1['Subject'],df2['Keyword'], df2['Count']], axis =1)
    df3['Count'] = df3['Count'].apply(lambda x: x.rstrip(")"))
    df3['Candidate'] = candidate
    final_output = final_output.append(df3)

final_output['Count'] =final_output['Count'].astype(int)
final_output['Keyword'] = final_output['Keyword'].astype(str)
final_output['Keyword']=final_output['Keyword'].map(lambda x:x.strip())
final_output['Count']= np.where(final_output['Keyword']=='date',0,final_output['Count'])
final_output.to_excel('resume_keyword_count.xlsx')
df = pd.merge(final_output.dropna(), keywords.dropna(), how='left', left_on= 'Keyword', right_on = 'Criteria')
#df =df.drop(columns = ['Subject', 'Criteria'])
df['Score'] = df['Count']
df_agg = df.groupby('Candidate')['Score'].sum()
df_agg = pd.DataFrame(df_agg).sort_values(by='Score', ascending=False)
df_agg.to_excel('ranked_candidate.xlsx')
descriptive_stats = df_agg.describe()
descriptive_stats.to_excel('candidate_descriptive_stats.xlsx')
df2 = final_output.groupby('Keyword')['Count'].sum()
df2= pd.DataFrame(df2).sort_values(by='Count', ascending=False).to_excel('keywords_stats.xlsx')
df2= pd.read_excel('keywords_stats.xlsx')

#creates a bar chart of the counts for the top 10 keywords across all candidates.
df2 = df2.nlargest(10 ,columns ='Count')
plt = sns.barplot(x='Keyword', y='Count', data=df2, palette='GnBu_d')
plt.set(ylabel='Frequency')
plt.set(title='Frequency of Most Common Keywords')
for x_ticks in plt.get_xticklabels():
    x_ticks.set_rotation(30)
fig =plt.get_figure()
fig.savefig('Word_Frequency.png')
