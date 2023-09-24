import eel
from empStats import EmployeeStats
from alerts_class import late_alerts
performance_id = None 
Employee = None
alertpage =late_alerts()
@eel.expose
def login(performance_id_input):
    global performance_id ,Employee,flag
    performance_id =int(performance_id_input)
    Employee = EmployeeStats(performance_id)
@eel.expose
def solfa():
    return  alertpage.school_fees();
@eel.expose
def all_alerts(sheetname,colname):
    return alertpage.alerts(sheetname,colname)
@eel.expose
def setFlag():
    Employee.set_flag("1")
@eel.expose
def getFlag():
    return Employee.get_flag()
    
@eel.expose
def logOut():
  performance_id = None;
  Employee = None;
  

@eel.expose
def get_all_info():
    all_info=[Employee.personal_info(),Employee.card_info(),Employee.job_info(),Employee.educational_info(),Employee.military_info(),Employee.social_info()]
    return all_info
@eel.expose
def make_hours_data():
    return Employee.make_hours_data();
@eel.expose
def update_range(start,end):
    Employee.update_range(start_mon=start,end_mon=end)
    
@eel.expose
def get_months_data(start,end):
    return ''
@eel.expose
def get_lateness():
    return Employee.months_lateness();

@eel.expose
def alerts():
    return alertpage.alerts();

@eel.expose
def get_performance_id():
    return performance_id  # Return the stored performance ID
@eel.expose
def getErrorLog():
    get_all_info()
    return remove_dublicate(Employee.error_log)
def remove_dublicate(my_list):
    unique_list = []
    for item in my_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

try:
    eel.init('web')
    eel.start('index.html', size=(800, 800))
except Exception as e:
    eel.start('index.html', size=(800, 800),mode ="edge")
    print("Error starting EEL:", e)