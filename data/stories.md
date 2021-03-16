## hospitalization
* greet
  - utter_greet
* hospitalization
  - utter_hospitalization
  
## hospitalization and back
* greet
  - utter_greet
* hospitalization
  - utter_hospitalization
* greet
  - utter_greet

  
## occupied_beds
* greet
  - utter_greet
* occupied_beds
  - utter_occupied_beds

## say goodbye
* goodbye
  - utter_goodbye

  
  
## interactive_story_1
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* under_dev
    - utter_under_dev

## How many people are projected to be hospitalized this week?
* greet
    - utter_greet
* hospitalization
    - utter_hospitalization
* hospitalized_current_week
    - action_hospitalized_current_week
	- utter_fallback
	- action_restart
	
	
##What is the maximum number of people who are projected to be hospitalized?
* greet
    - utter_greet
* hospitalization
    - utter_hospitalization
* max_projected_hospitalization_current_week
	- action_max_projected_hospitalization_current_week
	- utter_fallback
	- action_restart

##What is the maximum number of people who are projected to be hospitalized?
* greet
    - utter_greet
* hospitalization
    - utter_hospitalization
* max_projected_hospitalization_current_week
	- action_max_projected_hospitalization_current_week
	- utter_fallback
	- action_restart
	
##When do hospitalizations peak?
* greet
    - utter_greet
* hospitalization
    - utter_hospitalization
* hospitalization_peak
	- action_select_scenario
* select_scenario{"scenario": "Adaptive"}
    - slot{"scenario": "Adaptive"}
	- action_hospitalization_peak
	- utter_fallback
	- action_restart
	
##What are the top 5 regions for hospitalizations?
* greet
    - utter_greet
* hospitalization
    - utter_hospitalization
* top_5_regions_hospitalization
	- slot{"CARDINAL":"5"}
	- action_select_scenario
* select_scenario{"scenario": "Adaptive"}
    - slot{"scenario": "Adaptive"}
	- action_top_5_regions_hospitalization
* no
	- utter_fallback
	- action_restart

	
	
##What are the top 5 regions for hospitalizations?  - Yes Loop
* greet
    - utter_greet
* hospitalization
    - utter_hospitalization
* top_5_regions_hospitalization
	- slot{"CARDINAL":"5"}
	- action_select_scenario
* select_scenario{"scenario": "Adaptive"}
    - slot{"scenario": "Adaptive"}
	- action_top_5_regions_hospitalization
* yes
	- action_select_week
* select_week{"week_ending_date":"10-17-2020"}
	- slot{"week_ending_date":"10-17-2020"}
	- action_top_5_regions_hospitalization
* yes
	- action_select_week
* select_week{"week_ending_date":"10-24-2020"}
	- slot{"week_ending_date":"10-24-2020"}
	- action_top_5_regions_hospitalization
* yes
	- action_select_week
* select_week{"week_ending_date":"10-31-2020"}
	- slot{"week_ending_date":"10-31-2020"}
	- action_top_5_regions_hospitalization
* no
	- utter_fallback
	- action_restart

##How many hospitalizations are expected in <region_name>?
* greet
    - utter_greet
* hospitalization
    - utter_hospitalization
* expected_hospitalization_in_region
	- action_select_region
* select_region{"region":"central"}
	- slot{"region":"central"}
	- action_select_scenario
* select_scenario{"scenario": "Adaptive"}
    - slot{"scenario": "Adaptive"}
	- action_expected_hospitalization_in_region
* yes
	- action_select_week
* select_week{"week_ending_date":"10-17-2020"}
	- slot{"week_ending_date":"10-17-2020"}
	- action_expected_hospitalization_in_region
* yes
	- action_select_week
* select_week{"week_ending_date":"10-24-2020"}
	- slot{"week_ending_date":"10-24-2020"}
	- action_expected_hospitalization_in_region
* yes
	- action_select_week
* select_week{"week_ending_date":"10-31-2020"}
	- slot{"week_ending_date":"10-31-2020"}
	- action_expected_hospitalization_in_region
* no
	- utter_fallback
	- action_restart


	
##Which scenario shows the highest number of projected hospitalizations?
* greet
    - utter_greet
* hospitalization
    - utter_hospitalization
* highest_projected_hospitalization
	- action_highest_projected_hospitalization
	- utter_fallback
	- action_restart
	
##Which regions are projected to have greater than <number>% of occupied beds?
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* projected_greater_occupied_beds
    - utter_projected_greater_occupied_beds
* projected_greater_occupied_beds{"CARDINAL": "86"}
    - slot{"CARDINAL": "86"}
    - action_select_scenario
* select_scenario{"scenario": "Adaptive-MoreControl"}
    - slot{"scenario": "Adaptive-MoreControl"}
    - action_projected_greater_occupied_beds
* yes
    - action_select_days
* select_days{"hospitalization_days": "11"}
    - slot{"hospitalization_days": "11"}
    - action_projected_greater_occupied_beds
