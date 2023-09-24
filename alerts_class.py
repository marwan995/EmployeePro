import pandas as pd
import numpy as np
from datetime import datetime 

class late_alerts:
    def __init__(self) :
        self.excels_dict = self.read_all_excels()
        

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
             'data/shared_data/الحالة الاجتماعية.xlsx',
            'data/shared_data/سلفة.xlsx'
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
            excels_dict[excel_file.split('data/')[2].split('.')[0]] = df

        return excels_dict
    def school_fees(self):
        e_d = self.excels_dict
        sc_d =e_d['سلفة']
        s_d = e_d['الحالة الاجتماعية']
        df = pd.merge(sc_d, s_d, on=['رقم الاداء'], how='inner')
        mr = df[df['الإبن'].isin(df[['الإبن 1', 'الإبن 2', 'الإبن 3']].values.flatten())]
        end_matching = mr[mr['تاريخ الميلاد '].isin(mr[['تاريخ ميلاد الإبن 1', 'تاريخ ميلاد الإبن 2', 'تاريخ ميلاد الإبن 3']].values.flatten())]
        end_matching['تاريخ الميلاد '] = end_matching['تاريخ الميلاد '].apply(swap_day_month)
        res = end_matching[['رقم الاداء','الاســـم _x','الإبن','تاريخ الميلاد ']].to_dict(orient='records')
        return res


    def alerts(self ,sheetname,colname):
            e_d = self.excels_dict
            c_d = e_d[sheetname]
            c_d[colname] =c_d[colname].apply(swap_day_month)
            if colname =="تاريخ التعيين":
                c_d[colname] =c_d[colname].apply(calculate_updated_year)
            res = []
            
            for index, one_date in enumerate(c_d[colname]):
                try:
                    date_object = datetime.strptime(str(one_date), '%d/%m/%Y').date()
                except ValueError:
                    
                    # Handle the case where the date is in a different format
                    try:
                        date_object = pd.to_datetime(one_date).date()
                    except Exception:
                        continue

                current_date = datetime.now().date()
                
                if ((date_object.year, date_object.month) <= (current_date.year, current_date.month)) or ((date_object.year <= current_date.year) and (colname =="تاريخ التعيين") ):
                    row_dict = {}  # Create a dictionary for the current row
                    for column_name in c_d.columns:
                        
                        if column_name == colname:
                            row_dict[column_name] = date_object.strftime('%d/%m/%Y')
                        else:
                            value = c_d.at[index, column_name]
                            if isinstance(value, np.int64):
                                value = str(value)
                            elif(isinstance(value, pd.Timestamp)):
                                value = value.to_pydatetime().strftime('%d/%m/%Y')
                            row_dict[column_name] = value
                        row_dict['مدة التأخير'] = (current_date - date_object).days if (date_object) < (current_date) else -1

                    row_dict={key: value for key, value in row_dict.items() if pd.notna(value)}
                    res.append(row_dict)
            res=sorted(res, key=lambda x: x['مدة التأخير'],reverse=True)
            return res
def date_string(date):
    
    try:
        return date.strftime("%d/%m/%Y") if isinstance(date, datetime.date) else date
    except Exception as e:
        print(e)
        return "لا يوجد"
def calculate_updated_year(dateString):
    year = int(dateString.split("/")[2])
    this_year = datetime.now().year
    result = ((this_year - year) // 6) * 6 + year
    updated_year = result + 6 if result != this_year else result

    parts = dateString.split("/")
    parts[2] = str(updated_year)
    
    updated_date_string = "/".join(parts)
    return updated_date_string

def swap_day_month(date_str):
    try:
        if isinstance(date_str, datetime):
            date_str = date_str.strftime('%Y-%m-%d')
        elif isinstance(date_str, pd.Timestamp):
            date_str = date_str.strftime('%Y-%m-%d')

            
        date_object = datetime.strptime(date_str, '%Y-%m-%d')
        swapped_date = date_object.replace(day=date_object.month, month=date_object.day)
        return swapped_date.strftime('%d/%m/%Y')
    except Exception as e:
        return date_str