from flask import Response, render_template, url_for, redirect, request, flash, abort
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import staff
from ..models import User, Staff, Student, Department, Enrolled, Course, Faculty
from .forms import AddCourseForm, HirePersonForm
from ..database import db_session as sess, cursor as c, db
from ..decorators import staff_only
import cx_Oracle

@staff.route('/dashboard', methods=['GET', 'POST'])
@login_required
@staff_only
def dashboard():
    add_course_form = AddCourseForm()
    hire_form = HirePersonForm()
    staff = sess.query(Staff).filter_by(sid=current_user.id).one()
    f_set = [(str(x[0]), x[1].title()) for x 
             in sess.query(Faculty.fid, Faculty.fname).filter_by(deptid = staff.deptid).all()]
    add_course_form.faculty.choices =  f_set
    
    if request.method=='POST':
        if add_course_form.validate_on_submit():
            print "validating " + add_course_form.faculty.data
            try:
                add_course_form.cname.data = add_course_form.cname.data.replace("'", "''")
                print add_course_form.cname.data
                c.execute("INSERT INTO courses (cid, cname, fid, meets_at, room, limit) VALUES ('{0}', '{1}', '{2}', 'NONE 0:00', 'none', 999)"
                          .format(str(add_course_form.cid.data).upper(), add_course_form.cname.data
                                  , str(add_course_form.faculty.data)))
                db.commit()
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                print "DB Error: {0} -- {1}".format(error.code, error.message)
                db.rollback()
                if error.code == 1:
                    flash('Primary key constraint: Failed to add course')
                else: flash('Failed to add course.')
    
        elif hire_form.validate_on_submit():
            print "hiring " + hire_form.name.data + " as " + hire_form.role.data
            if hire_form.role.data == 'staff':
                params = "(sname, deptid)"
            else: params = "(fname, deptid)"
            try:
                c.execute("INSERT INTO {0} {1} VALUES ('{2}', {3})"
                          .format(hire_form.role.data, params, hire_form.name.data, staff.deptid))  
                db.commit()
                flash('Hired {0}!'.format(hire_form.name.data))
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                print "DB Error: {0} -- {1}".format(error.code, error.message)
                db.rollback()
                flash('Failed to hire person')

        return redirect(url_for('.dashboard'))
    else:
        try:
            department = sess.query(Department).filter_by(did=staff.deptid).one()
            c_list = (sess
                      .query(Course, Faculty)
                      .filter(Faculty.deptid == staff.deptid)
                      .join(Faculty)
                      .all() 
                  )
            c_list = [ {'c': x[0], 'f': x[1]} for x in c_list]
            
            e_list = (sess
                      .query(Enrolled, Student)
                      .filter(Enrolled.cid.in_([x['c'].cid for x in c_list]))
                      .join(Student)
                      .all())
            e_list = [ {'e': x[0], 's': x[1]} for x in e_list] 
        
            for x in c_list:
                x['es'] = []
                for z in e_list:
                    if z['e'].cid == x['c'].cid:
                        x['es'].append(z)
                        
        except:
            raise
            
        return render_template('staff/dashboard.html', staff=staff, 
                               department=department, c_list = c_list, 
                               add_course_form = add_course_form, 
                               hire_form=hire_form)
                        
                        
@staff.route('/edit_grade', methods=['GET','POST'])
@login_required
@staff_only
def edit_grade():
    cid = request.form['pk'].split('_')
    test = request.form['name']
    value = request.form['value']

    try:
        c.execute("update enrolled set {0} = {1} where cid = '{2}' and sid = {3}"
                     .format(test, value, cid[1], cid[0]))
        db.commit()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print "DB Error: {0} - {1}".format(error.code, error.message)
        db.rollback()
        return Response(status=400)
    
    return Response(status=200)

@staff.route('/update_course', methods=['GET', 'POST'])
@login_required
@staff_only
def update_course():
    pk = request.form['pk']
    attr = request.form['name']
    val = request.form['value']
      
    try:
        c.execute("update courses set {0} = '{1}' where cid = '{2}'".format(attr, val, pk))
        db.commit()
    except cx_Oracle.DatabaseError as ex:
        error, = ex.args
        print "DB Error: {0} - {1}".format(error.code, error.message)
        db.rollback()
        if str(error.code) == '20001':
            print 'Enrollment Trigger'
            return Response('Registration limit is incompatible with enrollment', status=409)
            
        return Response(status=400)
   
    return Response(status=200)

@staff.route('/update_personnel', methods=['GET', 'POST'])
@login_required
@staff_only
def update_personnel():
    if request.form['pk'] >= 4000:
        t,a,k = 'Faculty','fname', 'fid'
    else:
        t,a,k = 'Staff', 'sname', 'sid'
    print t, a
    try:
        c.execute("UPDATE {0} SET {1} = '{2}' WHERE {3} = {4}"
                  .format(t,a,request.form['value'],k,request.form['pk'])) 
        db.commit()
    except cx_Oracle.DatabaseError as ex:
        error, = ex.args
        print "DB Error: {0} - {1}".format(error.code, error.message)
        db.rollback()
        return Response(status=400)
        
    return Response('updated person name',status=200)
        
