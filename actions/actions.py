# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import SlotSet
import pandas as pd
import os
import math
import json
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)

root_dir= "/app/data/covid19-resource-allocation-ui/data_va_actuals/"
beds_data_path="/app/data/covid19-resource-allocation-ui/data_va_actuals/"

log_file_location="/app/logs/"

    
class ActionHospitalizedCurrentWeek(Action):

    def name(self) -> Text:
        return "action_hospitalized_current_week"

    def run(self, dispatcher, tracker, domain):
        
        json_path=root_dir+"/supported_scenarios.json"

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Get current weeks saturday's date
        now = datetime.now()
        sat_date = now - timedelta(days = now.weekday()-5)
        sat_date=sat_date.strftime('%m-%d-%Y')

        # Filename for the current week
        csv_f_name="nssac_ncov_ro_"+str(sat_date)+".csv"

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
        dd=data['configuration']['defaultDuration']

        # Get total of scenarion for each file
        hos_df=pd.DataFrame()
        for f in dirlist:
            temp_df=pd.read_csv(root_dir+"/"+f+'/duration'+str(dd)+"/"+csv_f_name)
            tot_hos_val=temp_df['Hospitalizations (Median)'].sum()
            temp_ret_df=pd.concat([pd.DataFrame({"File_Name":[f]}),pd.DataFrame({"Total Count":[tot_hos_val]})],axis=1)
            hos_df=hos_df.append(temp_ret_df)
            #print(f+"-"+str(tot_hos_val))
            
        hos_df=hos_df.reset_index(drop=True)
        
        # Read Scenario.json to update the filename
        with open(json_path) as f:
            data = json.load(f)
        
        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Rename Filename
        hos_df=pd.merge(hos_df,scenario_map, on='File_Name', how='inner')
        hos_df=hos_df[['Scenario','Total Count']]
        
        #hos_df.to_html()
        json_dict=json.loads(hos_df.to_json(orient='split'))
        del json_dict['index']
        json_dict['isTable']=True
        json_dict=json.dumps(json_dict)
        dispatcher.utter_message(text="Below are the details about total number of people (for each scenario across ), projected to be hospitalized in the current week:")
        dispatcher.utter_message(json_message=json_dict)
        
        logger.debug("User Id-"+str(tracker.sender_id))
        logger.debug("Latest Messages-"+str(tracker.latest_message))
        logger.debug("Events-"+str(tracker.events))
        logger.debug("Latest Action Name-"+str(tracker.latest_action_name))
        logger.debug("Slots-"+str(tracker.slots))
        logger.debug("Events After Restart -"+"%s\n" % place for place in tracker.events_after_latest_restart())
        
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)

        return [AllSlotsReset()]

class ActionMaxProjectedHospitalizationCurrentWeek(Action):

    def name(self) -> Text:
        return "action_max_projected_hospitalization_current_week"

    def run(self, dispatcher, tracker, domain):
        
        json_path=root_dir+"/supported_scenarios.json"

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Get current weeks saturday's date
        now = datetime.now()
        sat_date = now - timedelta(days = now.weekday()-5)
        sat_date=sat_date.strftime('%m-%d-%Y')
            
        # Filename for the current week
        csv_f_name="nssac_ncov_ro_"+str(sat_date)+".csv"

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
        dd=data['configuration']['defaultDuration']


        # Get total of scenarion for each file
        max_df=pd.DataFrame()
        for f in dirlist:
            temp_df=pd.read_csv(root_dir+"/"+f+'/duration'+str(dd)+"/"+csv_f_name)
            max_val=temp_df['Hospitalizations (Median)'].max()
            temp_ret_df=pd.concat([pd.DataFrame({"File_Name":[f]}),pd.DataFrame({"Max Count":[max_val]})],axis=1)
            max_df=max_df.append(temp_ret_df)
            #print(f+"-"+str(tot_hos_val))
            
        max_df=max_df.reset_index(drop=True)

        # Read Scenario.json to update the filename
        with open(json_path) as f:
            data = json.load(f)

        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Rename Filename
        max_df=pd.merge(max_df,scenario_map, on='File_Name', how='inner')
        max_df=max_df[['Scenario','Max Count']]

        max_df=max_df[max_df["Max Count"]==max_df["Max Count"].max()]
        
        # Convert to Dictionary
        json_dict=json.loads(max_df.to_json(orient='split'))
        del json_dict['index']
        json_dict['isTable']=True
        json_dict=json.dumps(json_dict)
        dispatcher.utter_message(text="The scenario with the maximum number of hospitalizations in the current week is: ")
        dispatcher.utter_message(json_message=json_dict)
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
        return [AllSlotsReset()] 

