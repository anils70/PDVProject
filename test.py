""" Test program """
#print("Hello Sets")

#set_1 = {1,3,2,1,5,7,6}
#print(set_1)
#set_2={}
#print("sest1:",type(set_1), type(set_2))

#for item in set_1:
#    print(item)

#set_3 = set(range(5))
#print("set3:",set_3, type(set_3))

"""
Some sample code illustrating the speed of the "in" operator for lists vs. dictionaries in Python
See https://wiki.python.org/moin/TimeComplexity for more details
"""

import time
import random
import csv

def read_csv_file(file_name):
    """
    Given a CSV file, read the data into a nested list
    Input: String corresponding to comma-separated  CSV file
    Output: Nested list consisting of the fields in the CSV file
    """

    with open(file_name, newline='') as csv_file:       # don't need to explicitly close the file no
        csv_table = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_table.append(row)
    return csv_table

CANCER_RISK_FIPS_COL = 2
CENTER_FIPS_COL = 0

def test_CSV_join_efficiency(cancer_csv_file, center_csv_file):
    """
    Extract lists of FIPS codes from cancer-risk data set and county center data set
    Measure running time to determine whether FIPS codes in cancer-risk set are in county center set
    """
    # Read in both CSV files
    risk_table = read_csv_file(cancer_csv_file)
    risk_FIPS_list = [risk_table[idx][CANCER_RISK_FIPS_COL] for idx in range(len(risk_table))]
    print("Read", len(risk_FIPS_list), "cancer-risk FIPS codes")

    center_table = read_csv_file(center_csv_file)
    center_FIPS_list = [center_table[idx][CENTER_FIPS_COL] for idx in range(len(center_table))]
    print("Read", len(center_FIPS_list), "county center FIPS codes")

    start_time = time.time()
    for code in risk_FIPS_list:
        if code in center_FIPS_list:
            pass
    end_time = time.time()
    print("Checked for FIPS membership using list in", end_time-start_time, "seconds")


    center_FIPS_dict = {code : True for code in center_FIPS_list}
    start_time = time.time()
    for code in risk_FIPS_list:

        if code in center_FIPS_dict:
            pass
    end_time = time.time()
    print("Checked for FIPS membership using dict in", end_time-start_time, "seconds")
    
test_CSV_join_efficiency("cancer_risk_trimmed_solution.csv", "USA_Counties_with_FIPS_and_centers.csv")

# Code that test the efficiency of "in" operator on larger examples
