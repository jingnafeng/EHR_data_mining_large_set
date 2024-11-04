in_path = '/Hypertension/Optum/' ## input path
out_path = '/Hypertension/Optum/processed/' ## output path


# wc: count of line from terminal 
# 3,676,732,750  hypertension_diag.csv  
# 1,574,599,252  hypertension_rx.csv
# 271,221,455  hypertension_medication.csv

# splited diag files:
# adrd, not sorted by fst_dt
# non-adrd, not sorted by fst_dt

"""
(base) [jfeng@ hyper_output]$ ls -lh /data/user_data/ hypertension/
total 408G
-rwxr-xr-x 1     1.3G May 24 14:41  hypertension_confinement.csv 
-rwxr-xr-x 1     121G May 24 15:26  hypertension_diag.csv
-rwxr-xr-x 1     105G May 24 16:03  hypertension_lab.csv 
-rwxr-xr-x 1     708M May 24 16:04  hypertension_mbr_co_enroll.csv 
-rwxr-xr-x 1     417M May 24 16:04  hypertension_mbr_enroll.csv
-rwxr-xr-x 1      92G May 24 16:38  hypertension_medical.csv 
-rwxr-xr-x 1     8.6G May 24 16:42  hypertension_medication.csv 
-rwxr-xr-x 1     753M May 24 16:42  hypertension_procedure.csv 
-rwxr-xr-x 1      81G May 24 17:11  hypertension_rx.csv 
"""

adrd_code_10 = ['F01.50', 'F01.51', 'F02.80', 'F02.81', 'F03.90', 'F03.91', 'F04', 'F05', 'F06.1', 'F06.8', 
    'G13.8', 'G30.0', 'G30.1', 'G30.8', 'G30.9', 'G31.01', 'G31.09', 'G31.1', 'G31.2', 'G94', 'R41.81', 'R54']

adrd_code_9 = ['331.0', '331.11', '331.19', '331.2', '331.7', '290.0', '290.10', '290.11', '290.12', 
    '290.13', '290.20', '290.21', '290.3', '290.40', '290.41', '290.42', '290.43', 
    '294.0', '294.10', '294.11', '294.20', '294.21', '294.8', '797']