class ActionHighestProjectedHospitalization(Action):

    def name(self) -> Text:
        return "action_highest_projected_hospitalization"
        

    def run(self, dispatcher, tracker, domain):
        json_path=root_dir+"/supported_scenarios.json"

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
        dd=data['configuration']['defaultDuration']


        # Get Max for each scenario and create a summary file
        sum_df_max=pd.DataFrame()
        for f in dirlist:
            temp_df=pd.read_csv(root_dir+"/"+f+'/duration'+str(dd)+"/"+"nssac_ncov_ro-summary.csv")
            temp_df=temp_df[:-1]
            temp_df=temp_df[temp_df['Total Hospitalizations (Median)']==temp_df['Total Hospitalizations (Median)'].max()]
            temp_df=temp_df.reset_index(drop=True)
            temp_df=pd.concat([pd.DataFrame(temp_df),pd.DataFrame({"File_Name":[f]})], axis=1)
            sum_df_max=sum_df_max.append(temp_df)
            #print(f+"-"+str(tot_hos_val))

        # Now get the max of the newly created summary file
        sum_df_max=sum_df_max[sum_df_max['Total Hospitalizations (Median)']==sum_df_max['Total Hospitalizations (Median)'].max()]
            
        # Keep only the required columns
        sum_df_max=sum_df_max[["date","File_Name","Total Hospitalizations (Median)"]]

        # update the filename

        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Rename Filename
        sum_df_max=pd.merge(sum_df_max,scenario_map, on='File_Name', how='inner')
        sum_df_max=sum_df_max[["date","Scenario","Total Hospitalizations (Median)"]]

        dispatcher.utter_message("{} has a maximum value of {} in the week ending {}.".format(str(sum_df_max['Scenario'][0]),str(sum_df_max['Total Hospitalizations (Median)'][0]),str(sum_df_max['date'][0])))
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
        return [AllSlotsReset()]

class ActionHospitalizationPeak(Action):

    def name(self) -> Text:
        return "action_hospitalization_peak"
        

    def run(self, dispatcher, tracker, domain):
        scenario = tracker.get_slot("scenario")
        
        json_path=root_dir+"/supported_scenarios.json"

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
        dd=data['configuration']['defaultDuration']

        # Create Scenario Map

        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Get Folder Name as per selected file scenario
        s_file_name=scenario_map.loc[scenario_map['Scenario']==scenario]['File_Name'][0]

        # Read Data as per the selected scenario, default duration and for the current week
        read_df_path=root_dir+"/"+s_file_name+'/duration'+str(dd)+"/"+"nssac_ncov_ro-summary.csv"
        df=pd.read_csv(read_df_path)

        # Get max value of hospitalization
        df=df[df["Total Hospitalizations (Median)"]==df["Total Hospitalizations (Median)"].max()]
        df=df[["date","Total Hospitalizations (Median)"]]
        df=df.reset_index(drop=True)

        dispatcher.utter_message("Based on the selected scenario({}), Hospitalization will peak during Week ending on {} and its predicted value is {}.".format(str(scenario),str(df['date'][0]),str(df['Total Hospitalizations (Median)'][0])))
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
        return [AllSlotsReset()]

