# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 17:34:53 2020

@author: Ashish Kumar
"""


# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd
import dateparser
import random
import numpy as np
from word2number import w2n
from rasa_sdk.events import AllSlotsReset

        

class ActionCount(Action):
    """Action for listing entities.
    The entities might be filtered by specific attributes."""

    def name(self):
        return "action_count"

    def run(self, dispatcher, tracker, domain):
    
        # Data Directory
        data_dir="/appp/data/"
        
        case_type = tracker.get_slot("case_type")
        cardinal = tracker.get_slot("CARDINAL")
        county_name= tracker.get_slot("county_name")
        state_name = tracker.get_slot("state_name")
        country_name = tracker.get_slot("country_name")
        measure = tracker.get_slot("measure")
        state_country= tracker.get_slot("state_country")
        filter_clues= tracker.get_slot("filter_clues")
        extracted_date=tracker.get_slot("DATE")
        
        
        
        # Convert  all entities to lower case
        if (case_type!=None):
            case_type = str.lower(tracker.get_slot("case_type"))
        if (cardinal!=None):
            cardinal = int(w2n.word_to_num(tracker.get_slot("CARDINAL")))
        if (county_name!=None):
            county_name = str.lower(tracker.get_slot("county_name"))
        if (state_name!=None):
            state_name = str.lower(tracker.get_slot("state_name"))
        if (country_name!=None):
            country_name = str.lower(tracker.get_slot("country_name"))
        if (measure!=None):
            measure = str.lower(tracker.get_slot("measure"))
        if (state_country!=None):
            state_country= str.lower(tracker.get_slot("state_country"))
        if (filter_clues!=None):
            filter_clues= str.lower(tracker.get_slot("filter_clues"))
            
        #----------------Check If date is provided, if yes then parse-----------------#
        #-------------------- it and if no then select today's date-------------------#
        if (extracted_date in [None,'today','Today']):
            # Take the latest date from the summary sheet. This is done because
            # the file is updated as per US time Zone and many countries are ahead of
            # it and sometimes the data is also not available for the today's date
            # so, its better to show the latest available data.
            
            #Read Summary Sheet
            summary_df=pd.read_csv(data_dir+"/uidata/nssac-ncov-sd-summary.csv")
            latest_date=summary_df.iloc[-1].date
            entered_date= dateparser.parse(latest_date).date().strftime('%m-%d-%Y')
            dispatcher.utter_message(text="Selected Date {0}".format(entered_date))
        else:
            entered_date= dateparser.parse(extracted_date).date().strftime('%m-%d-%Y')
            dispatcher.utter_message(text="Selected Date {0}".format(entered_date))
        
        #-----------------------------------------------------------------------------#
        with open('/appp/listfile.txt', 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in tracker.events_after_latest_restart())         
        
        #-----------------------------------------------------------------------------#
        # Check if date is greater than today's date
        # Through an error message and ask user to enter date at max till today.
        #-----------------------------------------------------------------------------#


        #-----------------------------------------------------------------------------#
        # Check if multiple combination of state and county is available? Give the user
        # an option to select county / state / country
        #-----------------------------------------------------------------------------#

        #-----------------------------------------------------------------------------#
        # Check Using Spacy, if the identified GPE is not present in any of the 
        # combined list of county /state or country then ask the user to modify query 
        # for their state or country
        #-----------------------------------------------------------------------------#


            
        #------------------If County Name is Mentioned in User Utterance--------------#
        if (county_name!=None):
            county_file_date= dateparser.parse(entered_date).date().strftime('%Y-%m-%d')
            f_name_county="nssac-ncov-sd-usa-"+county_file_date+".csv"
            df=pd.read_csv(data_dir+"uidata/usa_counties/"+f_name_county)
            # Lower case Name (County) and Region (State) column
            df['Name']=df['Name'].str.lower()
            df['Region']=df['Region'].str.lower()
            # Filter data as per county
            df=df.loc[df['Name']==county_name]
            # Check for Measures
            
            #--------------------Measure Total-----------------------------#
            if(measure in ["how many",'total',None,'count']):
                #dispatcher.utter_message(text="County - Entered Total")
                if(measure=='total'):
                    #Check for case type
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['Confirmed'])
                        dispatcher.utter_message(text="Showing results for Total Confirmed Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['Est.Recovered'])
                        dispatcher.utter_message(text="Showing results for Total Recovered Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['Deaths'])
                        dispatcher.utter_message(text="Showing results for Total Death Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['Est.Active'])
                        dispatcher.utter_message(text="Showing results for Total Active Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                
                # Check if filter clues like till / untill is specified
                elif(measure !='total' and filter_clues in ['till','untill', 'as of']):
                    #dispatcher.utter_message(text="County - till/untill")
                    # Cumilative values are to be selected
                    #Check for case type
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['Confirmed'])
                        dispatcher.utter_message(text="Showing results for Total Confirmed Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['Est.Recovered'])
                        dispatcher.utter_message(text="Showing results for Total Recovered Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['Deaths'])
                        dispatcher.utter_message(text="Showing results for Total Death Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['Est.Active'])
                        dispatcher.utter_message(text="Showing results for Total Active Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                else:
                    # Daily count is to be selected
                    #Check for case type
                    #dispatcher.utter_message(text="County - else")
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['newConfirmed'])
                        dispatcher.utter_message(text="Showing results for Confirmed Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['newEst.Recovered'])
                        dispatcher.utter_message(text="Showing results for Recovered Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['newDeaths'])
                        dispatcher.utter_message(text="Showing results for Death Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['newEst.Active'])
                        dispatcher.utter_message(text="Showing results for Active Cases in {0}".format(county_name))
                        dispatcher.utter_message(text=str(out_val))
            #--------------------------------------------------------------#
            
            
         
        #------------------If State Name is Mentioned in User Utterance---------------#    
        elif (state_name!=None):
            # Fetch the required file from the uidata directory as per date
            f_name_state_country="nssac-ncov-sd-"+entered_date+".csv"
            # Read data
            df=pd.read_csv(data_dir+"uidata/"+f_name_state_country)
            # Lower case Name (State) and Region (Country) column
            df['Name']=df['Name'].str.lower()
            df['Region']=df['Region'].str.lower()
            
            #Select data as per state
            df=df.loc[df['Name']==state_name]
            
            # Check if data is available else look for other location
            if(len(df)==0):
                date_format= dateparser.parse(entered_date).date().strftime('%Y-%m-%d')
                # Fetch the required file from the uidata directory as per date
                f_name="nssac-ncov-sd-admin1-"+date_format+".csv"
                # Read data
                df=pd.read_csv(data_dir+"uidata/admin1/"+f_name)
                # Lower case Name (State/County) and Region (Country) column
                df['Name']=df['Name'].str.lower()
                df['Region']=df['Region'].str.lower()
                
                # Filter data as per country
                df=df.loc[df['Name']==state_name]
        
            # Check for Measures
            
            #--------------------Measure Total-----------------------------#
            if(measure in ["how many",'total',None,'count']):
                if(measure=='total'):
                    #dispatcher.utter_message(text="state - Entered Total")
                    #Check for case type
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['Confirmed'])
                        dispatcher.utter_message(text="Showing results for Total Confirmed Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['Est.Recovered'])
                        dispatcher.utter_message(text="Showing results for Total Recovered Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['Deaths'])
                        dispatcher.utter_message(text="Showing results for Total Death Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['Est.Active'])
                        dispatcher.utter_message(text="Showing results for Total Active Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                
                # Check if filter clues like till / untill is specified
                elif(measure !='total' and filter_clues in ['till','untill', 'as of']):
                    #dispatcher.utter_message(text="State - Entered till/untill")
                    # Cumilative values are to be selected
                    #Check for case type
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['Confirmed'])
                        dispatcher.utter_message(text="Showing results for Total Confirmed Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['Est.Recovered'])
                        dispatcher.utter_message(text="Showing results for Total Recovered Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['Deaths'])
                        dispatcher.utter_message(text="Showing results for Total Death Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['Est.Active'])
                        dispatcher.utter_message(text="Showing results for Total Active Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                else:
                    # Daily count is to be selected
                    #Check for case type
                    #dispatcher.utter_message(text="state - Entered else")
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['newConfirmed'])
                        dispatcher.utter_message(text="Showing results for Confirmed Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['newEst.Recovered'])
                        dispatcher.utter_message(text="Showing results for Recovered Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['newDeaths'])
                        dispatcher.utter_message(text="Showing results for Death Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['newEst.Active'])
                        dispatcher.utter_message(text="Showing results for Active Cases in {0}".format(state_name))
                        dispatcher.utter_message(text=str(out_val))
            #--------------------------------------------------------------#
                
                
        #------------------If Country Name is Mentioned in User Utterance-------------#
        elif (country_name!=None):
               
            #--------------------Measure Total-----------------------------#
            if(measure in ["how many",'total',None,'count']):
                # Fetch the required file from the uidata directory as per date
                f_name_state_country="nssac-ncov-sd-"+entered_date+".csv"
                # Read data
                df=pd.read_csv(data_dir+"uidata/"+f_name_state_country)
                # Lower case Name (State/County) and Region (Country) column
                df['Name']=df['Name'].str.lower()
                df['Region']=df['Region'].str.lower()
                
                # Filter data as per country
                #Select data as per state
                df=df.loc[df['Name']==country_name]
                
                if(measure=='total'):
                    #dispatcher.utter_message(text="Country - Entered Total")
                    #Check for case type
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['Confirmed'])
                        dispatcher.utter_message(text="Showing results for Total Confirmed Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['Est.Recovered'])
                        dispatcher.utter_message(text="Showing results for Total Recovered Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['Deaths'])
                        dispatcher.utter_message(text="Showing results for Total Death Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['Est.Active'])
                        dispatcher.utter_message(text="Showing results for Total Active Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                
                # Check if filter clues like till / untill is specified
                elif(measure !='total' and filter_clues in ['till','untill', 'as of']):
                    #dispatcher.utter_message(text="Country - Entered till/untill")
                    # Cumilative values are to be selected
                    #Check for case type
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['Confirmed'])
                        dispatcher.utter_message(text="Showing results for Total Confirmed Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['Est.Recovered'])
                        dispatcher.utter_message(text="Showing results for Total Recovered Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['Deaths'])
                        dispatcher.utter_message(text="Showing results for Total Death Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['Est.Active'])
                        dispatcher.utter_message(text="Showing results for Total Active Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                else:
                    # Daily count is to be selected
                    #Check for case type
                    #dispatcher.utter_message(text="Country - Entered daily Else")
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['newConfirmed'])
                        dispatcher.utter_message(text="Showing results for Confirmed Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['newEst.Recovered'])
                        dispatcher.utter_message(text="Showing results for Recovered Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['newDeaths'])
                        dispatcher.utter_message(text="Showing results for Death Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['newEst.Active'])
                        dispatcher.utter_message(text="Showing results for Active Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
            #--------------------------------------------------------------#
                       
            
        #-----------------If County / State / Country is not mentioned,---------------#
        #----------------- then dispaly count across globe ---------------------------#
        else:
            df=pd.read_csv(data_dir+"uidata/"+"nssac-ncov-sd-summary.csv")
            # Filter as per date
            df=df.loc[df['date']==entered_date]
            # Check for Measures 
            
            #--------------------Measure Total-----------------------------#
            if(measure in ["how many",'total',None]):
                # Check if filter clues like till / untill is specified
                if(measure=='total'):
                    #Check for case type
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['Confirmed'])
                        dispatcher.utter_message(text="Showing results for Total Confirmed Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['Est.Recovered'])
                        dispatcher.utter_message(text="Showing results for Total Recovered Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['Deaths'])
                        dispatcher.utter_message(text="Showing results for Total Death Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['Est.Active'])
                        dispatcher.utter_message(text="Showing results for Total Active Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                
                # Check if filter clues like till / untill is specified
                elif(measure !='total' and filter_clues in ['till','untill', 'as of']):
                    # Cumilative values are to be selected
                    #Check for case type
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['Confirmed'])
                        dispatcher.utter_message(text="Showing results for Total Confirmed Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['Est.Recovered'])
                        dispatcher.utter_message(text="Showing results for Total Recovered Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['Deaths'])
                        dispatcher.utter_message(text="Showing results for Total Death Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['Est.Active'])
                        dispatcher.utter_message(text="Showing results for Total Active Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                else:
                    # Daily count is to be selected
                    #Check for case type
                    if (case_type in [None, 'confirmed']):
                        out_val=int(df['newConfirmed'])
                        dispatcher.utter_message(text="Showing results for Confirmed Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['recovered', 'recovery']):
                        out_val=int(df['newEst.Recovered'])
                        dispatcher.utter_message(text="Showing results for Recovered Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['deaths','death','deceased']):
                        out_val=int(df['newDeaths'])
                        dispatcher.utter_message(text="Showing results for Death Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
                    if (case_type in ['active']):
                        out_val=int(df['newEst.Active'])
                        dispatcher.utter_message(text="Showing results for Active Cases in {0}".format(country_name))
                        dispatcher.utter_message(text=str(out_val))
            #--------------------------------------------------------------#

        return [AllSlotsReset()]
