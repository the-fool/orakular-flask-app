from app.models import Course, Department, Enrolled, Faculty, Staff, Student
from app.database import db_session as sess, cursor, db
from random import randint, shuffle
from database import db
from itertools import cycle
from app.student import views as student

db.ex("database/db_teardown.sql")
db.ex("database/db_config.sql")
db.ex("database/data.sql")

lc = sess.query(Course).all()                
ls = sess.query(Student).all()
for s in ls:
    tmp = lc[:]
    shuffle(tmp)
    i = 0
    while i < 3:
        d = {}
        d["cid"] = tmp.pop().cid
        d["sid"] = s.sid
        d["exam1"] = randint(50,100)
        d["exam2"] = randint(55,100)
        d["final"] = randint(55,100)
        en = Enrolled(**d)
        try: 
            if student.check_schedule(d["cid"], s.sid) == 0:
                sess.add(en)
                sess.commit()
            else:
                print "****SCHEDULE CONFLICT*****"
                i -= 1
        except:
            print "error"
            sess.rollback()
            i -= 1
        i += 1
            
        
