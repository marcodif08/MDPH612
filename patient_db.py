import psycopg2

DATABASE = "patient_db"
USER = "postgres"
PASSWORD = "mdph612M"
HOST = "127.0.0.1"
PORT = "5432"

#CREATE DATABASES

#Create patient database containing name, ROI, strcture file path, beam file path, gif file path
def create_patient_db(cur):
    cur.execute("DROP TABLE IF EXISTS PATIENT CASCADE")
    cur.execute('''CREATE TABLE PATIENT (
          PATIENTID INT PRIMARY KEY     NOT NULL,
          PNAME           TEXT    NOT NULL,
          ROI      TEXT     NOT NULL,
          FULLPATHS            TEXT     NOT NULL,
          FULLPATHB            TEXT     NOT NULL,
          FULLPATHG            TEXT     NOT NULL);''')


#INSERT DATABASES

def fill_db(cur):
    #Patient information
    patients_list = [
            [1, 'Patient 1', 'Abdomen','./Abdomen/RS.PYTIM05_.dcm','./Abdomen/RP.PYTIM05_PS2.dcm','./static/images/Abdomen.gif'],
            [2, 'Patient 2', 'ENT', './ENT/RS.1.2.246.352.71.4.2088656855.2401823.20110920093221.dcm', './ENT/RP.1.2.246.352.71.5.2088656855.377514.20110921073559.dcm','./static/images/ENT.gif'],
            [3, 'Patient 3', 'Prostate','./Prostate/RS.1.2.246.352.71.4.2088656855.2404649.20110920153449.dcm','./Prostate/RP.1.2.246.352.71.5.2088656855.377401.20110920153647.dcm','./static/images/Prostate.gif'],

        ]


    try:
        for row in patients_list:
            cur.execute("INSERT INTO PATIENT (PATIENTID,PNAME,ROI,FULLPATHS,FULLPATHB,FULLPATHG) \
                VALUES (%i, '%s', '%s', '%s', '%s', '%s')"%(row[0],row[1],row[2],row[3],row[4],row[5]))
    except Exception as e:
        print (e)

#DISPLAY DATABASES
def read_db(cur, table):
    cur.execute('SELECT * FROM %s'%table)
    rows = cur.fetchall()
    for row in rows:
        print (row)

def main():
    # Open Database
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    print("Database opened successfully")
    cur = con.cursor()

    # Create Database Tables
    create_patient_db(cur)

    # Insert data to tables
    fill_db(cur)
    con.commit()

if __name__ == "__main__":
    main()
