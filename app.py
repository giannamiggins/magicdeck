from flask import Flask, render_template, request
from pusher import Pusher
from sqlalchemy import Column, String, Date, Integer, cast, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, mapper
from sqlalchemy import create_engine, Table, MetaData, text
from datetime import date, timedelta
import credentials
today = date.today()

app = Flask(__name__)
engine = create_engine(credentials.rundeckdb, echo=False)
Base = declarative_base(engine)

metadata = Base.metadata
Session = sessionmaker(bind=engine)
session = Session()

class Execution(Base):
    __tablename__ = "execution"

    id = Column(Integer, primary_key=True)
    project = Column(String)
    status = Column(String)
    date_completed = Column(Date)

    def __init__(self, id, project, status, date_completed):
        self.id = id
        self.project = project
        self.status = status
        self.date_completed = date_completed

class Jobs(Base):
    __tablename__ = "scheduled_execution"

    id = Column(Integer, primary_key=True)
    project = Column(String)
    job_name = Column(String)
    last_updated = Column(String)

    def __init__(self, id, project, job_name, last_updated):
        self.id = id
        self.project = project
        self.job_name = job_name
        self.last_updated = last_updated


# configure pusher object
pusher = Pusher(
app_id="819028",
key="dcf23db54c14bbf4de21",
secret="392db480872378769d1f",
cluster="us2",
ssl=True)

#sql variables
ad_runs = session.query(Execution.project).filter_by(project='Admin').filter(cast(Execution.date_completed, Date)==date.today()).count()
ad_fails = session.query(Execution.project).filter_by(status='failed').filter_by(project='Admin').filter(cast(Execution.date_completed, Date)==date.today()).count()
j_runs = session.query(Execution.project).filter_by(project='Jarvis').filter(cast(Execution.date_completed, Date)==date.today()).count()
j_fails = session.query(Execution.project).filter_by(status='failed').filter_by(project='Jarvis').filter(cast(Execution.date_completed, Date)==date.today()).count()
k_runs = session.query(Execution.project).filter_by(project='Kraken').filter(cast(Execution.date_completed, Date)==date.today()).count()
k_fails = session.query(Execution.project).filter_by(status='failed').filter_by(project='Kraken').filter(cast(Execution.date_completed, Date)==date.today()).count()
p_runs = session.query(Execution.project).filter_by(project='Perry').filter(cast(Execution.date_completed, Date)==date.today()).count()
p_fails = session.query(Execution.project).filter_by(status='failed').filter_by(project='Perry').filter(cast(Execution.date_completed, Date)==date.today()).count()
cache_runs = session.query(Execution.project).filter_by(project='Cache_Execution').filter(cast(Execution.date_completed, Date)==date.today()).count()
cache_fails = session.query(Execution.project).filter_by(status='failed').filter_by(project='Cache_Execution').filter(cast(Execution.date_completed, Date)==date.today()).count()
app_runs = session.query(Execution.project).filter_by(project='App-Integrations').filter(cast(Execution.date_completed, Date)==date.today()).count()
app_fails = session.query(Execution.project).filter_by(status='failed').filter_by(project='App-Integrations').filter(cast(Execution.date_completed, Date)==date.today()).count()
mp_runs = session.query(Execution.project).filter_by(project='MemberProfile').filter(cast(Execution.date_completed, Date)==date.today()).count()
mp_fails = session.query(Execution.project).filter_by(status='failed').filter_by(project='MemberProlie').filter(cast(Execution.date_completed, Date)==date.today()).count()
d_runs = session.query(Execution.project).filter_by(project='Deployment').filter(cast(Execution.date_completed, Date)==date.today()).count()
d_fails = session.query(Execution.project).filter_by(status='failed').filter_by(project='Deployment').filter(cast(Execution.date_completed, Date)==date.today()).count()
bus_runs = session.query(Execution.project).filter_by(project='BusinessSystems').filter(cast(Execution.date_completed, Date)==date.today()).count()
bus_fails = session.query(Execution.project).filter_by(status='failed').filter_by(project='BusinessSystems').filter(cast(Execution.date_completed, Date)==date.today()).count()
jb_runs = session.query(Execution.project).filter_by(project='Jarvis-Blink').filter(cast(Execution.date_completed, Date)==date.today()).count()
jb_fails = session.query(Execution.project).filter_by(status='failed').filter_by(project='Jarvis-Blink').filter(cast(Execution.date_completed, Date)==date.today()).count()

proj = session.query(Execution.project).filter_by(status='failed').order_by(Execution.date_completed.desc()).limit(10)
stat = session.query(Execution.status).filter_by(status='failed').order_by(Execution.date_completed.desc()).limit(10)

perry = session.query(Jobs.job_name).filter_by(project='Perry').order_by(Jobs.last_updated.desc()).limit(3)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', ad_runs=ad_runs, ad_fails=ad_fails, j_runs=j_runs, j_fails=j_fails, k_runs=k_runs, k_fails=k_fails, 
	p_runs=p_runs, p_fails=p_fails, cache_runs=cache_runs, cache_fails=cache_fails, app_runs=app_runs, app_fails=app_fails, mp_runs=mp_runs, 
	mp_fails=mp_fails, d_runs=d_runs, d_fails=d_fails, bus_runs=bus_runs, bus_fails=bus_fails, jb_runs=jb_runs, jb_fails=jb_fails, 
	list_fails="projects to be named", proj=proj, stat=stat, perry=perry)

@app.route('/orders', methods=['POST'])
def order():
    data = request.form
    pusher.trigger(u'order', u'place', {
            u'units': data['units']
        })
    return "units logged"

@app.route('/message', methods=['POST'])
def message():
    data = request.form
    pusher.trigger(u'message', u'send', {
            u'name': data['name'],
            u'message': data['message']
        })
    return "message sent"

@app.route('/customer', methods=['POST'])
def customer():
    data = request.form
    pusher.trigger(u'customer', u'add', {
            u'name': data['name'],
            u'position': data['position'],
            u'office': data['office'],
            u'age': data['age'],
            u'salary': data['salary'],
        })
    return "customer added"


if __name__ == '__main__':
	app.run(debug=True)
    