import sqlite3
#from playertest import VideoMain

conn = sqlite3.connect('video.db')

c = conn.cursor()

#c.execute("""CREATE TABLE videos (
   #         directory text,
  #          object1 text,
 #           object2 text
 #           )""")


def insert_emp(direc,obj1,obj2):
    with conn:
        c.execute("SELECT * FROM videos WHERE directory=:directory", {'directory': direc})
        if c.fetchall()==[]:
            c.execute("INSERT INTO videos VALUES (:directory, :object1, :object2)", {'directory': direc, 'object1': obj1, 'object2': obj2})



def get_emps_by_directory(thedirectory):
    c.execute("SELECT * FROM videos WHERE directory=:directory", {'directory': thedirectory})
    return c.fetchall()

def get_emps_by_obj1(theobject):
    c.execute("SELECT * FROM videos WHERE object1=:object1", {'object1': theobject})
    return c.fetchall()

def get_emps_by_obj2(theobject):
    c.execute("SELECT * FROM videos WHERE object2=:object2", {'object2': theobject})
    return c.fetchall()



def remove_emp(thedirectory):
    with conn:
        c.execute("DELETE from videos WHERE directory = :directory",{'directory': thedirectory})
                  

conn.commit()
