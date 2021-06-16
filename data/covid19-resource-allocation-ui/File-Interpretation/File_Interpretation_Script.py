# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 21:31:05 2020

@author: varun_mandiram
"""
import sys
import pandas as pd
from datetime import timedelta
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

def interpret_file(file_name,date_str):    
    #read date & data file
    #data_date = datetime.date(2020, 1, 21)
    data_date = datetime.strptime(date_str, '%m-%d-%Y').date()
    data=pd.read_csv(file_name, sep=" ", header=None)
    data.columns = ['gurobi','xyzf_data','ignore_data','value_data']
    
    #split to idenitify x & f rows 
    data[['xyzf_value','hrr_data']]= data.xyzf_data.str.split('\[|\]', expand=True).iloc[:,[0,1]]
    
    # subset wrt x and extract HRR number , no of days and value for x
    data_x=data[data['xyzf_value']=='x']
    data_x[['HRR_number','day_number']]=data_x.hrr_data.str.split(",",expand=True)
    data_x['HRR_number']=data_x['HRR_number'].astype(int)
    data_x['day_number']=data_x['day_number'].astype(int)
    data_x['Value_demand_beds']=data_x.value_data.str.split(")",expand=True)[0].astype(float)
    data_x=data_x.reset_index(drop=True)
    data_x_reqd=data_x[['HRR_number','day_number','Value_demand_beds']]
    
    
    # subset wrt f and extract HRR number ,transfer , no of days and value for f
    data_f=data[data['xyzf_value']=='f']
    data_f[['HRR_number','transfer','day_number']]=data_f.hrr_data.str.split(",",expand=True)
    data_f['HRR_number']=data_f['HRR_number'].astype(int)
    data_f['transfer']=data_f['transfer'].astype(int)
    data_f['day_number']=data_f['day_number'].astype(int)
    data_f['Value_demand_beds']=data_f.value_data.str.split(")",expand=True)[0].astype(float)
    data_f=data_f.reset_index(drop=True)
    data_f_reqd=data_f[['HRR_number','transfer','day_number','Value_demand_beds']]
    
    #compute fvalues related to x
    f_sum_value_list=[]
    for i,irow in data_x_reqd.iterrows():
        data_temp=data_f_reqd[(data_f_reqd['transfer']==irow['HRR_number']) & (data_f_reqd['day_number']==irow['day_number'])]
        f_beds_sum=data_temp['Value_demand_beds'].sum()
        f_sum_value_list.append(f_beds_sum)
    
    #Add fvalues to x
    data_x_reqd['f_sum_value']=f_sum_value_list
    data_x_reqd['Value']=data_x_reqd['Value_demand_beds']+data_x_reqd['f_sum_value']
    data_x_reqd['Date']=data_x_reqd.apply(lambda x: data_date+timedelta(days= x['day_number']),axis=1)
    data_x_reqd_agg=data_x_reqd[['HRR_number','Date','Value']]
    data_x_reqd_agg.to_csv("B0vars_D7_B0_Transformed.csv",index=False)
    
    return data_x_reqd_agg.head()



if __name__ == "__main__":
    #call both filename & date
    filename= sys.argv[1]
    date=sys.argv[2]
    interpret_file(filename,date)