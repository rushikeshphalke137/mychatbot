# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 18:45:32 2020

@author: Ashish Kumar
"""

# Code to Merge Logfiles and Extract the following information from it.
# - UserId
# - Timestamp
# - Event (User Uttered/ Bot Uttered)
# - Displayed Text
# - Identified Intent
# - Entities Identified


# Import Packages
import re
import datetime
import pandas as pd 
import os   

# Logfiles location
log_file_dir="D:/UVA - Simulation Systems/Chatbot/mrdd_cb_v8/logs/"
out_dir="D:/UVA - Simulation Systems/Chatbot/mrdd_cb_v8/"

# Create lists and dataframes to store data
event_list=[]
text_list=[]
tstamp_list=[]
intent_list=[]
entities_list=[]
userid_list=[]

merged_log_df=pd.DataFrame()

# Get the list of all the .txt file for log files folder
log_list=os.listdir(log_file_dir)

# Iterate for each log file and parse data
for log_file in log_list:
    
    with open(log_file_dir+log_file) as fd:
        # Iterate over the lines
        for line in fd:
            # Clean Data
            line=line.replace("'", "")
            line=line.replace(": ", ":")
            line=line.replace("\'", "\"")
            line=line.replace("None","'None'")
            # Capture one-or-more characters of non-whitespace after the initial match
            match_event = re.search(r'event:(\S+)', line)
            
            #Check if we have an event
            if match_event:
                event = match_event.group(1)
                event=event.replace(",", "")
                
                # We are only intrested in user and bot events
                
                if event == 'user':
                    event_list.append(event)
                    
                    # Check for text, timestamp, intent and entities form each lines
                    match_text = re.search(r'text:(.*)parse_data:', line)
                    match_timestamp=re.search(r'timestamp:(.*?)\d*\.?\d+',line)
                    match_intent=re.search(r'''intent':(.*?)\d*\.?\d+}|intent:(.*?)\d*\.?\d+}''',line)
                    match_entities=re.search(r''''entities':(.*?)]|entities:(.*?)]''',line)
                    
                    # Clean text
                    if match_text:
                        # Yes, process it
                        text = match_text.group(1)
                        text=text.replace(",", "")
                        text_list.append(text)
                    else:
                        text_list.append("No text Identified")
                    
                    # Clean Timestamp
                    if match_timestamp:
                        tstamp= match_timestamp[0]
                        tstamp=tstamp.replace("timestamp:","")
                        #tstamp=re.match('\d*\.?\d+',tstamp)[0]
                        tstamp=str(datetime.datetime.fromtimestamp(float(tstamp)))
                        tstamp_list.append(tstamp)
                    
                    # Clean Intents
                    if match_intent:
                        intent=match_intent[0]
                        intent=intent.replace("{intent:","")
                        #intent=intent.replace(", entities","")
                        intent_list.append(intent)
                    else:
                        intent_list.append("No Intent Identified")
                    
                    # Clean Entities
                    if match_entities:
                        entities=match_entities[0]
                        entities=entities.replace(", entities","")
                        entities_list.append(entities)
                    else:
                        entities_list.append("No Entities Identified")
    
    
                if event == 'bot':
                    # Check for text, timestamp, intent and entities form each lines
                    event_list.append(event)
                    match_text = re.search(r'text:(.*) data:', line)
                    match_timestamp=re.search(r'timestamp:(.*?)\d*\.?\d+',line)
                    match_intent=re.search(r'''intent':(.*?)\d*\.?\d+}|intent:(.*?)\d*\.?\d+}''',line)
                    match_entities=re.search(r''''entities':(.*?)]|entities:(.*?)]''',line)
                    
                    # Clean text
                    if match_text:
                        # Yes, process it
                        text = match_text.group(1)
                        text=text.replace(",", "")
                        text_list.append(text)
                    else:
                        text_list.append("No text Identified")
                        
                    # Clean Timestamp    
                    if match_timestamp:
                        tstamp= match_timestamp[0]
                        tstamp=tstamp.replace("timestamp:","")
                        #tstamp=re.match('\d*\.?\d+',tstamp)[0]
                        tstamp=str(datetime.datetime.fromtimestamp(float(tstamp)))
                        tstamp_list.append(tstamp)
                        
                    # Clean Intents    
                    if  match_intent==None:
                        #intent_list.append("No Intents as this is bot utterance")
                        intent_list.append("")
                    else:
                        intent=match_intent[0]
                        intent=intent.replace("{intent:","")
                        intent_list.append(intent)
                        
                    # Clean Entities    
                    if match_entities:
                        entities=match_entities[0]
                        entities=entities.replace(", entities","")
                        entities_list.append(entities)
                    else:
                        #entities_list.append("No Entities as this is bot utterance")
                        entities_list.append("")
    # Create a temporary dataframe to store all information in a dataframe
    df=pd.DataFrame()
    df['UserId']=[str(log_file.replace("_log.txt",""))]*len(event_list)
    df['Timestamp']=tstamp_list
    df['Event']=event_list
    df['Text']=text_list
    df['Identified Intent']=intent_list
    df['Entities']=entities_list
    merged_log_df=merged_log_df.append(df)

merged_log_df.to_csv(out_dir+"Parsed_LogFile.csv", index=False)
    


