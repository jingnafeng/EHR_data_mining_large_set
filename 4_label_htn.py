"""
Identify diagnosis records in splitted diagnosis files

In the python environment, run this script with the nohup command and logging
"""


import pandas as pd
import os 
import pickle
from datetime import datetime
import numpy as np
import path


cur_time = datetime.now()
print('Start working at: ', cur_time)

in_path = path.in_path
ot_path = path.ot_path+'dx_split/'
ot_label_path = path.ot_path+'hyper/'
hyper_path = path.label_path

# icd9 
icd9_file = 'hyper_code9.txt' 
icd9_df = pd.read_csv(hyper_path+icd9_file, sep=" ", header=None)
icd9_df.columns = ['dx_code']
print('', icd9_df.head(3))
icd9_ls = [str(x) for x in icd9_df.dx_code]
print('\n icd 9 codes to filter: ',icd9_ls[:5])

## icd 10
icd10_file = 'hyper_code10.txt' 
icd10_df = pd.read_csv(hyper_path+icd10_file, sep=" ", header=None)
icd10_df.columns = ['dx_code']
print('', icd10_df.head(3))
icd10_ls = [str(x) for x in icd10_df.dx_code]
print('\n icd 10 codes to filter: ',icd10_ls[:5])

## Count files in the path to processed:
f_ls = []
for filename in os.listdir(ot_path):
    f = os.path.join(ot_path, filename)
    if os.path.isfile(f):
        f_ls.append(f)

range_max = len(f_ls)+1
print('\n number of files to process: ', len(f_ls))


#pat_ct = 0
hyper_patient = []
## Enter the number of file:
n=1
for n in range (1,range_max):
    filename = 'dx_'+str(n)+'.csv'
    print('', filename)
    if n==1:
        df = pd.read_csv(ot_path+filename,
            dtype={'patid':np.int64,'diag':object,'icd_flag':np.int64, 'fst_dt':object},
            low_memory=False)
        print('working on file: ',df.head(3))
    else:
        df = pd.read_csv(ot_path+filename,
        names = ['patid','fst_dt','diag','icd_flag'],
        dtype={'patid':np.int64,'icd_flag':np.int64,'diag':object, 'fst_dt':object},
        low_memory=False)
        print('working on file: ',df.head(3))
   
    df['hyper_dx']=np.where(((df['diag'].isin(icd9_ls)) & 
            (df['icd_flag']==9)|
            ((df['diag'].isin(icd10_ls))&
            (df['icd_flag']==10))), 
            1, 0)

    #pat_ct += df.patid.nunique()

    hyper_df = df.loc[df['hyper_dx']==1]
    hyper_pid_ls = hyper_df['patid'].unique().tolist()
    hyper_pid = [int(x) for x in hyper_pid_ls]
    hyper_patient_ls = list(hyper_pid)

    hyper_patient.extend(hyper_patient_ls)

    print('\n hyper patient found:\n ', hyper_df,'\n', hyper_df.head(10))
    print('\n found patient list: ', hyper_patient[:3], '\n',hyper_patient[-3:])

    df.to_csv(ot_label_path+filename,sep='\t',index=False)

    print('\n Completed recording from split file: ', n)
    del hyper_df
    del df

hyper_pid = [int(x) for x in hyper_patient]
hyper_set = set(hyper_pid)
hyper_patient_final = list(sorted(hyper_set))

len_hyper = len(hyper_patient_final)

print('\n found patients with hyper diagnosis of one encounter or more: ', len_hyper)

#print('\n total patients: ', pat_ct)

with open(ot_path+'hyper_patient_dx.pickle', 'wb') as handle:
    pickle.dump(hyper_patient_final, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('\n =====end processing files=======')

end_time = datetime.now()
ela_time = end_time - cur_time

print('\n end working at', end_time, '\n elaspe time is: ', ela_time)