class ActionTop5RegionsHospitalization(Action):

    def name(self) -> Text:
        return "action_top_5_regions_hospitalization"
        

    def run(self, dispatcher, tracker, domain):
        cardinal = tracker.get_slot("CARDINAL")
        scenario = tracker.get_slot("scenario")
        hospitalization_days=tracker.get_slot("hospitalization_days")
        week_ending_date= tracker.get_slot("week_ending_date")
        
        if (cardinal==None):
            cardinal=5
            
        json_path=root_dir+"/supported_scenarios.json"

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
        if(hospitalization_days==None):    
            dd=data['configuration']['defaultDuration']
        else:
            dd=hospitalization_days

        # Create Scenario Map

        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Get Folder Name as per selected file scenario
        s_file_name=scenario_map.loc[scenario_map['Scenario']==scenario]['File_Name'][0]

        # Get current weeks saturday's date
        if( week_ending_date==None):
            now = datetime.now()
            sat_date = now - timedelta(days = now.weekday()-5)
            sat_date=sat_date.strftime('%m-%d-%Y')
        else:
            sat_date=week_ending_date
            
        # Filename for the current week
        csv_f_name="nssac_ncov_ro_"+str(sat_date)+".csv"

        # Read Data as per the selected scenario, default duration and for the current week
        read_df_path=root_dir+"/"+s_file_name+'/duration'+str(dd)+"/"+csv_f_name
        df=pd.read_csv(read_df_path)

        # Sort Dataframe
        df=df.sort_values(by=["Hospitalizations (Median)"],ascending=False)
        df=df.reset_index(drop=True)

        # Get only required columns
        df=df[['region_name','Hospitalizations (Median)']]
        df=df.rename(columns={"region_name": "Region", "Hospitalizations (Median)": "Hospitalizations"})

        # Check if cardinal value is more than the number of records
        if(float(cardinal)>len(df)):
            limit=len(df)
            dispatcher.utter_message("You queried for more regions than available, showing result for all the regions in decending order for Hospitalizations.")
            df=df.loc[:limit]
            # Convert to Dictionary
            json_dict=json.loads(df.to_json(orient='split'))
            del json_dict['index']
            json_dict['isTable']=True
            json_dict=json.dumps(json_dict)
            dispatcher.utter_message(json_message=json_dict)
            dispatcher.utter_message(text="The above result is for Week ending on {}, Do you want to check for any other week?".format(sat_date), buttons=[{'title': 'Yes', 'payload': '/yes'}, {'title': 'No', 'payload': '/no'}])
        else:
            df=df.loc[:math.ceil(float(cardinal))-1]
            # Convert to Dictionary
            json_dict=json.loads(df.to_json(orient='split'))
            del json_dict['index']
            json_dict['isTable']=True
            json_dict=json.dumps(json_dict)
            dispatcher.utter_message(json_message=json_dict)
            dispatcher.utter_message(text="The above result is for Week ending on {}, Do you want to check for any other week?".format(sat_date), buttons=[{'title': 'Yes', 'payload': '/yes'}, {'title': 'No', 'payload': '/no'}])
            
            with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
                filehandle.writelines("%s\n" % place for place in tracker.events)
            
        return [SlotSet("week_ending_date", None)]

