## Identify patients with AD in the Confinement table
## Confinement table contains diagnosis, procedures and other information
## The size is conparably small and can be run in the pandas
## Later update the generated pickle file with patients identify from other diagnosis table

import pandas as pd
import csv
import pickle
from datetime import datetime
import numpy as np
import path ## a python file with custom input and output path, and ICD codes

in_path = path.in_path
ot_path = path.out_path+'proc_split/' ## output to root output path with a proc_split subdirectory

## Import ICD codes from icd code list in the path.py
icd9 = path.adrd_code_9
icd10 = path.adrd_code_10


## Find AD patient in Confinement
## patid Patient ID
## diag diagnosis column
## icd_flag 10 for ICD 10 diagnosis; 9 for ICD 9 diagnosis
## fst_dt first diagnosis date in the format of YYYY-MM-DD

df = pd.read_csv() ## Path to the confinement table
df.diag = df.diag.astype(str)

df_adrd = df.loc[((df.icd_flag==9)&(df.diag.isin(icd9)))|
    ((df.icd_flag==10)&(df.diag.isin(icd10)))]

## Print output
print ("First 5 rows of the dataframe: "+'\n')
print(df_adrd.head())

## Check patient count
patient_count = df_adrd.icd_flag.unique()
print("AD patients in the Confinement table totals: "+ patient_count+'\n')

## Check ICD flags
flg_ls = df_adrd.icd_flag.unique().tolist()
print("ICD Flags in the Confinement table: "+ flg_ls+'\n')

## Check Diagnosis codes found in the dataframe
dx_ls = df_adrd.diag.unique().tolist()
print("Diagnosis codes found in the Confinement table: "+ dx_ls+'\n')

## Deduplicate and resort the dataframe by columns patient ID ('patid') and first diagnosis date ('fst_dt')
df_adrd = df_adrd.drop_duplicates()
df_adrd = df_adrd.sort_values(by=['patid', 'fst_dt']).reset_index(drop=True)

## Generate the output as a temp csv
# this file contains AD patients identified in Confinement but it is not all AD in the cohort


df_adrd.to_csv(ot_path+'temp_pat_adrd_conf.csv',sep='\t', index=False)

# next we generate the AD patient list by filtering in the diagnosis table