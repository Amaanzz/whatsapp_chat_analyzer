import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns



st.sidebar.title("whatsapp chat analyser")

uploaded_file = st.sidebar.file_uploader("choose to Upload a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data= bytes_data.decode("utf-8")
    df=preprocessor.preprocessor(data)

# fetching unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user=st.sidebar.selectbox("show analysis with respect to",user_list)

    if st.sidebar.button("show analysis"):
      num_messages, words, num_media_messages,links = helper.fetch_stats(selected_user,df)
      st.title("TOP STATISTICS")
      col1, col2, col3, col4 =st.columns(4)

      with col1:
          st.header("total messages")
          st.title(num_messages)
      with col2:
          st.header("total words")
          st.title(words)
      with col3:
          st.header("total media shared")
          st.title(num_media_messages)
      with col4:
          st.header("total links")
          st.title(links)
      #timeline
      st.title("MONTHLY TIMELINE STATISTICS")
      timeline=helper.monthly_timeline(selected_user,df)
      fig, ax = plt.subplots()
      ax.plot(timeline['time'], timeline['message'])
      plt.xticks(rotation='vertical')
      st.pyplot(fig)
      #dsily timeline
      st.title("DAILY TIMELINE STATISTICS")
      daily_timeline = helper.daily_timelines(selected_user, df)
      fig, ax = plt.subplots()
      ax.plot(daily_timeline['SPECIFIC_DATE'],daily_timeline['message'])
      plt.xticks(rotation='vertical')
      st.pyplot(fig)
      #activity map
      st.title("activity map")
      col1, col2=st.columns(2)
      with col1:
          st.header("most busy day")
          busy_day=helper.week_activity(selected_user,df)
          fig, ax = plt.subplots()
          ax.bar(busy_day.index, busy_day.values, color='red')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)
      with col2:
          st.header("most busy month")
          busy_month=helper.month_activity(selected_user,df)
          fig, ax = plt.subplots()
          ax.bar(busy_month.index, busy_month.values,color='green')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)
      st.title("Weekly Activity Map")
      user_heatmap = helper.activity_heatmap(selected_user, df)
      if not user_heatmap.empty:

       fig, ax = plt.subplots(figsize=(10, 6))

       sns.heatmap(user_heatmap,ax=ax)
       st.pyplot(fig)
      else:
          st.warning("No activity heatmap")

      #most busy users
      if selected_user=='overall':
          st.title("most busy users")
          x,new_df=helper.most_busy_users(df)
          fig, ax=plt.subplots()
          col1,col2= st.columns(2)
          with col1:
              ax.bar(x.index,x.values,color='black')
              plt.xticks(rotation='vertical')
              st.pyplot(fig)
          with col2:
              st.dataframe(new_df)


    #wordcloud
    st.title("WORDCLOUD")
    df_wc=helper.create_wordcloud(selected_user,df)
    fig, ax=plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    #most common words
    st.title("MOST COMMON WORDS LIST")
    most_common_df=helper.most_common_words(selected_user,df)
    fig , ax=plt.subplots()
    ax.bar(most_common_df[0], most_common_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    st.dataframe(most_common_df)
    #emoji
    emoji_df=helper.emoji_helper(selected_user,df)
    st.title("EMOJI DATA")
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(emoji_df)
    with col2:
        fig, ax = plt.subplots()
        ax.pie(emoji_df[1], labels=emoji_df[0], autopct="%0.2f")
        st.pyplot(fig)