class ActionExpectedHospitalizationInRegion(Action):

    def name(self) -> Text:
        return "action_expected_hospitalization_in_region"
        

    def run(self, dispatcher, tracker, domain):
        region=tracker.get_slot("region")
        scenario = tracker.get_slot("scenario")
        week_ending_date= tracker.get_slot("week_ending_date")

        json_path=root_dir+"/supported_scenarios.json"

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
        dd=data['configuration']['defaultDuration']

        # Create Scenario Map
        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Get Folder Name as per selected file scenario
        s_file_name=scenario_map.loc[scenario_map['Scenario']==scenario]['File_Name'][0]

        # Get current weeks saturday's date
        if( week_ending_date==None):
            now = datetime.now()
            sat_date = now - timedelta(days = now.weekday()-5)
            sat_date=sat_date.strftime('%m-%d-%Y')
        else:
            sat_date=week_ending_date
            
        # Filename for the current week
        csv_f_name="nssac_ncov_ro_"+str(sat_date)+".csv"

        # Read Data as per the selected scenario, default duration and for the current week
        read_df_path=root_dir+"/"+s_file_name+'/duration'+str(dd)+"/"+csv_f_name
        df=pd.read_csv(read_df_path)

        df=df[df['region_name']==region]

        # Get only required columns
        df=df[['region_name','Hospitalizations (Median)']]
        df=df.rename(columns={"region_name": "Region", "Hospitalizations (Median)": "Hospitalizations"})
        # Convert to Dictionary
        json_dict=json.loads(df.to_json(orient='split'))
        del json_dict['index']
        json_dict['isTable']=True
        json_dict=json.dumps(json_dict)
        dispatcher.utter_message(json_message=json_dict)
        dispatcher.utter_message(text="The above result is for Week ending on {}, Do you want to check for any other week?".format(sat_date), buttons=[{'title': 'Yes', 'payload': '/yes'}, {'title': 'No', 'payload': '/no'}])
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
        return [SlotSet("week_ending_date", None)]

class ActionProjectedPercentageOccupiedBedsHC(Action):

    def name(self) -> Text:
        return "action_projected_percentage_occupied_beds_hc"
        

    def run(self, dispatcher, tracker, domain):
        scenario = tracker.get_slot("scenario")
        week_ending_date= tracker.get_slot("week_ending_date")
        cardinal= tracker.get_slot("CARDINAL")
        hospitalization_days=tracker.get_slot("hospitalization_days")

        bed_data=pd.read_csv(beds_data_path+"VHASS_Region_Counts.csv")

        json_path=root_dir+"/supported_scenarios.json"

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
            
        # Check if hospitlization days are provided
        if(hospitalization_days!=None):
            dd=hospitalization_days
        else:
            dd=data['configuration']['defaultDuration']

        # Create Scenario Map
        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Get Folder Name as per selected file scenario
        s_file_name=scenario_map.loc[scenario_map['Scenario']==scenario]['File_Name'][0]


        # Get current weeks saturday's date
        if( week_ending_date==None):
            now = datetime.now()
            sat_date = now - timedelta(days = now.weekday()-5)
            sat_date=sat_date.strftime('%m-%d-%Y')
        else:
            sat_date=week_ending_date


        # Read Data as per the selected scenario, default duration and for the current week
        read_df_path=root_dir+"/"+s_file_name+'/duration'+str(dd)+"/"+"nssac_ncov_ro_"+sat_date+".csv"
        df=pd.read_csv(read_df_path)


        # Calculate percentage of occupied beds (covid+non covid)
        out_df=pd.concat([bed_data['#VHASS_Region'],pd.DataFrame(round((df['Max Occupied Beds']/bed_data['Beds'])*100,2)+float(cardinal))],axis=1)

        # Rename Columns
        out_df=out_df.rename(columns={"#VHASS_Region": "Region", 0: "% of Occupied Bed"})
        # Convert to Dictionary
        json_dict=json.loads(out_df.to_json(orient='split'))
        del json_dict['index']
        json_dict['isTable']=True
        json_dict=json.dumps(json_dict)
        dispatcher.utter_message("The projected percentage of occupied beds based on hospital capacity is displayed below:")                              
        dispatcher.utter_message(json_message=json_dict)
        #dispatcher.utter_message(df.to_html(index=False, justify="justify-all"))
        dispatcher.utter_message(text="The above result is for Week ending on {}, and default duration of {} days, Do you want to check for any other duration or week?".format(sat_date,dd), buttons=[{'title': 'Yes', 'payload': '/yes'}, {'title': 'No', 'payload': '/no'}])
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
        return []

