#!/usr/bin/env python
""" For a set of data files used in our dashboard,
generate:

1. a summary file called nssac-ncov-sd-summary.csv with below headers:
   (for all countries)
date,totalConfirmed,totalDeaths,totalRecovered,newConfirmed,newDeaths,newRecovered

date  in mm-dd-yyyy format
total stands for cumulative amount as
new   stands for changes in previous day

2. nssac-ncov-sd-region_list.csv
  use latest data file to generate a csv file to populate region drop down menu

3. region_first_case.txt (not finished)
   this will be used for timeline, currently shows some error when running

4. a summary file for each region in nssac-ncov-sd-region_list.csv
   Notes from DX: 
   1. let store files in a new folder called "regions" under current data folder.
   2. the format should be same as nssac-ncov-sd-summary.csv, if using region's name
      as part of file name is hard, you might consider to add an id column in nssac-ncov-sd-summary.csv
      for linking purpose. you can also use "ISO_3" code in file name 
      (regions.csv is checked in as reference)
   3. pay attention to "Mainland China" and we need to aggregate data for all 31 provinces.
 
By Dawen Xie
"""

import sys
import os
import csv
import glob

def main():

    datafolder = sys.argv[1]
    if not os.path.isdir(datafolder):
        print(f"ERROR: Data folder {datafolder} does not exist. Exiting...")
        sys.exit()

    total_by_date_file="summary1.csv"
    print(f"Generate total by date file: {total_by_date_file}")
    file = open(total_by_date_file, "w")
    file.write("date,totalConfirmed,totalDeaths,totalRecovered\n")
    latest_file = ""
    for source_file in sorted(glob.glob(f"{datafolder}/nssac-ncov-sd-??-*.csv")):
        latest_file = source_file
        s=str.split(source_file,".")
        file_name=s[0]
        date_str=file_name[-10:]
        with open(source_file) as csv_file:
            csv_reader= csv.reader(csv_file, delimiter=',')
            line_count, tC, tD, tR= 0,0,0,0
            for row in csv_reader:
                if line_count == 0:
                    line_count +=1
                    continue
                else:
                    tC += int(row[3])
                    tD += int(row[4])
                    #171 - Added code to handle blank recovered count - Start
                    try:
                        valR = int(row[5])
                    except ValueError:
                        # int(row[5]) is something that cannot be converted to
                        # a number. It could be an empty string, or a string like 'hello'
                        # a default value = 0
                        valR = 0
                        #print(f"#171: Found Blank Values For date {date_str} Recovered Value = {valR}")
                    tR += valR
                    #print(f"#171: Current date {date_str} Recovered Value = {valR}")
                    #171 - Added code to handle blank recovered count - End
                    #tR += int(row[5])	#171-Commented earlier implementation.
            file.write(f"{date_str},{tC},{tD},{tR}\n")
    file.close()

    summary_file="nssac-ncov-sd-summary.csv"
    print(f"Generate nssac summary file: {summary_file}")
    file = open(summary_file, "w")
    file.write("date,totalConfirmed,totalDeaths,totalRecovered,newConfirmed,newDeaths,newRecovered\n")
    with open(total_by_date_file) as csv_file:
        csv_reader= csv.reader(csv_file, delimiter=',')
        #pC confirmed number in previous day
        line_count, pC, pD, pR= 0,0,0,0
        for row in csv_reader:
            if line_count == 0:
                line_count +=1
                continue
            elif line_count == 1:
                (pC, pD, pR) = row[1:]
                line_count +=1
                file.write(f"{row[0]},{row[1]},{row[2]},{row[3]},0,0,0\n")
            else:
                line_count +=1
                dC=int(row[1])-int(pC)
                dD=int(row[2])-int(pD)
                dR=int(row[3])-int(pR)
                file.write(f"{row[0]},{row[1]},{row[2]},{row[3]},{dC},{dD},{dR}\n")
                (pC, pD, pR) = row[1:]
    file.close()

    # 3. generate region list (for country dropdown menu) and region_first_case.csv (for timeline)
    # first_case file is NOT finished yet
    print(f"latest file: {latest_file}")
    region_list_file="nssac-ncov-sd-region_list.csv"
    region_first_case_file="region_first_case.txt"
    cmd = f"rm {region_first_case_file}"
    returned_value = os.system(cmd)
    file = open(region_list_file, "w")
    file.write("All regions\n")
    region_list = []
    with open(latest_file) as csv_file:
        csv_reader= csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count +=1
                continue
            else:
                line_count +=1
                region = str.split(row[1],'(')[0].strip()
                if region not in region_list:
                    region_list.append(region)
                    #get country's first date
                    cmd = f"grep {region} {datafolder}/nssac-ncov-sd-??-*.csv | head -n 1 | cut -d'/' -f9 >> {region_first_case_file}"
                    returned_value = os.system(cmd)
    for region in sorted(region_list):
        file.write(f"{region}\n")
    file.close()

    # 4. Generate summary file for every region
    for region in sorted(region_list):
        region_file=region.replace(" ", "_")
        region_data_file_temp="nssac-ncov-sd-summary-" + region_file + "-temp.csv"
        region_data_file="nssac-ncov-sd-summary-" + region_file + ".csv"
        file = open(region_data_file_temp, "w")
        file.write("date,totalConfirmed,totalDeaths,totalRecovered,newConfirmed,newDeaths,newRecovered\n")
        file.close()
        cmd = f"grep -w {region},2020 {datafolder}/nssac-ncov-sd-??-*.csv | cut -d ',' -f3,4,5,6 >> {region_data_file_temp}"
        count = os.system(cmd)

        file = open(region_data_file, "w")
        file.write("date,totalConfirmed,totalDeaths,totalRecovered,newConfirmed,newDeaths,newRecovered\n")

        with open(region_data_file_temp) as csv_file:
            csv_reader=csv.reader(csv_file, delimiter=',')
            line_count, pC, pD, pR= 0,0,0,0
            for row in csv_reader:
                if line_count == 0:
                    line_count +=1
                    continue
                elif line_count == 1:
                    date = str.split(row[0],' ')[0].strip()
                    (pC, pD, pR) = row[1:]
                    line_count +=1
                    file.write(f"{date},{row[1]},{row[2]},{row[3]},0,0,0\n")
                else:
                    date = str.split(row[0],' ')[0].strip()
                    line_count +=1
                    dC=int(row[1])-int(pC)
                    dD=int(row[2])-int(pD)
                                        
                    #171 - Added code to handle blank recovered count - End
                    #print(f"#171: Current date {date} Previous Recovered Row Value = {pR}")
                    #print(f"#171: Current date {date} Current Recovered Row Value = {row[3]}")
                    
                    #171 - Added code to handle blank recovered count - Start
                    try:
                        cRCnt = int(row[3])
                    except ValueError:
                        cRCnt = 0
                        #print(f"#171: Found Blank Values For date {date} Recovered Value = {cRCnt}")
                    
                    dR=cRCnt-int(pR) #Commented to handle blank recovered count.
                    #print(f"#171: Current date {date} current-previous = {dR}")
                    file.write(f"{date},{row[1]},{row[2]},{row[3]},{dC},{dD},{dR}\n")
                    pC = int(row[1])
                    pD = int(row[2])
                    #pR = int(row[3])
                    
                    try:
                        pR = int(row[3])
                    except ValueError:
                        pR = 0
                        #print(f"#171: Found Blank Values For Previous date {date} Recovered Value = {pR}")
                    #(pC, pD, pR) = row[1:]
        file.close() 
        cmd = f"rm {region_data_file_temp}"
        os.system(cmd)
 
    print("all done...")

if __name__ == '__main__':
    main()


