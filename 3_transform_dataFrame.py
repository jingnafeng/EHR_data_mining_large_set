import pandas as pd
import csv
import sys
import pickle
import os
from datetime import datetime
import path

in_path = path.in_path
ot_path = path.out_path

"""
Confinement table
"""
## Import files
filename = '_hypertension_confinement'
raw = pd.read_csv(in_path+filename+'.csv', delimiter = '\t')

#
output_sub = ot_path+'diag_split/' 
"""
Confinement: Select diagnosis records
"""
cl = ['patid', 'admit_date','icd_flag', 'diag1', 'diag2','diag3','diag4','diag5'] 
dx = raw[cl]
dx = dx.drop_duplicates()
print(dx.patid.nunique()) # 4,669,162

## Data impute
dx = dx.fillna('-1')

# Melt to datamodel the team use:
dx = pd.melt(dx, id_vars = ['patid','admit_date','icd_flag'], value_vars=['diag1', 'diag2','diag3','diag4','diag5'])

dx = dx.drop(columns = 'variable')

dx = dx.rename({'value':'diag'},axis=1)

## Dedupe and exclude null
err_ls = ['00000','-------']
dx.loc[dx.diag.isin(err_ls)] # 4,258 records in hypertension adrd confinement

dx = dx.loc[~dx.diag.isin(err_ls)]
dx = dx.loc[dx.diag!='-1']
dx.icd_flag = dx.icd_flag.astype(int)
dx = dx.drop_duplicates()

print(dx.info())
## Output
dx.to_csv(output_sub+"confinement_diagnosis.csv",index=False)

"""
Confinement: Select procedure records
"""
output_sub=ot_path+'proc_split/'
cl = ['patid', 'admit_date','icd_flag', 'proc1', 'proc2','proc3','proc4','proc5'] 
dx = raw[cl]
dx = pd.melt(dx, id_vars = ['patid','admit_date','icd_flag'], value_vars=['proc1', 'proc2','proc3','proc4','proc5'])

dx = dx.drop(columns = 'variable')

dx = dx.rename({'value':'proc'},axis=1)

dx.icd_flag = dx.icd_flag.astype(int)

err_ls = ['00000','0000000','-------','0000000000']
dx = dx.loc[~dx.proc.isin(err_ls)]
dx = dx.loc[dx.proc!='-1']
dx = dx.drop_duplicates()

dx.rename({'admit_date':'fst_dt'},axis =1,inplace=True)
dx.info()

dx.to_csv(output_sub+'confinement_proc.csv',index=False)

"""
Procedure Table: Select procedure records
"""

## Import files
filename = 'xx_hypertension_procedure'

raw = pd.read_csv(in_path+filename+'.csv', delimiter = '\t')
dx = raw
dx = dx.fillna('-1')
dx = dx.drop_duplicates()
err_ls = ['00000','0000000','-------','0000000000','0000000', '0000000']
dx = dx.loc[~dx.proc.isin(err_ls)]
dx = dx.loc[dx.proc!='-1']
dx = dx.drop_duplicates()
dx.info()

dx.to_csv(output_sub+'procedure_proc.csv',index=False)