class ActionProjectedGreaterOccupiedBeds(Action):

    def name(self) -> Text:
        return "action_projected_greater_occupied_beds"
        

    def run(self, dispatcher, tracker, domain):
        region=tracker.get_slot("region")
        scenario = tracker.get_slot("scenario")
        week_ending_date= tracker.get_slot("week_ending_date")
        cardinal= tracker.get_slot("CARDINAL")
        hospitalization_days= tracker.get_slot("hospitalization_days")

        json_path=root_dir+"/supported_scenarios.json"
        
        if(cardinal==None):
            dispatcher.utter_message(text="Please enter a valid percentage.")
            dispatcher.utter_template("utter_projected_greater_occupied_beds",tracker)
        else:
      
            # Get list of scenarios. These are the list of folders in root directory
            dirlist = [item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item))]

            # Read Scenario.json to get the default duration
            with open(json_path) as f:
                data = json.load(f)
            # Check if hospitlization days are provided
            if(hospitalization_days!=None):
                dd=int(hospitalization_days)
            else:
                dd=data['configuration']['defaultDuration']

            # Create Scenario Map
            scenario_map=pd.DataFrame()
            for i in range(len(data['scenarios'])):
                f_name=data['scenarios'][i]['directory']
                f_name=f_name.replace("data_va_durations/","")
                
                s_name=data['scenarios'][i]['scenario_display_name_line1']
                
                temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
                scenario_map=scenario_map.append(temp_df)
                
            # Get Folder Name as per selected file scenario
            s_file_name=scenario_map.loc[scenario_map['Scenario']==scenario]['File_Name'][0]

            # Get current weeks saturday's date
            if( week_ending_date==None):
                now = datetime.now()
                sat_date = now - timedelta(days = now.weekday()-5)
                sat_date=sat_date.strftime('%m-%d-%Y')
            else:
                sat_date=week_ending_date
            
            
            # Filename for the current week
            csv_f_name="nssac_ncov_ro_"+str(sat_date)+".csv"
            
            # Read Data as per the selected scenario, default duration and for the current week
            read_df_path=root_dir+"/"+s_file_name+'/duration'+str(dd)+"/"+csv_f_name
            df=pd.read_csv(read_df_path)
            
            df=df.loc[df['Projected Demand (%)']>=float(cardinal)]
            df=df[["region_name",'Projected Demand (%)']]
            df=pd.DataFrame(df.rename(columns={"region_name":"Region","Projected Demand (%)":'% of Occupied Beds'}))
            
            if (len(df)<1):
                dispatcher.utter_message(text="No Records Found..!!")
                dispatcher.utter_message(text="The above result is for the current Week (ending on {}) and default hospitalization duration of {} days, Do you want to check for any other duration?".format(sat_date,dd), buttons=[{'title': 'Yes', 'payload': '/yes'}, {'title': 'No', 'payload': '/no'}])
            else:
                # Convert to Dictionary
                json_dict=json.loads(df.to_json(orient='split'))
                del json_dict['index']
                json_dict['isTable']=True
                json_dict=json.dumps(json_dict)
                "Below regions are projected to have greater than {} % of occupied beds:".format(str(cardinal))
                dispatcher.utter_message("Below regions are projected to have greater than {} % of occupied beds:".format(str(cardinal)))                              
                dispatcher.utter_message(json_message=json_dict)
                dispatcher.utter_message(text="The above result is for the current Week (ending on {}) and default hospitalization duration of {} days, Do you want to check for any other duration?".format(sat_date,dd), buttons=[{'title': 'Yes', 'payload': '/yes'}, {'title': 'No', 'payload': '/no'}])
                with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
                    filehandle.writelines("%s\n" % place for place in tracker.events)
        return [SlotSet("hospitalization_days", None)]

