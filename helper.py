from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
import pandas as pd
import emoji_data_python as emoji_data
import re

extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    num_messages=df.shape[0]


    words=[]
    for m in df['message']:
        words.extend(m.split()) 
    media=df[df['message']=='<Media omitted>\n'].shape[0]
    
    link=[]
    for message in df['message']:
        link.extend(extract.find_urls(message))
      
    return num_messages,len(words),media,len(link)

def most_active_user(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

def create_wordcloud(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=300,min_font_size=10,background_color='white')
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

def emoji(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    
    emojis = []
    emoji_pattern = r'[\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF]'
    for message in df['message']:
    # Extract emojis from the message using the regular expression pattern
        extracted_emojis = re.findall(emoji_pattern, message)
        emojis.extend(extracted_emojis)
    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])
    return emoji_df

def montly_timeline(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!="Overall":
        df=df[df['user']==selected_user]
    return df['month'].value_counts()