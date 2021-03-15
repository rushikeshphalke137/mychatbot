-- 	This script is used to created all tables for mrdd va data
-- 	created : 07/20/2020
--
-- 	By Komal K. Dudakiya
-- 
--table 1:  usa_mrdd_hrr.
CREATE TABLE IF NOT EXISTS :current_schema.usa_mrdd_hrr
(
	region_id character varying(128) PRIMARY KEY,
	region_name character varying(128) NULL,
	total_beds integer default NULL,
	last_updated_date date default (now() at time zone 'UTC')
);

-- table 2:  usa_mrdd_scenarios.
CREATE TABLE IF NOT EXISTS :current_schema.usa_mrdd_scenarios
(
	scenario_id SERIAL,-- PRIMARY KEY,
	name character varying(128) NULL,
	description character varying NULL,
	data_directory character varying NULL,
	default_duration integer,
	start_date date default (now() at time zone 'UTC'),
	end_date date NULL,
	last_update date default (now() at time zone 'UTC'),
	PRIMARY KEY (name)
);

-- table 3:  usa_mrdd_data.
CREATE TABLE IF NOT EXISTS :current_schema.usa_mrdd_data
(
	id SERIAL,
	scenario_id integer, --REFERENCES :current_schema.usa_va_mrdd_scenarios (scenario_id),
	region_id character varying(128) NULL,
	region_name character varying(128) NULL,
	reported_date date default (now() at time zone 'UTC'),
	weekly_hospitalizations_med integer,
	weekly_hospitalizations_lower_bound integer,
	weekly_hospitalizations_upper_bound integer,
	max_daily_occupancy integer,
	max_daily_occupancy_lower_bound integer,
	max_daily_occupancy_upper_bound integer,
	last_update date default (now() at time zone 'UTC'),
	duration integer default 7,
	PRIMARY KEY (scenario_id, region_id, reported_date, last_update, duration)
);