class ActionHighestProjectedOccupiedBeds(Action):

    def name(self) -> Text:
        return "action_highest_projected_occupied_beds"
        

    def run(self, dispatcher, tracker, domain):
        region=tracker.get_slot("region")
        scenario = tracker.get_slot("scenario")
        week_ending_date= tracker.get_slot("week_ending_date")
        hospitalization_days= tracker.get_slot("hospitalization_days")

        json_path=root_dir+"/supported_scenarios.json"

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
            
        # Check if hospitlization days are provided
        if(hospitalization_days!=None):
            dd=hospitalization_days
        else:
            dd=data['configuration']['defaultDuration']

        # Create Scenario Map
        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Get Folder Name as per selected file scenario
        s_file_name=scenario_map.loc[scenario_map['Scenario']==scenario]['File_Name'][0]

        # Get current weeks saturday's date
        if( week_ending_date==None):
            now = datetime.now()
            sat_date = now - timedelta(days = now.weekday()-5)
            sat_date=sat_date.strftime('%m-%d-%Y')
        else:
            sat_date=week_ending_date
            

        # Filename for the current week
        csv_f_name="nssac_ncov_ro_"+str(sat_date)+".csv"

        # Read Data as per the selected scenario, default duration and for the current week
        read_df_path=root_dir+"/"+s_file_name+'/duration'+str(dd)+"/"+csv_f_name
        df=pd.read_csv(read_df_path)

        df=df.loc[df['Projected Demand (%)']==df['Projected Demand (%)'].max()]

        dispatcher.utter_message(text="Highest percentage of occupied beds for the selected scenario ({}) in the current Week (ending on {}) and default hospitalization duration of {} days is for {} region and its value is {} percent.".format(scenario,sat_date,dd,",".join(list(df['region_name'])),str(list(df['Projected Demand (%)'])[0])))
        dispatcher.utter_message(text="Do you want to check for any other duration?",buttons=[{'title': 'Yes', 'payload': '/yes'}, {'title': 'No', 'payload': '/no'}])
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
                
        return [SlotSet("hospitalization_days", None)]

class ActionCrisisMode(Action):

    def name(self) -> Text:
        return "action_crisis_mode"
        

    def run(self, dispatcher, tracker, domain):
        region=tracker.get_slot("region")
        scenario = tracker.get_slot("scenario")
        week_ending_date= tracker.get_slot("week_ending_date")
        hospitalization_days= tracker.get_slot("hospitalization_days")

        json_path=root_dir+"/supported_scenarios.json"

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
            
        # Check if hospitlization days are provided
        if(hospitalization_days!=None):
            dd=hospitalization_days
        else:
            dd=data['configuration']['defaultDuration']

        # Create Scenario Map
        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Get Folder Name as per selected file scenario
        s_file_name=scenario_map.loc[scenario_map['Scenario']==scenario]['File_Name'][0]

        # Get current weeks saturday's date
        if( week_ending_date==None):
            now = datetime.now()
            sat_date = now - timedelta(days = now.weekday()-5)
            sat_date=sat_date.strftime('%m-%d-%Y')
        else:
            sat_date=week_ending_date
            
            

        # Filename for the current week
        csv_f_name="nssac_ncov_ro_"+str(sat_date)+".csv"

        # Read Data as per the selected scenario, default duration and for the current week
        read_df_path=root_dir+"/"+s_file_name+'/duration'+str(dd)+"/"+csv_f_name
        df=pd.read_csv(read_df_path)

        df=df.loc[df['Projected Demand (%)']>=120]
        df=df[["region_name",'Projected Demand (%)']]
        df=pd.DataFrame(df.rename(columns={"region_name":"Region","Projected Demand (%)":'% of Occupied Beds'}))

        if len(df)>0:
            #dispatcher.utter_message("Below are the regions in crisis* mode")
            # Convert to Dictionary
            json_dict=json.loads(df.to_json(orient='split'))
            del json_dict['index']
            json_dict['isTable']=True
            json_dict=json.dumps(json_dict)
            dispatcher.utter_message("Below are the regions in crisis stage:")                              
            dispatcher.utter_message(json_message=json_dict)
            #dispatcher.utter_message(df.to_html(index=False, justify="justify-all"))
            dispatcher.utter_message(text="The above result is for the current Week (ending on {}) and default hospitalization duration of {} days, Do you want to check for any other duration?".format(sat_date,dd), buttons=[{'title': 'Yes', 'payload': '/yes'}, {'title': 'No', 'payload': '/no'}])
            with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
                filehandle.writelines("%s\n" % place for place in tracker.events)
        else:
            dispatcher.utter_message(text="Currently no regions are in crisis stage..!!")
            dispatcher.utter_message(text="The above result is for the current Week (ending on {}) and default hospitalization duration of {} days, Do you want to check for any other duration?".format(sat_date,dd), buttons=[{'title': 'Yes', 'payload': '/yes'}, {'title': 'No', 'payload': '/no'}])
            with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
                filehandle.writelines("%s\n" % place for place in tracker.events)
        return [SlotSet("hospitalization_days", None)]

