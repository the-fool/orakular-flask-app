drop table students cascade constraints / 
drop table department cascade constraints / 
drop table faculty cascade constraints /
drop table courses cascade constraints / 
drop table enrolled / drop table staff /
drop sequence student_id / drop sequence course_id / drop sequence faculty_id /
drop sequence staff_id / drop sequence department_id 
/
create table students (sid integer primary key not null, 
sname varchar(50) not null, major varchar(30) default 'undeclared' not null, 
s_level varchar(15) not null, age integer)
/
create table department
(did integer primary key not null, dname varchar(50))
/
create table faculty
(fid integer primary key not null, fname varchar(50), deptid integer,
foreign key(deptid) references department(did)
  on delete set null)
/
create table courses
(cid char(12) primary key not null, cname varchar(50) not null,
meets_at char(30), room char(15), fid integer, limit integer,
foreign key(fid) references faculty(fid) 
  on delete set null)
/
create table enrolled
(sid integer, cid char(12), exam1 integer, exam2 integer, final integer,
  primary key (sid, cid), 
  foreign key(sid) references students(sid)
   on delete cascade
  ,
  foreign key(cid) references courses(cid)
   on delete cascade
)
/
create table staff
(sid integer primary key not null, sname varchar(50), deptid integer,
foreign key(deptid) references department(did)
 on delete set null)
/
create sequence student_id
/
create sequence course_id
/
create sequence faculty_id
/
create sequence staff_id
/
create sequence department_id
/
create trigger student_id_increment
before insert on students
for each row
begin
  select student_id.NEXTVAL
  into :new.sid
  from dual;
end;
/
create trigger fid_increment
before insert on faculty
for each row
begin
  select faculty_id.NEXTVAL
  into :new.fid
  from dual;
end;
/
create trigger cid_increment
before insert on courses
for each row
begin
  select course_id.NEXTVAL
  into :new.cid
  from dual;
end;
/
create trigger staff_id_increment
before insert on staff
for each row
begin
  select staff_id.NEXTVAL
  into :new.sid
  from dual;
end;
/
create trigger dept_id_increment
before insert on department
for each row
begin
  select department_id.NEXTVAL
  into :new.did
  from dual;
end;
