from flask import Flask, request, render_template
import psycopg2

DATABASE = "patient_db"
USER = "postgres"
PASSWORD = "mdph612M"
HOST = "127.0.0.1"
PORT = "5432"

app = Flask(__name__, template_folder='templates')

@app.route('/')
def start():
    return redirect('http://127.0.0.1:5000/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #goes to form in the index.html file to see what the drop down menu is currently selecting
        current_roi = request.form.get('rois')
        if current_roi != "None":
            query_img = """SELECT FULLPATHG FROM PATIENT WHERE ROI='%s'"""%(current_roi)
            conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
            cur = conn.cursor()
            cur.execute(query_img)
            results_img = cur.fetchall()

        else:
            results_img = []

        #gif file path
        full_filename = results_img[0][0]
        return render_template("index.html", user_image = full_filename, ROI = current_roi)

    return render_template("index.html", user_image = './static/images/Abdomen.gif', ROI = 'Abdomen')

app.run()