class ActionProjectedPercentageOccupiedBeds(Action):

    def name(self) -> Text:
        return "action_projected_percentage_occupied_beds"
        

    def run(self, dispatcher, tracker, domain):
        region=tracker.get_slot("region")
        scenario = tracker.get_slot("scenario")
        week_ending_date= tracker.get_slot("week_ending_date")
        hospitalization_days= tracker.get_slot("hospitalization_days")

        json_path=root_dir+"/supported_scenarios.json"

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
            
        # Check if hospitlization days are provided
        if(hospitalization_days!=None):
            dd=hospitalization_days
        else:
            dd=data['configuration']['defaultDuration']

        # Create Scenario Map
        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Get Folder Name as per selected file scenario
        s_file_name=scenario_map.loc[scenario_map['Scenario']==scenario]['File_Name'][0]

        # Get current weeks saturday's date
        if( week_ending_date==None):
            now = datetime.now()
            sat_date = now - timedelta(days = now.weekday()-5)
            sat_date=sat_date.strftime('%m-%d-%Y')
        else:
            sat_date=week_ending_date
            
            

        # Filename for the current week
        csv_f_name="nssac_ncov_ro_"+str(sat_date)+".csv"

        # Read Data as per the selected scenario, default duration and for the current week
        read_df_path=root_dir+"/"+s_file_name+'/duration'+str(dd)+"/"+csv_f_name
        df=pd.read_csv(read_df_path)

        df=df.loc[df["region_name"]==region]

        dispatcher.utter_message(text="{}% beds will be occupied in case of {} days of hospitalization for the current week (ending on {}).".format(str(float(df["Projected Demand (%)"])),str(dd),sat_date))
        dispatcher.utter_message(text="Do you want to check for any other duration?".format(sat_date,dd), buttons=[{'title': 'Yes', 'payload': '/yes'}, {'title': 'No', 'payload': '/no'}])
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
        return [SlotSet("hospitalization_days", None)]

