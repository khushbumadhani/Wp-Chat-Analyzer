
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload a file")

if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocessor(data)
    # st.dataframe(df)

    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user=st.sidebar.selectbox("Show analysis with",user_list)

    if st.sidebar.button("Show Analysis"):
        num_msg,words,media,links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(media)
        with col4:
            st.header("Links Shared")
            st.title(links)

        st.title("Monthly Timeline ")
        timeline=helper.montly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Activity map")
        col1,col2=st.columns(2)
        with col1:
            st.header("most active day")
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots(figsize=(8, 7))
            
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("most active month")
            busy_month=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        
        if selected_user=='Overall':
            st.title("most active user")
            x,new_df=helper.most_active_user(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)
            
            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        df_wc=helper.create_wordcloud(selected_user,df)
        st.title("wordcloud")
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        emoji_df=helper.emoji(selected_user,df)
        st.title("emoji Analysis")
        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            top_emojis = emoji_df.head(5)
            emoji_labels = top_emojis['Emoji']
            emoji_counts = top_emojis['Count']

            # Plotting the pie chart using Streamlit
            st.set_option('deprecation.showPyplotGlobalUse', False)  # Disable deprecated warning
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(emoji_counts, labels=emoji_labels, autopct='%1.1f%%', startangle=90)
            ax.set_title('Top 10 Emojis')
            ax.axis('equal')


            st.pyplot(fig)
        
    

