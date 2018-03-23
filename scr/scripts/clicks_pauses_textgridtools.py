

# coding: utf-8

# This script copies pause intervals onto a new pause tier for the GECO corpus. It copies also filled pause intervals, inbreath intervals and click intervals into separate three tiers. ZM

# In[1]:


from __future__ import division
from glob import glob


# In[2]:


import tgt as tgt
#import mumodo
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import itertools


# In[3]:

import sys

for arg in sys.argv:
    print arg

os.chdir("/Volumes/Marine_WD_Elements/case_study_2/")


# In[13]:


f=[]

#for path in glob('*.TextGrid'):
path = sys.argv[1]
print "Processing file: " + path
tgt1 = tgt.read_textgrid(path, encoding='utf-8')
file_id = os.path.basename(path)[:-9]
MAU = tgt1.get_tier_by_name('MAU')

c1 = tgt1.get_tier_by_name('clicks')
speech = tgt1.get_tier_by_name('speech')
breathing = speech.get_annotations_with_matching_text('inbr')
silences = speech.get_annotations_with_matching_text('sil')

clic=[]
for interval in c1.annotations:
    inter = [interval.start_time,interval.end_time,interval.text]
    clic.append(inter)
    
my_df = pd.DataFrame(clic)
my_df.to_csv(file_id+'_clicks.txt', header=None, index=None, sep=' ')
#my_df.to_csv(file_id+'_clicks.csv', encoding='utf-16', index=False, header=False)
print(my_df)

br=[]
for interval in breathing:
    inter = [interval.start_time,interval.end_time,interval.text]
    br.append(inter)
    
my_df_br = pd.DataFrame(br)
my_df_br.to_csv(file_id+'_breathing.txt', header=None, index=None, sep=' ')
#my_df_br.to_csv(file_id+'_breathing.csv', encoding='utf-16', index=False, header=False)
print(my_df_br)

si=[]
for interval in silences:
    inter = [interval.start_time,interval.end_time,interval.text]
    si.append(inter)
    
my_df_si = pd.DataFrame(si)
my_df_si.to_csv(file_id+'_silences.txt', header=None, index=None, sep=' ')
#my_df_si.to_csv(file_id+'_silences.csv', encoding='utf-16', index=False, header=False)
print(my_df_si)

# In[5]:


print("Here we are all the data have been extracted!")