* yes
    - action_select_days
* select_days{"hospitalization_days": "11"}
    - slot{"hospitalization_days": "11"}
    - action_projected_greater_occupied_beds
* yes
    - action_select_days
* select_days{"hospitalization_days": "11"}
    - slot{"hospitalization_days": "11"}
    - action_projected_greater_occupied_beds
* no
    - utter_fallback
    - action_restart


##Get projected percentages of occupied beds based on hospital capacity (Update Week)
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* projected_percentage_occupied_beds_hc
    - utter_projected_percentage_occupied_beds_hc
* number_check{"CARDINAL": "89.5"}
    - slot{"CARDINAL": "80"}
	- action_select_scenario
* select_scenario{"scenario": "Adaptive-LessControl"}
    - slot{"scenario": "Adaptive-LessControl"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "11-28-2020"}
    - slot{"week_ending_date": "11-28-2020"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "12-12-2020"}
    - slot{"week_ending_date": "12-12-2020"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "12-12-2020"}
    - slot{"week_ending_date": "12-12-2020"}
    - action_projected_percentage_occupied_beds_hc
* no
    - utter_fallback
    - action_restart
	
##Get projected percentages of occupied beds based on hospital capacity (Update Week)
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* projected_percentage_occupied_beds_hc
    - utter_projected_percentage_occupied_beds_hc
* number_check{"CARDINAL": "70"}
    - slot{"CARDINAL": "70"}
	- action_select_scenario
* select_scenario{"scenario": "Adaptive-LessControl"}
    - slot{"scenario": "Adaptive-LessControl"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "11-28-2020"}
    - slot{"week_ending_date": "11-28-2020"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "12-12-2020"}
    - slot{"week_ending_date": "12-12-2020"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "12-12-2020"}
    - slot{"week_ending_date": "12-12-2020"}
    - action_projected_percentage_occupied_beds_hc
* no
    - utter_fallback
    - action_restart
	
##Get projected percentages of occupied beds based on hospital capacity (Update Week)
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* projected_percentage_occupied_beds_hc
    - utter_projected_percentage_occupied_beds_hc
* number_check{"CARDINAL": "90"}
    - slot{"CARDINAL": "90"}
	- action_select_scenario
* select_scenario{"scenario": "Adaptive-LessControl"}
    - slot{"scenario": "Adaptive-LessControl"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "11-28-2020"}
    - slot{"week_ending_date": "11-28-2020"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "12-12-2020"}
    - slot{"week_ending_date": "12-12-2020"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "12-12-2020"}
    - slot{"week_ending_date": "12-12-2020"}
    - action_projected_percentage_occupied_beds_hc
* no
    - utter_fallback
    - action_restart
	
##Get projected percentages of occupied beds based on hospital capacity (Update Duration)
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* projected_percentage_occupied_beds_hc
    - utter_projected_percentage_occupied_beds_hc
* number_check{"CARDINAL": "86"}
    - slot{"CARDINAL": "86"}
    - action_select_scenario
