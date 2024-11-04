import pandas as pd
import numpy as np
import csv
from collections import OrderedDict
import data_util_ehr as util 
import pickle
import os
import datetime
import path

in_path = path.in_path
ot_path = path.out_path


## Replace member enrollment table here:
## Source file has these columns: #cl = ['patid','eligeff','eligend','gdr_cd','yrdob','extract_ym']
pat = pd.read_csv(in_path+'Sori_hypertension_mbr_co_enroll.csv', low_memory=False, delimiter='\t')


ct = pat.patid.nunique()
print("Enrollment count: "+ct+'\n')

## Make a copy of the original file with name co
co = pat
co['observation_y'] = abs(co.eligeff.str[:4].astype(int)-co.eligend.str[:4].astype(int))
co_min = co.observation_y.min()
print ("Minimum years of observation: "+co_min+'\n')

## Filter to 3 or more years
co = co.loc[co.observation_y>=3]

## New dataframe with selected columns, dedup, resort:
df = co[['patid','yrdob','gdr_cd', 'observation_y']]
df = df.drop_duplicates().reset_index(drop=True)

## Print some info of df:
pid_ct = df.patid.nunique()
ob_max = df.observation_y.max()
print("Patients who have 3 years or more observation: "+pid_ct+'\n' )
print("Maximum observation year in record: "+ob_max+'\n' )

## Output new files:
df.to_csv(ot_path+'patients_demo_3yr.csv', sep='\t', index=False)
