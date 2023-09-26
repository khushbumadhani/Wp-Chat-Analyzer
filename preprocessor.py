
import pandas as pd
import re
def preprocessor(data):
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    message=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_message':message,'message_date':dates})
    df['message_date']=pd.to_datetime(df['message_date'],format='%m/%d/%y, %H:%M - ')
    df.rename(columns={'message_date':'date'},inplace=True)
    df.head()
    
   

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(': ', message)
    
        if len(entry) > 1:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df.head()

    df['year']=df['date'].dt.year
    df['only_date']=df['date'].dt.date
    df['month_num']=df['date'].dt.month
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['minute']=df['date'].dt.minute
    return df