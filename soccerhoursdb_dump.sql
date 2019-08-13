create table sequences(name varchar(10), seq int);
insert into sequences values('user',104);
insert into sequences values('venue',206);
insert into sequences values('events',300);

CREATE TABLE user (

    pk_user_id INTEGER PRIMARY KEY AUTO_INCREMENT,

    user_fname VARCHAR(50),

    user_lname VARCHAR(50),

    username VARCHAR(50) NOT NULL,

    admin_status VARCHAR(1) NOT NULL,

    user_status VARCHAR(1) NOT NULL,

    user_email VARCHAR(50) NOT NULL,

    user_password VARCHAR(50) NOT NULL,

    zip_code INTEGER NOT NULL,

    date_added TIMESTAMP NOT NULL

);

INSERT INTO user VALUES(101,'Subhayu','Chakravarty','s7chak','A','A','s7chak@gmail.com','admin123',78751,'2019-07-28 13:29:09.589918');

INSERT INTO user VALUES(102,'Abhishek','Kardak','k4rd4k','N','A','akardak1@gmail.com','ghkhjGHGHG&^*^&*',78751,'2019-07-28 14:15:07.336178');

INSERT INTO user VALUES(103,'Prajval','Gupta','pgupta','N','A','pgupta@gmail.com','Abcd1234',78751,'2019-07-28 14:17:04.680268');

INSERT INTO user VALUES(104,'Shivang','Arya','sarya7','N','A','sarya7@gmail.com','sarya222',78751,'2019-07-28 14:20:12.563833');

CREATE TABLE venue (

    pk_venue_id INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,

    venue_name VARCHAR(50) NOT NULL,

    venue_desc VARCHAR(50) NOT NULL,

    venue_st_addr VARCHAR(50) NOT NULL,

    venue_zip_code INTEGER NOT NULL

);

INSERT INTO venue VALUES(201,'Charles Alan Wright Field_1','UT Intramural grounds','UT Austin',78712);

INSERT INTO venue VALUES(202,'Zilker Field_1','Zilker grounds','Zilker Park',78702);

INSERT INTO venue VALUES(203,'Clarks Field_1','Clarks grounds','UT Austin',78711);

INSERT INTO venue VALUES(204,'Clarks Field 2','UT Austin Clark''s ground 1','UT Austin',78712);

INSERT INTO venue VALUES(205,'Clarks Field 3','UT Austin Clark''s ground 1','UT Austin',78712);

INSERT INTO venue VALUES(206,'Zilker Field 2','Zilker Park ground 2','Zilker Park, Austin',78702);

CREATE TABLE slots (

    slot_id INTEGER NOT NULL,

    venue_id INTEGER NOT NULL,

    date DATETIME NOT NULL,

    availability VARCHAR(50) NOT NULL,
    event_id INTEGER

);


CREATE TABLE event_members (

    event_id INTEGER NOT NULL,

    user_id INTEGER NOT NULL

);


CREATE TABLE timeslots (

    start_time INTEGER NOT NULL,

    slot_id INTEGER NOT NULL

);

INSERT INTO timeslots VALUES(8,1);

INSERT INTO timeslots VALUES(9,2);

INSERT INTO timeslots VALUES(10,3);

INSERT INTO timeslots VALUES(11,4);

INSERT INTO timeslots VALUES(12,5);

INSERT INTO timeslots VALUES(13,6);

INSERT INTO timeslots VALUES(14,7);

INSERT INTO timeslots VALUES(15,8);

INSERT INTO timeslots VALUES(16,9);

INSERT INTO timeslots VALUES(17,10);

INSERT INTO timeslots VALUES(18,11);

INSERT INTO timeslots VALUES(19,12);

INSERT INTO timeslots VALUES(20,13);

CREATE TABLE events (

    pk_event_id INTEGER PRIMARY KEY AUTO_INCREMENT,

    event_name VARCHAR(50) NOT NULL,

    event_desc VARCHAR(50) NOT NULL,

    event_date DATE NOT NULL,

    start_time INTEGER NOT NULL,

    end_time INTEGER NOT NULL,

    user_id INTEGER NOT NULL,

    venue_id INTEGER NOT NULL,

    event_capacity INTEGER NOT NULL,

    event_status VARCHAR(50) NOT NULL,

    gender_option VARCHAR(50) NOT NULL,

    members_joined INTEGER NOT NULL

);

