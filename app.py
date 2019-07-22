from flask import Flask, render_template, request
from sqlalchemy import create_engine, text
import credentials

app = Flask(__name__)

@app.route('/dashboard/prod')
def dashboard():
    engine = create_engine(credentials.rundeckdb, echo=False)
        
    #recently failed jobs table
    query1 = text("""
    SELECT
    exe.project,
    se.job_name,
    exe.status,
    exe.execution_type

    FROM public.scheduled_execution se
    join public.execution exe on exe.scheduled_execution_id=se.id
    where exe.status='failed'
    order by exe.date_completed desc
    limit 10 """)
    recents = engine.execute(query1)
    job = []
    for w in recents:
        job.append(w)

    #number executions per project (card)
    query = text("""select project, count (*)
    from public.execution
    where date_completed >= CURRENT_DATE
    group by execution.project
    """)
    titles = engine.execute(query)
    executions = []
    for y in titles:
        executions.append(y)

    #number fails per project (card)
    query2 = text("""select project, count (*)
    from public.execution
    where status='failed' and date_completed >= CURRENT_DATE
    group by execution.project
    """)
    faillist = engine.execute(query2)
    failures = []
    for k in faillist:
        failures.append(k)

    #number fails per job for the week table
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

    #finds the day with the most failures
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

    length = len(week)

    #shows currently running jobs
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

    #build prod url
    g = 0
    host = "devops"
    while g < len(failures):
        project = failures[g][0]
        url = "http://{0}.equinoxfitness.com/rundeck/project/{1}/activity?statFilter=fail".format(host, project)
        failures[g] = failures[g], url
        g += 1
        
    return render_template('dashboard.html', engine=engine, titles=executions, job=job, counts=failcount, failures=failures, running=running, week=week, length=length)

@app.route('/dashboard/qa')
def qa():
    engineqa = create_engine(credentials.qaurl, echo=False)
    #recently failed jobs table
    query1 = text("""
    SELECT
    exe.project,
    se.job_name,
    exe.status,
    exe.execution_type

    FROM public.scheduled_execution se
    join public.execution exe on exe.scheduled_execution_id=se.id
    where exe.status='failed'
    order by exe.date_completed desc
    limit 10 """)
    recents = engineqa.execute(query1)
    jobqa = []
    for w in recents:
        jobqa.append(w)

    #number executions per project (card)
    query = text("""select project, count (*)
    from public.execution
    where date_completed >= CURRENT_DATE
    group by execution.project
    """)
    titles = engineqa.execute(query)
    executionsqa = []
    for y in titles:
        executionsqa.append(y)

    #number fails per project (card)
    query2 = text("""select project, count (*)
    from public.execution
    where status='failed' and date_completed >= CURRENT_DATE
    group by execution.project
    """)
    faillist = engineqa.execute(query2)
    failuresqa = []
    for k in faillist:
        failuresqa.append(k)

    #number fails per job for the week table
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
    counts = engineqa.execute(query3)
    failcountqa = []
    for x in counts:
        failcountqa.append(x)

    #finds the day with the most failures
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
    days = engineqa.execute(query4)
    weekqa = []
    for k in days:
        weekqa.append(k)

    lengthqa = len(weekqa)

    #shows currently running jobs
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
    ongoing = engineqa.execute(query6)
    runningqa = []
    for y in ongoing:
        runningqa.append(y)

    #build qa url
    g = 0
    host = "qa-devops"
    while g < len(failuresqa):
        project = failuresqa[g][0]
        url = "http://{0}.equinoxfitness.com/rundeck/project/{1}/activity?statFilter=fail".format(host, project)
        failuresqa[g] = failuresqa[g], url
        g += 1

    return render_template('qa.html', titles=executionsqa, job=jobqa, counts=failcountqa, failures=failuresqa, running=runningqa, week=weekqa, length=lengthqa)

