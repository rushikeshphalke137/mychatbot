#! /bin/bash
#
#	This is the master script used to load MRDD data files into database
#	Following are the steps:
#    1. create database schema.
#    2. load region - hrr data into usa_mrdd_hrr table.
#	 3. load scenarios from supported_scenarios.json file.
#	 4. load data for corresponding scenarios. 
#
# created : 09/17/2020
#
# by Komal K. Dudakiya

echo -e "\n-- Started At "`date`

. ./envload.config	#Execute the config file to set environment variables.

##########################################
##
## PART I: Data Injection to DB
##
##########################################

# generate all tables
echo -e "\nCreating Database Tables..."
psql -h $HOST_NAME -d $DB_NAME -q -f create_mrdd_usa_tables.sql -v current_schema=$SCHEMA_NAME 2> $LOG_FILE

#Processing for regions (HRR) data.
# process data file (HRR_Data.csv) and generate 'queries_mrdd_usa_hrr.sql' file to insert data into DB.
echo -e "\nProcessing regions (hrr) data file..."
$SCRIPT_DIR/gen_mrdd_usa_hrr_queries.py
echo "queries_mrdd_usa_hrr.sql has been generated."

# run sql script generated in above step to populate 'usa_mrdd_hrr' table.
echo "Inserting region data (HRR) into database..."
psql -h $HOST_NAME -d $DB_NAME -q -f queries_mrdd_usa_hrr.sql -v current_schema=$SCHEMA_NAME 2>> $LOG_FILE

#Processing for scenario data.
# process data files (supported_scenarios.json) and generate 'queries_mrdd_usa_scenarios.sql' file to insert data into DB.
echo -e "\nProcessing scenario data file & inserting data into database..."
$SCRIPT_DIR/gen_mrdd_usa_scenarios_queries.py
#echo "queries_mrdd_usa_scenarios.sql has been generated."

# run sql script generated in above step to populate 'usa_va_mrdd_scenarios' table.
#echo "Inserting scenarios data into database..."
#psql -h $HOST_NAME -d $DB_NAME -q -f queries_mrdd_va_scenarios.sql -v current_schema=$SCHEMA_NAME 2>> $LOG_FILE

#Processing for data.
# process data files and generate 'queries_mrdd_usa_data.sql' file to insert data into DB.
echo -e "\nProcessing data files..."
$SCRIPT_DIR/populateUsData.sh
echo "queries_mrdd_usa_data.sql has been generated."

# run sql script generated in above step to populate 'usa_va_mrdd_data' table.
echo "Inserting data into database..."
psql -h $HOST_NAME -d $DB_NAME -q -f queries_mrdd_usa_data.sql -v current_schema=$SCHEMA_NAME 2>> $LOG_FILE

echo -e "\n-- Finished At "`date`
