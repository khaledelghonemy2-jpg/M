import os,sys
os.environ["LOCALAPPDATA"]=sys.argv[1]
os.environ.pop("TURSO_AUTH_TOKEN",None)
sys.path.insert(0,sys.argv[2])
import ALLOCATE_PRO as ap
assert not ap.CLOUD_ENABLED, "cloud must be off for tests"
ap.init_db()
from ap import *
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
print("ALL TESTS PASSED")
