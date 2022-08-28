create table IF NOT EXISTS listings(
	item_id varchar(12), 
	title varchar not null, 
	global_id varchar, 
	product_id varchar, 
	postal_code varchar,
	location_ varchar, 
	country varchar, 
	currency varchar, 
	price numeric, 
	condition_ varchar, 
	shipping_type varchar,
	shipping_currency varchar, 
	shipping_cost numeric, 
	top_rated boolean, 
	start_date date, 
	end_date date, 
	listing_type varchar,
	date_added date,
	canadian_price_base numeric,
	canadian_total numeric

	PRIMARY KEY(item_id, date_added)
);

create table IF NOT EXISTS smartphones(
	phone_id varchar(32),
	brand varchar,
	series varchar,
	model varchar,
	phone_name varchar,
	storage_size varchar,

	primary key (phone_id)
);

create table IF NOT EXISTS phonelistings(
	phone_id varchar(32),
	item_id varchar(12),
	date_added date,
	
	primary key (phone_id, item_id, date_added),
	foreign key (item_id, date_added) references listings (item_id, date_added) on delete cascade on update cascade,
	foreign key (phone_id) references smartphones (phone_id) on update cascade
);