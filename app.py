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
    execution_type = Column(String)

    def __init__(self, id, project, status, date_completed, scheduled_execution_id):
        self.id = id
        self.project = project
        self.status = status
        self.date_completed = date_completed
        self.scheduled_execution_id = scheduled_execution_id
        self.execution_type = execution_type

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


job = session.query(Execution.project, Jobs.job_name, Execution.status, Execution.execution_type).filter(Execution.scheduled_execution_id == Jobs.id).filter_by(status='failed').order_by(Execution.date_completed.desc()).limit(10)

query = text("""select project, count (*)
from public.execution
where date_completed >= CURRENT_DATE
group by execution.project
""")
titles = engine.execute(query)
executions = []
for y in titles:
    executions.append(y)

query2 = text("""select project, count (*)
from public.execution
where status='failed' and date_completed >= CURRENT_DATE
group by execution.project
""")

faillist = engine.execute(query2)
failures = []
for k in faillist:
    failures.append(k)

#build url
g = 0
host = "devops"

while g < len(failures):
    project = failures[g][0]
    url = "http://{0}.equinoxfitness.com/rundeck/project/{1}/activity?statFilter=fail".format(host, project)
    failures[g] = failures[g], url
    g += 1

query3 = text("""
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
counts = engine.execute(query3)
failcount = []
for x in counts:
    failcount.append(x)

query4 = text("""
select date_completed, count(*)
from (
select CAST(date_completed as date)
from public.execution
where status = 'failed' 
and date_completed >= CURRENT_DATE - 6
group by execution.date_completed
)as x
group by x.date_completed
order by count desc
""")
days = engine.execute(query4)
week = []
for k in days:
    week.append(k)

query6 = text("""
SELECT 
       exe.date_started,
       exe.project,
       se.job_name
FROM public.scheduled_execution se
join public.execution exe on exe.scheduled_execution_id=se.id
where exe.date_completed is null
order by date_started desc
""")
ongoing = engine.execute(query6)
running = []
for y in ongoing:
    running.append(y)




@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', titles=executions, job=job, counts=failcount, failures=failures, running=running, week=week)


if __name__ == '__main__':
	app.run(debug=True)
    