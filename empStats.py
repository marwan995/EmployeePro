import pandas as pd
import numpy as np
import datetime 

class EmployeeStats:
    def __init__(self,perf_id,start_mon = 1,end_mon = 12):
        self.id=perf_id
        self.start_mon = start_mon
        self.end_mon = end_mon
        self.error_log =[]
        self.dfs = self.read_range(start_mon, end_mon)
        self.emp_df = self.extract_days()
        self.lateness = self.calculate_lateness()
        self.excels_dict = self.read_all_excels()
        self.flag="0"
    def update_range(self, start_mon, end_mon):
        self.start_mon = start_mon
        self.end_mon = end_mon
        self.dfs = self.read_range(start_mon, end_mon)
        self.emp_df = self.extract_days()
        self.lateness = self.calculate_lateness()
        self.error_log = []
    def get_flag(self):
        return self.flag
    def set_flag(self,val):
        self.flag = val
    def card_info(self):
        e_d = self.excels_dict
        c_d={}
        c1_d={}
        try:
            c_d = e_d['بطاقات شخصية'].iloc[0]  
        except Exception as e:
            self.error_log.append(" لم يتم العثور علي رقم الاداء "+str(self.id)+" "+"في شيت البطاقات")
            return {'title':"معلومات البطاقة"}
        try:
            c1_d = e_d['موهلات عليا تعديل'].iloc[0] 
        except Exception as e:
              c1_d['نوعها (شخصية -عائلية-قومى )']='لا يوجد'
              self.error_log.append( "لم يتم العثور علي رقم الاداء "+str(self.id)+" "+"في شيت موهلات عليا تعديل")
        c_info = {
            'title':"معلومات البطاقة",
            'رقم البطاقة': str(c_d['رقم البطاقة ']),
            'تاريخ صدور البطاقة': date_string(c_d['تاريخ صدور البطاقة']),
            'تاريخ الانتهاء': date_string(c_d['تاريخ الانتهاء']) ,
            'محافظة الصدور': c_d['محافظة الصدور'],
            'جهة الصدور': c_d['جهة الصدور'],
            'نوعها': c1_d['نوعها (شخصية -عائلية-قومى )']
        }

        c_info = {key: value for key, value in c_info.items() if pd.notna(value)}
        return c_info;
    def personal_info(self):
        e_d = self.excels_dict
        p_d={}
        p1_d={}
        p2_d={}
        current_date = datetime.date.today() 
        try:
            p_d = e_d['بيانات العاملين'].iloc[0]  
          
        except Exception  as e:
            self.error_log.append(" لم يتم العثور علي رقم الاداء "+str(self.id)+" بيانات العاملين "+"في شيت ")
            return {'title':"معلومات شخصية"}
        try:
            p1_d = e_d['موهلات عليا تعديل'].iloc[0]  

        except Exception as e:
              self.error_log.append( "لم يتم العثور علي رقم الاداء "+str(self.id)+" "+"في شيت موهلات عليا تعديل")
              return {
                  'title':"معلومات شخصية",
                  'الإسـم': p_d['الأسم'],
                  'رقم الأداء': str( p_d['رقم الاداء']),
                  'الرقم القومي':str( p_d['رقم البطاقة ']),
                  'التليفون': p_d['رقم المحمول'],
                  'السن': current_date.year - int(date_string(p_d['تاريخ الميلاد ']).split('/')[2]) ,
                  'الحاله الإجتماعية': p_d['الحاله الإجتماعية '],
                  'تاريخ الميلاد' : date_string(p_d['تاريخ الميلاد ']),
                  'العنوان': p_d['العنوان ']}
        
        
        p_info = {
            'title':"معلومات شخصية",
            'الإسـم': p_d['الأسم'],
            'رقم الأداء': str( p_d['رقم الاداء']),
            'الرقم القومي':str( p_d['رقم البطاقة ']),
            'التليفون': p_d['رقم المحمول'],
            'الديانة' : p1_d['الديانه'],
            'اللقب': 'لا يوجد',
            'النوع' : p1_d['النوع'],
            'السن': current_date.year - int(date_string(p_d['تاريخ الميلاد ']).split('/')[2]) ,
            'الحاله الإجتماعية': p_d['الحاله الإجتماعية '],
            'تاريخ الميلاد' : date_string(p_d['تاريخ الميلاد ']),
            'العنوان': p_d['العنوان ']
            
        }
        try:
            p2_d = e_d['أسم الموظف مفصل'].iloc[0]
            p_info['اللقب']=p2_d['اللقب ( العائلة)']
        except Exception as e:
              self.error_log.append( "لم يتم العثور علي رقم الاداء "+str(self.id)+" "+"في شيت أسم الموظف مفصل")
            
        p_info = {key: value for key, value in p_info.items() if pd.notna(value)}
        return p_info
   
    def months_lateness(self):
        month_list = [[] for _ in range(13)]
        month_total=[[] for _ in range(13)]
        
        for index, row in self.lateness.iterrows():
            date_parts = row['date'].split('/')
            day = date_parts[0]
            month = int( int(date_parts[1]) - 1 )
            lateness = row['lateness']
            month_total[month].append( round(lateness, 2))
            entry = day + ' - ' + str(round(lateness, 2))
            month_list[month].append(entry)
        
        for index in range(len(month_total)):
            month_total[index] = round(total_latness(month_total[index]),2)
                    
        return {'days':lateness_helper(month_list,False),'totalPerMonth':lateness_helper(month_total,False),'total':round(total_latness(month_total),2)};
    
    def military_info(self):
        e_d = self.excels_dict
        m_d={}
        try:
            m_d = e_d['الخدمة العسكرية'].iloc[0]  
        except Exception as e:
              self.error_log.append( "لم يتم العثور علي رقم الاداء "+str(self.id)+" "+"في شيت الخدمة العسكرية")
              return {'title':"معلومات عسكرية"}
        m_info = {
            'title':"معلومات عسكرية", 
            'الموقف من التجنيد' : m_d['الموقف من التجنيد'],
            'الدرجة': m_d['الدرجة'],
            'تاريخ بداية الخدمة':date_string(m_d['تاريخ بداية الخدمة ']),
            'تاريخ انتهاء الخدمة':date_string(m_d['تاريخ انتهاء الخدمة']),
            'توضيح المسببات':m_d['توضيح المسببات']  
        }
    
        m_info = {key: value for key, value in m_info.items() if pd.notna(value)}
        return m_info
    def job_info(self):
        e_d =self.excels_dict
        j_d={}
        
        try:
            j_d = e_d['بيانات العاملين'].iloc[0]
        except Exception as e:
            self.error_log.append(" لم يتم العثور علي رقم الاداء "+str(self.id)+" بيانات العاملين "+"في شيت ")
            return {'title':"معلومات وظيفية"} 
        ed_d = e_d['المؤهل الدراسي للعاملين']
        j_info = {
            'title':"معلومات وظيفية",
        }
        for column in e_d['بيانات العاملين'].columns[e_d['بيانات العاملين'].columns.get_loc('تاريخ بداية بالقطاع الخبرة'):e_d['بيانات العاملين'].columns.get_loc('المستوي الوظيفي')+1]:
            value = j_d[column]
            if isinstance(value, pd.Timestamp):
                value = value.strftime('%d/%m/%Y')
            j_info[column] = str(value)
        j_info ['قياس مستوي المهارة'] ='لا يوجد'
        j_info ['شهادة مزاولة المهنة'] ='لا يوجد'
        try:
            j_info ['قياس مستوي المهارة'] =date_string(ed_d['قياس مستوي المهارة'].iloc[0])
            j_info ['شهادة مزاولة المهنة'] =date_string(ed_d['تاريخ الانتهاء'].iloc[0])
        except Exception as e:
            self.error_log.append("لم يتم العثور علي رقم الاداء "+str(self.id)+" "+" في شيت المؤهل الدراسي للعاملين ")
       
        j_info = {key: value for key, value in j_info.items() if pd.notna(value)}
        return j_info;

    def educational_info(self):
        e_d = self.excels_dict
        ed_d={}
        try:
            ed_d = e_d['المؤهل الدراسي للعاملين'].iloc[0]
        except Exception as e:
            self.error_log.append("لم يتم العثور علي رقم الاداء "+str(self.id)+" "+" في شيت المؤهل الدراسي للعاملين ")
            return {'title':"معلومات دراسية"}
        ed_info = {
            'title':"معلومات دراسية",
        }
        for column in e_d['المؤهل الدراسي للعاملين'].columns[e_d['المؤهل الدراسي للعاملين'].columns.get_loc('المؤهل الحالي'):e_d['المؤهل الدراسي للعاملين'].columns.get_loc('تاريخ  الحصول عليها')+1]:
            value = ed_d[column]
            if isinstance(value, pd.Timestamp):
                value = value.strftime('%d/%m/%Y')
            ed_info[column] = value
    
        ed_info = {key: value for key, value in ed_info.items() if pd.notna(value)}
        return ed_info;
    def social_info(self):
            e_d = self.excels_dict
            s_d={}
            try:
                s_d = e_d['الحالة الاجتماعية'].iloc[0]
            except Exception as e:
                self.error_log.append("لم يتم العثور علي رقم الاداء "+str(self.id)+" "+" في شيت الحالة الاجتماعية ")
                return {'title':"معلومات الحالة الاجتماعية"}
            s_info = {
                'title':"معلومات الحالة الاجتماعية",
            }
            for column in e_d['الحالة الاجتماعية'].columns[e_d['الحالة الاجتماعية'].columns.get_loc('الحالة الإجتماعية'):e_d['الحالة الاجتماعية'].columns.get_loc('ملاحظات')+1]:
                value = s_d[column]
                if isinstance(value, pd.Timestamp):
                    value = value.strftime('%d/%m/%Y')
                s_info[column] = value
        
            s_info = {key: value for key, value in s_info.items() if pd.notna(value)}
            return s_info;


    def read_all_excels(self):
        excels_dict = {}
        excel_files = [
            'data/shared_data/بيانات العاملين.xlsx',
            'data/shared_data/بطاقات شخصية.xlsm',
            'data/shared_data/الخدمة العسكرية.xlsx',
            'data/shared_data/العلاوات التشجعية والمكافاة التشجعية.xlsx',
            'data/shared_data/المؤهل الدراسي للعاملين.xlsx',
            'data/shared_data/المؤهلات العليا.xlsx',
            'data/shared_data/موهلات عليا تعديل.xlsx',
            'data/shared_data/أسم الموظف مفصل.xlsx',
            'data/shared_data/اقرار ذمة مالية.xlsx',
            'data/shared_data/الحالة الاجتماعية.xlsx'

        ]
        for excel_file in excel_files:
            sheet_name = pd.ExcelFile(excel_file).sheet_names[0]
            
            df = pd.DataFrame();
            if excel_file == 'data/shared_data/بطاقات شخصية.xlsm' or excel_file =='data/shared_data/موهلات عليا تعديل.xlsx':
                df = pd.read_excel(excel_file, sheet_name=sheet_name, engine="openpyxl",header=3) 
            elif excel_file =='data/shared_data/العلاوات التشجعية والمكافاة التشجعية.xlsx':
                df = pd.read_excel(excel_file, sheet_name=sheet_name, engine="openpyxl",header=1)
            else:
                df = pd.read_excel(excel_file, sheet_name=sheet_name, engine="openpyxl")
            try:
                filtered_df = df[df['رقم الاداء'] == self.id].head(1)
                excels_dict[excel_file.split('data/')[2].split('.')[0]] = filtered_df
            except Exception as e:
                self.error_log.append(f"{self.id}"+"رقم الأداء"+f"{excel_file}"+" غير موجود في شيت ")


        return excels_dict

    def extract_days(self):
        days_df = []
        for index , d in enumerate(self.dfs):
            d.fillna(0, inplace=True)
            columns_range = d.loc[:, 1:31]
            try:
                row_with_id = columns_range.loc[d['رقم الأداء '] == self.id]
                
                if  not row_with_id.empty:
                    days_df.append(row_with_id.head(1))
                else:
                    self.error_log.append(f"{index+1} "+"رقم الاداء رقم "+f"{self.id}: "+"غير موجود في شيت شهر ")
            except Exception as e:
                self.error_log.append(f"{index+1} "+f"غير موجود  في شيت شهر  {self.id}:"+"رقم الاداء رقم ")
            
        return days_df

    def calculate_lateness(self):
        try:
            lateness = pd.DataFrame(columns=["date", "lateness"])
            for index, mon in enumerate(self.emp_df):
                for day in mon.columns:
                   try:
                        working_hours = mon[day].iloc[0]
                        if working_hours == 0.0 or working_hours == 8.0 or  isinstance(working_hours, str)  :
                            continue

                        date_val = str(day) + "/" + str(index + 1) + "/" + str(datetime.datetime.now().year)
                        late = 7.6 - working_hours if int(working_hours) < working_hours else 8 - working_hours
                        lateness = pd.concat([lateness, pd.DataFrame({"date": [date_val], "lateness": [late]})], ignore_index=True)
                   except KeyError:
                        self.error_log.append("عند حساب مده التأخير"+f"{day}"+" لم يتم العثور على العمود")
            lateness.fillna("", inplace=True)
            return lateness
        except Exception as e:
            self.error_log.append(f'Error occurred: {str(e)} in lateness claculation')
            return lateness


    def make_hours_data(self):
        types_of_day = {'سفر', 'حج', 'س/و', 'ع', 'غ','س','ص','و','م','ع ب','ث','ب ر','ع ع'}
        
        # Initialize a dictionary to store the lists of lists
        lists_of_lists = {word: [[] for _ in range(13)] for word in types_of_day}
        
        list_of_dfs = self.emp_df
        for month_index, df in enumerate(list_of_dfs, start=1):
            for col in df.columns:
                try:
                    val = df[col].iloc[0]
                    if val in types_of_day:
                        lists_of_lists[val][month_index].append(col)
                except KeyError:
                    self.error_log.append( f'{month_index}'+' في شيت '+f'{col} '+'لم يتم العثور على العمود')
        lists_of_lists ={word:lateness_helper(lists_of_lists[word],True) for word in lists_of_lists }
        return lists_of_lists


    def read_range(self,start_mon, end_mon):
        dfs = []
        for i in range(start_mon, end_mon + 1):
            try:

                dfs.append(pd.read_excel(f"data/mon{i}/mon{i}.xlsx", engine="openpyxl", header=1, sheet_name="شيت الساعات"))
            except Exception:
                self.error_log.append(f'mon{i}.xlsx'+'لم يتم العثور علي '+' شيت ')
                continue
        return dfs
def lateness_helper(list,flag):
    non_empty_indices = [i for i, sublist in enumerate(list) if sublist]
    first_non_empty_idx = non_empty_indices[0] if non_empty_indices else None
    last_non_empty_idx = non_empty_indices[-1] if non_empty_indices else None
    sublist = list[1 if flag else first_non_empty_idx :last_non_empty_idx + 1] if first_non_empty_idx is not None and last_non_empty_idx is not None else []
    return sublist
def total_latness(late):

    total_hours = 0
    fraction_sum = 0

    for entry in late:
        whole_hour = int(entry)
        fraction = round(entry - whole_hour,2)
        
        total_hours += whole_hour
        fraction_sum += fraction
        
        if fraction_sum >= 0.6:
            total_hours += 1
            fraction_sum -= 0.6
    total_hours += fraction_sum
    return total_hours
def date_string(date):
    try:
        return date.strftime("%d/%m/%Y") if isinstance(date, datetime.date) else date
    except Exception as e:
        return "لا يوجد"






