from flask import Flask, render_template, request
from pusher import Pusher
from sqlalchemy import Column, String, Date, Integer, cast, func, text
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
    scheduled_execution_id = Column(Integer)

    def __init__(self, id, project, status, date_completed, scheduled_execution_id):
        self.id = id
        self.project = project
        self.status = status
        self.date_completed = date_completed
        self.scheduled_execution_id = scheduled_execution_id

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
app_id=credentials.id,
key=credentials.key,
secret=credentials.secret,
cluster=credentials.cluster,
ssl=True)

#sql variables
allprojects = session.query(Execution.project).filter(cast(Execution.date_completed, Date)==date.today()).subquery()
fails = session.query(Execution.project).filter_by(status='failed').filter(cast(Execution.date_completed, Date)==date.today()).subquery()

ad_runs = session.query(allprojects).filter_by(project='Admin').count()
ad_fails = session.query(fails).filter_by(project='Admin').count()
j_runs = session.query(allprojects).filter_by(project='Jarvis').count()
j_fails = session.query(fails).filter_by(project='Jarvis').count()
k_runs = session.query(allprojects).filter_by(project='Kraken').count()
k_fails = session.query(fails).filter_by(project='Kraken').count()
p_runs = session.query(allprojects).filter_by(project='Perry').count()
p_fails = session.query(fails).filter_by(project='Perry').count()
cache_runs = session.query(allprojects).filter_by(project='Cache_Jobs').count()
cache_fails = session.query(fails).filter_by(project='Cache_Jobs').count()
app_runs = session.query(allprojects).filter_by(project='App-Integrations').count()
app_fails = session.query(fails).filter_by(project='App-Integrations').count()
mp_runs = session.query(allprojects).filter_by(project='MemberProfile').count()
mp_fails = session.query(fails).filter_by(project='MemberProlie').count()
d_runs = session.query(allprojects).filter_by(project='Deployment').count()
d_fails = session.query(fails).filter_by(project='Deployment').count()
bus_runs = session.query(allprojects).filter_by(project='BusinessSystems').count()
bus_fails = session.query(fails).filter_by(project='BusinessSystems').count()
jb_runs = session.query(allprojects).filter_by(project='Jarvis-Blink').count()
jb_fails = session.query(fails).filter_by(project='Jarvis-Blink').count()

job = session.query(Execution.project, Jobs.job_name, Execution.status).filter(Execution.scheduled_execution_id == Jobs.id).filter_by(status='failed').order_by(Execution.date_completed.desc()).limit(10)

query = text("""
select project,job_name,status,count(*) from

(SELECT
exe.project,
se.job_name,
exe.status

FROM public.scheduled_execution se
join public.execution exe on exe.scheduled_execution_id=se.id
where exe.date_completed >= CURRENT_DATE -6
) as his

where status = 'failed'
group by status, job_name, project
order by count DESC
limit(10)
""")
counts = engine.execute(query)
failcount = []
for x in counts:
    failcount.append(x)

query2 = text("""
SELECT 
       exe.date_started,
       exe.project,
       se.job_name
FROM public.scheduled_execution se
join public.execution exe on exe.scheduled_execution_id=se.id
where exe.date_completed is null
order by date_started desc
""")
ongoing = engine.execute(query2)
running = []
for y in ongoing:
    running.append(y)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', ad_runs=ad_runs, ad_fails=ad_fails, j_runs=j_runs, j_fails=j_fails, k_runs=k_runs, k_fails=k_fails, 
	p_runs=p_runs, p_fails=p_fails, cache_runs=cache_runs, cache_fails=cache_fails, app_runs=app_runs, app_fails=app_fails, mp_runs=mp_runs, 
	mp_fails=mp_fails, d_runs=d_runs, d_fails=d_fails, bus_runs=bus_runs, bus_fails=bus_fails, jb_runs=jb_runs, jb_fails=jb_fails, job=job, counts=failcount, running=running)

if __name__ == '__main__':
	app.run(debug=True)
    