class ActionSelectScenario(Action):

    def name(self) -> Text:
        return "action_select_scenario"
        

    def run(self, dispatcher, tracker, domain):
    
        json_path=root_dir+"/supported_scenarios.json"
        
        # Read Scenario.json to update the filename
        with open(json_path) as f:
            data = json.load(f)
        
        scenario_map=pd.DataFrame()
        for i in range(len(data['scenarios'])):
            f_name=data['scenarios'][i]['directory']
            f_name=f_name.replace("data_va_durations/","")
            
            s_name=data['scenarios'][i]['scenario_display_name_line1']
            
            temp_df=pd.concat([pd.DataFrame({"File_Name":[f_name]}),pd.DataFrame({"Scenario":[s_name]})],axis=1)
            scenario_map=scenario_map.append(temp_df)
            
        # Get Scenario buttons at random
        buttons = []
        for t in scenario_map['Scenario']:
            buttons.append({"title":"{}".format(t),"payload": str('''/select_scenario{"scenario":"'''+t+'''"}''')})
        #logger.debug(buttons)
        
        #dispatcher.utter_message(buttons)
        dispatcher.utter_message(text="Please Select Scenario", buttons=buttons)
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
        return []

class ActionSelectRegion(Action):

    def name(self) -> Text:
        return "action_select_region"
        

    def run(self, dispatcher, tracker, domain):
    
        json_path=root_dir+"/supported_scenarios.json"
        
        # Read Scenario.json to update the filename
        with open(json_path) as f:
            data = json.load(f)

        # Get list of scenarios. These are the list of folders in root directory
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]

        # Get the list of file in any scenario and duration 8
        week_files=(os.listdir(root_dir+"/"+dirlist[0]+"/duration8/"))

        # Remove summary file from list
        week_files.remove('nssac_ncov_ro-summary.csv')

        # Read any file to get the region name
        df=pd.read_csv(root_dir+"/"+dirlist[0]+"/duration8/"+week_files[0])

        region_list= list(df['region_name'])
            
        # Get Scenario buttons at random
        buttons = []
        for r in region_list:
            buttons.append({"title":"{}".format(r),"payload": str('''/select_region{"region":"'''+r+'''"}''')})

        dispatcher.utter_message(text="Please Select region", buttons=buttons)
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
        return []
        
class ActionSelectWeek(Action):

    def name(self) -> Text:
        return "action_select_week"
        

    def run(self, dispatcher, tracker, domain):
    
        # Get any of the first directory name
        dirlist = [ item for item in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, item)) ]
        folder_name=dirlist[0]

        json_path=root_dir+"/supported_scenarios.json"

        # Read Scenario.json to get the default duration
        with open(json_path) as f:
            data = json.load(f)
            
        dd=data['configuration']['defaultDuration']

        # Get the names of csv files to extract date
        week_files=os.listdir(root_dir+"/"+folder_name+"/duration"+str(dd))

        # Remove summary file from list
        week_files.remove('nssac_ncov_ro-summary.csv')
        # Extract date
        week_date=[]
        for f in week_files:
            f=f.replace("nssac_ncov_ro_","")
            f=f.replace(".csv","")
            f=datetime.strptime(f, '%m-%d-%Y')
            week_date.append(f)

        week_date.sort()
        week_date.pop()
        #week_date=[x.strftime('%m-%d-%Y') for x in week_date]

        # Create a list for week with number
        #button_title=["Week Ending "+str(x.strftime("%b"))+" "+str(x.day) for x in week_date]

        buttons = []
        for t in week_date:
            buttons.append({"title":"{}".format("Week Ending "+str(t.strftime("%b"))+" "+str(t.day)),"payload": str('''/select_week{"week_ending_date":"'''+t.strftime('%m-%d-%Y')+'''"}''')})
        #logger.debug(buttons)
        dispatcher.utter_message(text="Please Select Week", buttons=buttons)
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
        return []

class ActionSelectDays(Action):

    def name(self) -> Text:
        return "action_select_days"
        

    def run(self, dispatcher, tracker, domain):
        # Create buttons from 1 -14
        buttons = []
        for i in range(1,15):
            buttons.append({"title":"{}".format(i),"payload": str('''/select_days{"hospitalization_days":"'''+str(i)+'''"}''')})
        dispatcher.utter_message(text="Select Hospitalization Days:", buttons=buttons)
        with open(log_file_location+str(tracker.sender_id)+"_"+'log.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events)
        return []
