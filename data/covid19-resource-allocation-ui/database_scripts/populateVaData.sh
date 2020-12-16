#! /bin/bash
#
#	This script is used to read scenerios from database to populate data into 'usa_va_mrdd_data' table.
#	
# created : 07/24/2020
#
# by Shirish P. Dumbre

. ./envload.config

SCEN_TABLE_NAME="$SCHEMA_NAME.usa_va_mrdd_scenarios"
DATA_TABLE_NAME="$SCHEMA_NAME.usa_va_mrdd_data"
OUT_FILE="$SCRIPT_DIR/queries_mrdd_va_data.sql"

#echo "OUT_FILE=$OUT_FILE"
touch $OUT_FILE
:> $OUT_FILE

#Read the active scenerios
SCENARIO_DATA=$(psql -h $HOST_NAME -d $DB_NAME -A -t -q -c "(SELECT scenario_id, data_directory FROM $SCEN_TABLE_NAME WHERE end_date IS NULL)")

if [ $? -ne 0 ]
then
        echo "Failed to retrieve dates from $SCEN_TABLE_NAME table."
        exit 1
fi

#\read -r -a SCENARIO_DATA_ARRAY <<< $SCENARIO_DATA
#mapfile -t SCENARIO_DATA_ARRAY <<< $SCENARIO_DATA

SAVEIFS=$IFS
IFS=$'\n'
SCENARIO_DATA_ARRAY=($SCENARIO_DATA)
IFS=$SAVEIFS

for SINGLE_SCENARIO_DATA in "${SCENARIO_DATA_ARRAY[@]}"; do
	
	SCENARIO_ID=`echo $SINGLE_SCENARIO_DATA|cut -d'|' -f1`
	DATA_DIR=$BASE_DIR_PATH/`echo $SINGLE_SCENARIO_DATA|cut -d'|' -f2`
	
	./gen_mrdd_va_data_queries.py $SCENARIO_ID $DATA_TABLE_NAME $DATA_DIR $OUT_FILE
	
	# run sql script generated in above step to populate 'usa_va_mrdd_data' table.
	#echo "Inserting data into database for scenario_id=$SCENARIO_ID..."
	#psql -h $HOST_NAME -d $DB_NAME -q -f queries_mrdd_va_data.sql

done

#out_file.write(f"SELECT COUNT(*) AS DATA_RECORDS_INSERTED FROM {data_table};")
#echo "SELECT COUNT(*) AS DATA_RECORDS_INSERTED FROM $DATA_TABLE_NAME;" >> $OUT_FILE

#out_file.write(f"\\q \n")
echo "\\q \n" >> $OUT_FILE