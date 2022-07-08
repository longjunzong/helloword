# TDengine smart meters

## Create a database
```
create database power keep 3650;
```

## Use a database
```
use power
```

## Create a super table
```
create table smart_meters(ts timestamp, current float, 
voltage float, phase float) tags (device_id binary(16), 
province binary(10), city binary(10), group_id int)
```

## Create a subsuper table
```
create table h1001 using smart_meters 
tags(‘1001’,’SiChuan’,’ChengDu’, 1);
```

## Insert a record
```
insert into h1001 (ts, current, voltage, phase) 
values (now, 10.3, 219.6, 0.38);
```
## Query records in a period
```
select ts, current, volitage, phase from h1001 where ts > now-30d
```

