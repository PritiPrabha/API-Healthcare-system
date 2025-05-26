create database health;
use health;
create table patient(pid SERIAL primary key,pname text,ppemail text,ppassw text,pphn BIGINT,pplace text);
create table doctor(did SERIAL primary key,dname text,demail text,dpassw text,dphn BIGINT,dspec text,dkw text);
create table query(qid SERIAL primary key,pemail text,kw text,answer text);
select * from patient;
select * from doctor;
select * from query;
