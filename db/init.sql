drop table if exists sms;

create table sms
(
	id INTEGER
		primary key
		 autoincrement,
	SMSRN VARCHAR(64),
	SMSRF int,
	SMSRB VARCHAR(512),
	SMSRD VARCHAR(64),
	SMSRT VARCHAR(64)
);