from sqlalchemy import create_engine, text
import credentials
engine = create_engine(credentials.produrl, echo=False)

query = text("""
SELECT exe.project, se.job_name, exe.date_completed - exe.date_started, date_completed

FROM public.scheduled_execution se
join public.execution exe on exe.scheduled_execution_id=se.id

where exe.status='succeeded'
and exe.date_completed >= CURRENT_DATE - 28
group by se.job_name, exe.project, exe.date_started, exe.date_completed
order by se.job_name
""")

times = engine.execute(query)
timing = []
for x in times:
    timing.append(x)
avgtable = []
numprojects = 0
i = 0
j = 0
while i < len(timing)-1:
    summ=0
    count = 0
    avg = 0
    while timing[i][1] == timing[i+1][1] and i < len(timing)-2:
        summ += timing[i][2].total_seconds()
        count += 1
        i+=1
    summ += timing[i][2].total_seconds()
    avg = summ / (count + 1)
    avgtable.append([timing[i][1], avg])
    i += 1
    numprojects += 1

query1 = text("""
SELECT exe.project, se.job_name, exe.date_completed - exe.date_started, cast(date_completed as varchar(16))

FROM public.scheduled_execution se
join public.execution exe on exe.scheduled_execution_id=se.id

where exe.status='succeeded'
and exe.date_completed >= CURRENT_DATE - 7
group by se.job_name, exe.project, exe.date_started, exe.date_completed
order by se.job_name
""")
thisweek = engine.execute(query1)
weekcheck = []
for x in thisweek:
    weekcheck.append(x)

toolong = []
for g in weekcheck:
    for m in avgtable:
        if g[1] == m[0]:
            if g[2].total_seconds() > m[1]*5:
                toolong.append([g[0], m[0], g[3], round(g[2].total_seconds()), round(m[1], 1)])

over = 1 
j=0  
while j < len(toolong) - 1:
    if toolong[j][1] != toolong[j+1][1]:
        over += 1
    j += 1
if len(toolong)==0:
    over = 0
#-----------------------------------------------------------------------------

engineqa = create_engine(credentials.qaurl, echo=False)
timesqa = engineqa.execute(query)
timingqa = []
for x in timesqa:
    timingqa.append(x)
avgtableqa = []
numprojects = 0
i = 0
j = 0
while i < len(timingqa)-1:
    summ=0
    count = 0
    avg = 0
    while timingqa[i][1] == timingqa[i+1][1] and i < len(timingqa)-2:
        summ += timingqa[i][2].total_seconds()
        count += 1
        i+=1
    summ += timingqa[i][2].total_seconds()
    avg = summ / (count + 1)
    avgtableqa.append([timingqa[i][1], avg])
    i += 1
    numprojects += 1

thisweekqa = engineqa.execute(query1)
weekcheckqa = []
for x in thisweekqa:
    weekcheckqa.append(x)

toolongqa = []
for g in weekcheckqa:
    for m in avgtableqa:
        if g[1] == m[0]:
            if g[2].total_seconds() > m[1]*5:
                toolongqa.append([g[0], m[0], g[3], round(g[2].total_seconds()), round(m[1], 1)])

overqa = 1 
j=0  
while j < len(toolongqa) - 1:
    if toolongqa[j][1] != toolongqa[j+1][1]:
        overqa += 1
    j += 1
if len(toolongqa)==0:
    overqa = 0
#-----------------------------------------------------------------------------

enginestag = create_engine(credentials.stagurl, echo=False)
timesstag = enginestag.execute(query)
timingstag = []
for x in timesstag:
    timingstag.append(x)
avgtablestag = []
numprojects = 0
i = 0
j = 0
while i < len(timingstag)-1:
    summ=0
    count = 0
    avg = 0
    while timingstag[i][1] == timingstag[i+1][1] and i < len(timingstag)-2:
        summ += timingstag[i][2].total_seconds()
        count += 1
        i+=1
    summ += timingstag[i][2].total_seconds()
    avg = summ / (count + 1)
    avgtablestag.append([timingstag[i][1], avg])
    i += 1
    numprojects += 1

thisweekstag = enginestag.execute(query1)
weekcheckstag = []
for x in thisweekstag:
    weekcheckstag.append(x)

toolongstag = []
for g in weekcheckstag:
    for m in avgtablestag:
        if g[1] == m[0]:
            if g[2].total_seconds() > m[1]*5:
                toolongstag.append([g[0], m[0], g[3], round(g[2].total_seconds()), round(m[1], 1)])

overstag = 1 
j=0  
while j < len(toolongstag) - 1:
    if toolongstag[j][1] != toolongstag[j+1][1]:
        overstag += 1
    j += 1
if len(toolongstag)==0:
    overstag = 0
#-----------------------------------------------------------------------------

enginetest = create_engine(credentials.testurl, echo=False)
timestest = enginetest.execute(query)
timingtest = []
for x in timestest:
    timingtest.append(x)
avgtabletest = []
numprojects = 0
i = 0
j = 0
while i < len(timingtest)-1:
    summ=0
    count = 0
    avg = 0
    while timingtest[i][1] == timingtest[i+1][1] and i < len(timingtest)-2:
        summ += timingtest[i][2].total_seconds()
        count += 1
        i+=1
    summ += timingtest[i][2].total_seconds()
    avg = summ / (count + 1)
    avgtabletest.append([timingtest[i][1], avg])
    i += 1
    numprojects += 1

thisweektest = enginetest.execute(query1)
weekchecktest = []
for x in thisweektest:
    weekchecktest.append(x)

toolongtest = []
for g in weekchecktest:
    for m in avgtabletest:
        if g[1] == m[0]:
            if g[2].total_seconds() > m[1]*5:
                toolongtest.append([g[0], m[0], g[3], round(g[2].total_seconds()), round(m[1], 1)])

overtest = 1 
j=0  
while j < len(toolongtest) - 1:
    if toolongtest[j][1] != toolongtest[j+1][1]:
        overtest += 1
    j += 1
if len(toolongtest)==0:
    overtest = 0