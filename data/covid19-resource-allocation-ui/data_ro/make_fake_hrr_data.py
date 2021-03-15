import sys
import random
from datetime import datetime, timedelta, date

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def getdatesarray(start_date, end_date):
    date_array = []
    curr_date = start_date
    while curr_date <= end_date:
        curr_date = curr_date + timedelta(7)
        date_array.append(curr_date)
    return date_array

_, fake_hrr_file, start, end, root_dir=sys.argv

# Read the fake HHR list into a list of dicts
hrr_list=[]

fin=open(fake_hrr_file, 'r')
hrrnum=0
hrrcity=""
hrr_beds=0
total_pop=0
objectid=0
count=0

print("Reading HRR File")

totalBedsCount = 0

for line in fin:
    count += 1
    modulo = count % 5
    if modulo == 0:  
        object_id = int(line.strip())
        totalBedsCount += hrr_beds
        hrr_dict = {"hrrnum": hrrnum, "hrrcity": hrrcity.upper(), "hrr_beds": hrr_beds, "total_pop": total_pop, "objectid": objectid, "bedsNeeded": 0, "projDemand": 0}
        hrr_list.append(hrr_dict)
        hrrnum=0
        hrrcity=""
        hrr_beds=0
        total_pop=0
        objectid=0
    elif modulo == 1:
        hrrnum = int(line.strip())
    elif modulo == 2:
        hrrcity = line.strip()
    elif modulo == 3:
        hrr_beds = int(line.strip())
    elif modulo == 4:
        total_pop = int(line.strip())

fin.close()
print("Closed fin file")

# Open nssac_ncov_ro_summary.csv
full_summary_file = open(root_dir + "/nssac_ncov_ro-summary.csv", "w")
# full_summary_file.write("date,Total Beds Avail,Total Vent. Avail,Total Staff Avail,Total Hospitalized,Total Vents Demanded,Total Staff Demanded,Total Beds Count,Total Vent. Count,Total Staff Count,Total Cases\n")
full_summary_file.write("date,Total Projected Demand (%),Total Hospitalizations,Lower Hospitalization Bound,Upper Hospitalization Bound\n")

print("Creating and initializing HHR files")
# Loop through the HRRs and create their region_summary files
region_file=open(root_dir + "/nssac_ncov_ro_region_list.csv", "w")
region_file.write("All Regions\n")

for hrr in hrr_list:
    region_file.write(f"{hrr['hrrcity']}\n")
    hrr_file = open(root_dir + "/regions/nssac_ncov_ro_summary_hrr_" + str(hrr["hrrnum"]) + ".csv", "w")
    # hrr_file.write("date,Total Beds Avail,Total Vent. Avail,Total Staff Avail,Total Hospitalized,Total Vent. Demanded,Total Staff Demanded,Total Beds Count,Total Vent. Count,Total Staff Count,Total Cases\n")
    hrr_file.write("date,Total Projected Demand (%),Total Hospitalizations,Lower Hospitalization Bound,Upper Hospitalization Bound\n")
    hrr_file.close()
region_file.close()

# Loop through the dates and hrr_list to generate files for each hrr, then 
start_date = datetime.strptime(start,"%m-%d-%Y")
end_date = datetime.strptime(end, "%m-%d-%Y")
seed = 4
print("Looping through dates")
dates_array = getdatesarray(start_date, end_date)

totalBedsNeeded = 0
dateFileOpen = False

for single_date in daterange(start_date, end_date):
    # for writing files

    if (single_date in dates_array):
        # for writing files
        temp_date = single_date.strftime("%m-%d-%Y")
        dateFile = open(root_dir + "/nssac_ncov_ro_" + temp_date + ".csv", "w")
        dateFile.write("HRRNum,Hospital Referral Region,Projected Demand (%),Hospitalizations,Lower Hospitalization Bound,Upper Hospitalization Bound,Last Update\n")

    for hrr in hrr_list:
        hrr_beds = seed*random.randint(5,12)
        hrr["bedsNeeded"] += hrr_beds
        totalBedsNeeded += hrr_beds
        temp_hrr_proj_need = int(((0.8 * hrr["hrr_beds"]) + hrr_beds)*100/hrr["hrr_beds"])
        hrr["projDemand"] = max(hrr["projDemand"], temp_hrr_proj_need)
        if (single_date in dates_array):
            lower_bound = int(hrr["bedsNeeded"] - hrr["bedsNeeded"]*0.05)
            upper_bound = int(hrr["bedsNeeded"] + hrr["bedsNeeded"]*0.05)
        
            dateFile.write(f"{str(hrr['hrrnum'])},{hrr['hrrcity']},{str(hrr['projDemand'])},{str(hrr['bedsNeeded'])},{str(lower_bound)},{str(upper_bound)},{temp_date}\n")
            
            hrr_file = open(root_dir + "/regions/nssac_ncov_ro_summary_hrr_" + str(hrr["hrrnum"]) + ".csv", "a")
            hrr_file.write(f"{temp_date},{hrr['projDemand']},{str(hrr['bedsNeeded'])},{str(lower_bound)},{str(upper_bound)}\n")
            hrr_file.close()

            hrr["bedsNeeded"] = 0
            hrr["projDemand"] = 0

    if single_date in dates_array:
        dateFile.close()    
        total_proj_need = int(((0.8 * totalBedsCount) + totalBedsNeeded)*100/totalBedsCount)
        lower_bound = int(totalBedsNeeded - totalBedsNeeded*0.05)
        upper_bound = int(totalBedsNeeded + totalBedsNeeded*0.05)
        full_summary_file.write(f"{temp_date},{total_proj_need},{totalBedsNeeded},{lower_bound},{upper_bound}\n")
        seed = seed + 2
        totalBedsNeeded = 0
full_summary_file.close()
print("finished")
