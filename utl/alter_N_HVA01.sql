alter table N_HVA01 drop primary key;
alter table N_HVA01 add id integer AUTO_INCREMENT NOT NULL PRIMARY KEY;
alter table N_HVA01 modify column id int(11) first;