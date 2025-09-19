create database atm;
use atm;

create table accounts (
Acc_no int primary key,
Acc_holder varchar (20),
Pin int,
Balance float default 0
);

insert into accounts values(1001,"Gopi",1234,5000);

select * from accounts;