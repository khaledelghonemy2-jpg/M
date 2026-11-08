import os,sys
os.environ["LOCALAPPDATA"]=sys.argv[1]
os.environ.pop("TURSO_AUTH_TOKEN",None)
sys.path.insert(0,sys.argv[2])
import ALLOCATE_PRO as ap
assert not ap.CLOUD_ENABLED, "cloud must be off for tests"
ap.init_db()
from ALLOCATE_PRO import *
set_week_dates_batch({"Week 1":"2026-09-20","Week 2":"2026-09-27","Week 3":"2026-10-04","Week 4":"2026-10-11","Week 5":"2026-10-18","Week 6":"2026-10-25"})
add_worker("Ann"); add_client("Bob")
for wk in WEEKS: set_worker_wage("Ann",wk,1000)
# 1. rates by week
assert abs(allocation_cost(1,"Weekday",week="Week 1")-41.82)<1e-9
assert abs(allocation_cost(1,"Weekday",week="Week 3")-43.91)<1e-9
assert abs(allocation_cost(1,"Weekday","Ann",week="Week 1")-41.82)<1e-9
print("rates by week ok")
# 2. chain planner uses week rates; capacity matches save cost
set_client_estimate("Bob","Week 1","Weekday",100)
set_chain("Bob",["Ann"])
plan,short=plan_chain_allocation("Bob",["Week 1"])
h=plan[0][3]; assert abs(h*41.82-1000)<1e-6, h
save_allocations_batch([(wk,w,"Bob",cat,hrs,day,"","","") for wk,w,cat,hrs,day in plan])
assert abs(worker_wage_left("Ann","Week 1"))<1e-6, worker_wage_left("Ann","Week 1")
print("chain plan ok",round(h,3),"h; shortfall",short)
# 3. auto estimate follows bulk delete
a1=save_allocation_atomic("Week 2","Ann","Bob","Saturday",5,"Saturday")
a2=save_allocation_atomic("Week 2","Ann","Bob","Saturday",3,"Saturday")
assert get_client_estimate("Bob","Week 2","Saturday")==8
delete_allocations_batch([a1])
assert get_client_estimate("Bob","Week 2","Saturday")==3, get_client_estimate("Bob","Week 2","Saturday")
print("bulk delete estimate sync ok")
# 4. legacy edit is in place, keeps times, moves estimate
set_allocation_times(a2,"09:00","12:00")
nid=edit_allocation(a2,4,day="Sunday",category="Sunday")
assert nid==a2 and get_allocation_times(a2)==("09:00","12:00")
assert get_client_estimate("Bob","Week 2","Saturday")==0 and get_client_estimate("Bob","Week 2","Sunday")==4
print("legacy edit ok")
# 5. typed estimate never overwritten
set_client_estimate("Bob","Week 4","Weekday",10)
save_allocation_atomic("Week 4","Ann","Bob","Weekday",12)
assert get_client_estimate("Bob","Week 4","Weekday")==10
print("typed plan protected ok")
# 6. rename keeps notes
note_add("worker","Ann","great","me"); note_add("client","Bob","vip","me")
rename_worker("Ann","Anna"); rename_client("Bob","Bobby")
rows=load_notes_rows()
assert any(r[1]=="worker" and r[2]=="Anna" for r in rows) and any(r[1]=="client" and r[2]=="Bobby" for r in rows)
print("rename keeps notes ok")
# 7. login
create_user("khaled","pw123")
assert verify_user(" khaled ","pw123")=="manager" and verify_user("khaled","nope") is None
print("login ok")
print("est reconcile W1 $",est_reconcile_dollars("Bobby","Week 1","Weekday")[0])
# 8. roster: CareMile shifts with no allocation become dashed "ghosts"
import types
import ALLOCATE_PRO as _ap
snap={"clients":["Pine Lodge","Harbour View"],"cmv_info":[
  (1,"Week 1","Tom","Tom","2026-09-15","Tuesday","Pine Lodge-CO-CM017","care",3,"09:00","12:00","approved"),   # not allocated -> ghost
  (2,"Week 1","Tom","Tom","2026-09-16","Wednesday","Pine Lodge-CO-CM017","care",2,"09:00","11:00","approved"), # allocated -> none
  (3,"Week 1","Tom","Tom","2026-09-17","Thursday","Harbour View-CO-CM9","care",6,"08:00","14:00","approved"),  # 4h allocated -> 2h ghost 12-14
  (4,"Week 1","Tom","Tom","2026-09-18","Friday","Pine Lodge-CO-CM017","care",5,"08:00","13:00","Cancelled"),   # cancelled -> none
  (5,"Week 2","Tom","Tom","2026-09-22","Tuesday","Pine Lodge-CO-CM017","care",3,"09:00","12:00","approved")]} # other week -> none