@app.route('/dashboard/stag')
def stag():
    enginestag = create_engine(credentials.stagurl, echo=False)
    #recently failed jobs table
    query1 = text("""
    SELECT
    exe.project,
    se.job_name,
    exe.status,
    exe.execution_type

    FROM public.scheduled_execution se
    join public.execution exe on exe.scheduled_execution_id=se.id
    where exe.status='failed'
    order by exe.date_completed desc
    limit 10 """)
    recents = enginestag.execute(query1)
    jobstag = []
    for w in recents:
        jobstag.append(w)

    #number executions per project (card)
    query = text("""select project, count (*)
    from public.execution
    where date_completed >= CURRENT_DATE
    group by execution.project
    """)
    titles = enginestag.execute(query)
    executionsstag = []
    for y in titles:
        executionsstag.append(y)

    #number fails per project (card)
    query2 = text("""select project, count (*)
    from public.execution
    where status='failed' and date_completed >= CURRENT_DATE
    group by execution.project
    """)
    faillist = enginestag.execute(query2)
    failuresstag = []
    for k in faillist:
        failuresstag.append(k)

    #number fails per job for the week table
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
    counts = enginestag.execute(query3)
    failcountstag = []
    for x in counts:
        failcountstag.append(x)

    #finds the day with the most failures
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
    days = enginestag.execute(query4)
    weekstag = []
    for k in days:
        weekstag.append(k)

    lengthstag = len(weekstag)

    #shows currently running jobs
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
    ongoing = enginestag.execute(query6)
    runningstag = []
    for y in ongoing:
        runningstag.append(y)

    #build stag url
    g = 0
    host = "stag-devops"
    while g < len(failuresstag):
        project = failuresstag[g][0]
        url = "http://{0}.equinoxfitness.com/rundeck/project/{1}/activity?statFilter=fail".format(host, project)
        failuresstag[g] = failuresstag[g], url
        g += 1

    return render_template('stag.html', titles=executionsstag, job=jobstag, counts=failcountstag, failures=failuresstag, running=runningstag, week=weekstag, length=lengthstag)

@app.route('/dashboard/test')
def test():
    enginetest = create_engine(credentials.testurl, echo=False)
    #recently failed jobs table
    query1 = text("""
    SELECT
    exe.project,
    se.job_name,
    exe.status,
    exe.execution_type

    FROM public.scheduled_execution se
    join public.execution exe on exe.scheduled_execution_id=se.id
    where exe.status='failed'
    order by exe.date_completed desc
    limit 10 """)
    recents = enginetest.execute(query1)
    jobtest = []
    for w in recents:
        jobtest.append(w)

    #number executions per project (card)
    query = text("""select project, count (*)
    from public.execution
    where date_completed >= CURRENT_DATE
    group by execution.project
    """)
    titles = enginetest.execute(query)
    executionstest = []
    for y in titles:
        executionstest.append(y)

    #number fails per project (card)
    query2 = text("""select project, count (*)
    from public.execution
    where status='failed' and date_completed >= CURRENT_DATE
    group by execution.project
    """)
    faillist = enginetest.execute(query2)
    failurestest = []
    for k in faillist:
        failurestest.append(k)

    #number fails per job for the week table
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
    counts = enginetest.execute(query3)
    failcounttest = []
    for x in counts:
        failcounttest.append(x)

    #finds the day with the most failures
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
    days = enginetest.execute(query4)
    weektest = []
    for k in days:
        weektest.append(k)

    lengthtest = len(weektest)

    #shows currently running jobs
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
    ongoing = enginetest.execute(query6)
    runningtest = []
    for y in ongoing:
        runningtest.append(y)

    #build test url
    g = 0
    host = "test-devops"
    while g < len(failurestest):
        project = failurestest[g][0]
        url = "http://{0}.equinoxfitness.com/rundeck/project/{1}/activity?statFilter=fail".format(host, project)
        failurestest[g] = failurestest[g], url
        g += 1

    return render_template('test.html', titles=executionstest, job=jobtest, counts=failcounttest, failures=failurestest, running=runningtest, week=weektest, length=lengthtest)

if __name__ == '__main__':
	app.run(debug=True)