* select_scenario{"scenario": "Adaptive-LessControl"}
    - slot{"scenario": "Adaptive-LessControl"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_days
    - action_select_days
* select_days{"hospitalization_days": "11"}
    - slot{"hospitalization_days": "11"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_days
    - action_select_days
* select_days{"hospitalization_days": "11"}
    - slot{"hospitalization_days": "11"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_days
    - action_select_days
* select_days{"hospitalization_days": "11"}
    - slot{"hospitalization_days": "11"}
    - action_projected_percentage_occupied_beds_hc
* no
    - utter_fallback
    - action_restart


## What is the highest projected percentage of occupied beds?
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* highest_projected_occupied_beds
    - action_select_scenario
* select_scenario{"scenario": "Adaptive-MoreControl"}
    - slot{"scenario": "Adaptive-MoreControl"}
    - action_highest_projected_occupied_beds
* yes
    - action_select_days
* select_days{"hospitalization_days": "11"}
    - slot{"hospitalization_days": "11"}
    - action_highest_projected_occupied_beds
* yes
    - action_select_days
* select_days{"hospitalization_days": "10"}
    - slot{"hospitalization_days": "10"}
    - action_highest_projected_occupied_beds
* yes
    - action_select_days
* select_days{"hospitalization_days": "12"}
    - slot{"hospitalization_days": "12"}
    - action_highest_projected_occupied_beds
* no
    - utter_fallback
    - action_restart

## Which regions are projected to enter crisis stage?
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* crisis_mode
    - action_select_scenario
* select_scenario{"scenario": "Adaptive-MoreControl"}
    - slot{"scenario": "Adaptive-MoreControl"}
	- action_crisis_mode
* yes
    - action_select_days
* select_days{"hospitalization_days": "11"}
    - slot{"hospitalization_days": "11"}
    - action_crisis_mode
* yes
    - action_select_days
* select_days{"hospitalization_days": "10"}
    - slot{"hospitalization_days": "10"}
    - action_crisis_mode
* yes
    - action_select_days
* select_days{"hospitalization_days": "12"}
    - slot{"hospitalization_days": "12"}
    - action_crisis_mode
* no
    - utter_fallback
    - action_restart

## What is the projected percentage of occupied beds?
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* projected_percentage_occupied_beds
	- action_select_region
* select_region{"region":"central"}
	- slot{"region":"central"}
    - action_select_scenario
* select_scenario{"scenario": "Adaptive-MoreControl"}
    - slot{"scenario": "Adaptive-MoreControl"}
	- action_projected_percentage_occupied_beds
* yes
    - action_select_days
* select_days{"hospitalization_days": "11"}
    - slot{"hospitalization_days": "11"}
    - action_projected_percentage_occupied_beds
* yes
    - action_select_days
* select_days{"hospitalization_days": "10"}
    - slot{"hospitalization_days": "10"}
    - action_projected_percentage_occupied_beds
* yes
    - action_select_days
* select_days{"hospitalization_days": "12"}
    - slot{"hospitalization_days": "12"}
    - action_projected_percentage_occupied_beds
* no
    - utter_fallback
    - action_restart


## About MRDD Loop using back to About MRDD button
* greet
    - utter_greet
* about_mrdd
	- utter_about_mrdd
* greet
	- utter_greet
* about_mrdd
	- utter_about_mrdd
* about_hospitalization
	-utter_about_hospitalization
* about_mrdd
	- utter_about_mrdd
* about_occupied_beds
	- utter_about_occupied_beds
* about_mrdd
	- utter_about_mrdd
* about_projected_mean
	- utter_about_projected_mean
* about_mrdd
	- utter_about_mrdd
* about_forecast
	- utter_about_forecast
* about_mrdd
	- utter_about_mrdd
* about_projected_forecast
	- utter_about_projected_forecast
* about_mrdd
	- utter_about_mrdd
* about_scenario
	- utter_about_scenario
* about_mrdd
	- utter_about_mrdd
	
	
## About MRDD Loop using back to Main Menu button
* greet
    - utter_greet
* about_mrdd
	- utter_about_mrdd
* greet
	- utter_greet
* about_mrdd
	- utter_about_mrdd
* about_hospitalization
	-utter_about_hospitalization
* greet
	- utter_greet
* about_mrdd
	- utter_about_mrdd
* about_occupied_beds
	- utter_about_occupied_beds
* greet
	- utter_greet
* about_mrdd
	- utter_about_mrdd
* about_projected_mean
	- utter_about_projected_mean
* greet
	- utter_greet
* about_mrdd
	- utter_about_mrdd
* about_forecast
	- utter_about_forecast
* greet
	- utter_greet
* about_mrdd
	- utter_about_mrdd
* about_projected_forecast
	- utter_about_projected_forecast
* greet
	- utter_greet
* about_mrdd
	- utter_about_mrdd
* about_scenario
	- utter_about_scenario
* greet
	- utter_greet
* about_mrdd
	- utter_about_mrdd
	

## interactive_story_1
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* projected_greater_occupied_beds
    - utter_projected_greater_occupied_beds
* projected_greater_occupied_beds{"CARDINAL": "86"}
    - slot{"CARDINAL": "86"}
    - action_select_scenario
* select_scenario{"scenario": "Adaptive-MoreControl"}
    - slot{"scenario": "Adaptive-MoreControl"}
    - action_projected_greater_occupied_beds
* yes
    - action_select_days
* select_days{"hospitalization_days": "11"}
    - slot{"hospitalization_days": "11"}
    - action_projected_greater_occupied_beds
* no
    - utter_fallback
    - action_restart


## interactive_story_1
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* projected_percentage_occupied_beds_hc
    - utter_projected_percentage_occupied_beds_hc
* select_scenario{"CARDINAL": "90"}
    - slot{"CARDINAL": "90"}
    - action_select_scenario
* select_scenario{"scenario": "Adaptive-LessControl"}
    - slot{"scenario": "Adaptive-LessControl"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "11-28-2020"}
    - slot{"week_ending_date": "11-28-2020"}
    - action_projected_percentage_occupied_beds_hc
* yes
    - utter_week_duration
* select_week
    - action_select_week
* select_week{"week_ending_date": "12-12-2020"}
    - slot{"week_ending_date": "12-12-2020"}
    - action_projected_percentage_occupied_beds_hc
* no
    - utter_fallback
    - action_restart

## interactive_story_1
* greet
    - utter_greet
* occupied_beds
    - utter_occupied_beds
* projected_percentage_occupied_beds_hc
    - utter_projected_percentage_occupied_beds_hc
* number_check{"CARDINAL": "80"}
    - slot{"CARDINAL": "80"}
    - action_select_scenario
* select_scenario{"scenario": "Adaptive-LessControl"}
    - slot{"scenario": "Adaptive-LessControl"}
    - action_projected_percentage_occupied_beds_hc
* no
    - utter_fallback
    - action_restart
