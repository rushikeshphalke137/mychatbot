#! /bin/bash
#
#	This is the master script used to load MRDD data files into database
#	Following are the steps:
#    1. create database schema.
#    2. load region - vhass data into usa_va_mrdd_vhass table.
#	 3. load scenarios from supported_scenarios.json file.
#	 4. load data for corresponding scenarios. 
#
# created : 07/20/2020
#
# by Shirish P. Dumbre

echo -e "\n-- Started At "`date`

. ./envload.config	#Execute the config file to set environment variables.

##########################################
##
## PART I: Data Injection to DB
##
##########################################

# generate all tables
echo -e "\nCreating Database Tables..."
psql -h $HOST_NAME -d $DB_NAME -q -f create_mrdd_va_tables.sql -v current_schema=$SCHEMA_NAME 2> $LOG_FILE

#Processing for regions (VHASS) data.
# process data file (VHASS_Region_Counts.csv) and generate 'queries_mrdd_va_vhass.sql' file to insert data into DB.
echo -e "\nProcessing regions (vhass) data file..."
$SCRIPT_DIR/gen_mrdd_va_vhass_queries.py
echo "queries_mrdd_va_vhass.sql has been generated."

# run sql script generated in above step to populate 'usa_va_mrdd_vhass' table.
echo "Inserting region data (VHASS) into database..."
psql -h $HOST_NAME -d $DB_NAME -q -f queries_mrdd_va_vhass.sql -v current_schema=$SCHEMA_NAME 2>> $LOG_FILE

#Processing for scenario data.
# process data files (supported_scenarios.json) and generate 'queries_mrdd_va_scenarios.sql' file to insert data into DB.
echo -e "\nProcessing scenario data file & inserting data into database..."
$SCRIPT_DIR/gen_mrdd_va_scenarios_queries.py
#echo "queries_mrdd_va_scenarios.sql has been generated."

# run sql script generated in above step to populate 'usa_va_mrdd_scenarios' table.
#echo "Inserting scenarios data into database..."
#psql -h $HOST_NAME -d $DB_NAME -q -f queries_mrdd_va_scenarios.sql -v current_schema=$SCHEMA_NAME 2>> $LOG_FILE

#Processing for data.
# process data files and generate 'queries_mrdd_va_data.sql' file to insert data into DB.
echo -e "\nProcessing data files..."
$SCRIPT_DIR/populateVaData.sh
echo "queries_mrdd_va_data.sql has been generated."

# run sql script generated in above step to populate 'usa_va_mrdd_data' table.
echo "Inserting data into database..."
psql -h $HOST_NAME -d $DB_NAME -q -f queries_mrdd_va_data.sql -v current_schema=$SCHEMA_NAME 2>> $LOG_FILE

echo -e "\n-- Finished At "`date`
