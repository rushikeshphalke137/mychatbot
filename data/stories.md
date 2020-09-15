## welcome message
* get_started
  - utter_get_started
  
## greet and exit
* greet
  - utter_greet
* goodbye
  - utter_goodbye

## total cases in state
* greet
    - utter_greet
* count{"GPE": "virginia", "DATE": "08-11-2020", "state_name": "virginia"}
    - slot{"DATE": "08-11-2020"}
    - slot{"state_name": "virginia"}
    - action_count
* goodbye
	- utter_goodbye
	
## Direct count
* count{"GPE": "maharashtra", "DATE": "08-11-2020", "state_name": "maharashtra"}
    - slot{"DATE": "08-11-2020"}
    - slot{"state_name": "maharashtra"}
    - action_count

