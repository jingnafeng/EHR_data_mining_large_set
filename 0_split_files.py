import pandas as pd
import csv
import sys
import pickle
from datetime import datetime
import numpy as np
import path
# import func_jfeng as jf

in_path = path.in_path
ot_path = path.out_path


## Input file name of the file to chunk
filename = '_hypertension_lab.csv'
## Diag file
# 100000000 lines for original file 3676732750 lines
# 10000 lines for sample of 30001

# rx file
# 1574599252
# 100000000

# medical file
# 2838417705
# 100000000

# medication file
# 271221455
# 10000000

# lab file
# 1719636124
# 100000000
cur_time = datetime.now()

csvfile = open(in_path+filename, 'r').readlines()
fcnt = 1
len_csvfile = 1719636124  ##change with the len of the file return from wc command
line_per_file = 100000000  ## change with the size of each file
file_ct = len_csvfile/line_per_file
print('file len: ', len_csvfile)
print('number of file to generate: ', file_ct)

## make a directory to store the splitted file

for i in range (len_csvfile):
    if i %  line_per_file == 0:
        open(ot_path+'lab_split/lab_'+str(fcnt)+'.csv', 'w+').writelines(csvfile[i:i+line_per_file])
        print('\n finished file number: ', fcnt)
        fcnt +=1
        sys.stdout.flush()

print('\n work completed')
print('\n number of files generated ', fcnt-1)

print('\n =====end processing files=======')
end_time = datetime.now()
ela_time = end_time - cur_time

print('\n end working at', end_time, '\n elaspe time is: ', ela_time)