week_rows=[(1,"Week 1","Tom","Pine Lodge","Weekday",2,0,0,"Wednesday","","","","09:00","11:00"),
           (2,"Week 1","Tom","Harbour View","Weekday",4,0,0,"Thursday","","","","08:00","12:00")]
fake=types.SimpleNamespace(_snapshot=snap,_week_rows=lambda:week_rows,_CMV_SKIP_STATUS=_ap.App._CMV_SKIP_STATUS)
g=_ap.App._roster_cmv_ghosts(fake,"Week 1")
got=sorted((x["day"],x["client"],x["hours"],x["start"],x["end"],x["partial"]) for x in g)
assert got==[("Thursday","Harbour View",2.0,"12:00","14:00",True),("Tuesday","Pine Lodge",3.0,"09:00","12:00",False)], got
print("roster CareMile ghosts ok")
# 9. CareMile client names resolve to ONE client, or none when unsure (Monday auto-import)
cl=["Client 05 Jones","Client 15 Jones","Stephanie","Hava","Sarah Ali","Sarah Brown","Wafaa"]
R=_ap.cmv_resolve_client
assert R("Client 05 Jones-CO-CM001",cl)=="Client 05 Jones"
assert R("Stephanie Pickett-CO-CM017",cl)=="Stephanie"
assert R("Havva Cokacar-CO-CM025",cl)=="Hava"
assert R("Sarah Smith-CO-CM1",cl) is None          # two Sarahs: never guess
assert R("Nobody Here-CO-CM9",cl) is None
print("CareMile client resolving ok")
# 10. Client guide: formulas from the guide sheet, weekly hours and profit at its rates
P=_ap._guide_parse_hours
assert P("=8.5*((5*4)+2)",187)==(8.5,5.0) and P("=8*4",32)==(8.0,1.0) and P("=(6*(3*4))-4.5",67.5)==(6.0,3.0) and P("=SUM(G4:G8)",1)==(None,None)
g={"cats":{"Weekday":{"per_day":8.5,"days_week":5,"month":187},"Saturday":{"per_day":8,"days_week":1,"month":32},
           "Sunday":{"per_day":8,"days_week":1,"month":32},"Public Holiday":{"month":0}},"discount":1,"budget_month":19000}
assert _ap.guide_week_hours(g,"Weekday")==42.5
m=_ap.guide_money(g,"Week 1")      # Week 1 ends 20 Sep 2026 -> old rates, like the guide sheet
assert abs(m["cost"]-12096.82)<0.01 and abs(m["invoice"]-20122.33)<0.01 and abs(m["markup"]-66.34)<0.01, m
print("client guide maths ok")
# 11. Paste shifts: the real message format (worker's total with client, "Days:", "from X till Y", two shifts on one line)
msg="""Mike's Total amount with Regan = $1064.10
Days:
Monday from 8PM till 10PM
Sunday from 10AM till 4PM, And from 7PM till 9PM

Khaled's Total amount with Regan = $923.64
Days:
Saturday from 6AM till 8PM
Anisa - Tue 9-1 Regan
Development@CareMile"""
dates={wk:d for wk,d in zip(_ap.WEEKS,["2026-09-20","2026-09-27","2026-10-04","2026-10-11","2026-10-18","2026-10-25"])}
rows=_ap.parse_shift_message(msg,["Mike","Khaled","Anisa Haddad"],["Regan","Stephanie"],"Week 1",dates)
got=[(r["worker"],r["client"],r["day"],r["start"],r["end"],r["hours"],r["category"],r["issue"]) for r in rows]
assert got==[("Mike","Regan","Monday","20:00","22:00",2.0,"Weekday",""),("Mike","Regan","Sunday","10:00","16:00",6.0,"Sunday",""),
             ("Mike","Regan","Sunday","19:00","21:00",2.0,"Sunday",""),("Khaled","Regan","Saturday","06:00","20:00",14.0,"Saturday",""),
             ("Anisa Haddad","Regan","Tuesday","09:00","13:00",4.0,"Weekday","")], got
assert rows[0]["block_total"]==1064.10 and rows[3]["block_total"]==923.64
print("paste shifts ok")
print("ALL TESTS PASSED")
