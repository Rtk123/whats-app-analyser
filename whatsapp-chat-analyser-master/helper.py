# from urlextract import URLExtract
# import pandas as pd
# from collections import Counter
# import emoji
# import re
# import regex
# import streamlit as st
# from datetime import datetime


# def fetchStats(selectedUser, dataFrame):
#     if selectedUser != "Overall":
#         dataFrame = dataFrame[dataFrame['user'] == selectedUser]
#     totalMessages = dataFrame.shape[0]

#     word = []
#     for message in dataFrame['message']:
#         if isinstance(message, str):
#             word.extend(message.split())
#     totalWords = len(word)

#     totalMedia = dataFrame[dataFrame['message']
#                            == '<Media omitted>\n'].shape[0]

#     extractor = URLExtract()
#     urls = extractor.find_urls(" ".join(word))
#     totalURL = len(urls)

#     return totalMessages, totalWords, totalMedia, totalURL


# def mostBusy(x):
#     topChatter = x['user'].value_counts().head()
#     topChatterPercent = round((x['user'].value_counts(
#     )/x.shape[0])*100, 2).reset_index().rename(columns={'index': "Name", 'user': 'Percentage'})

#     return topChatter, topChatterPercent


# def mostCommon(selectedUser, x):
#     if selectedUser != "Overall":
#         x = x[x['user'] == selectedUser]
#     # remove stopwords and group notifications
#     withoutGN = x[x['user'] != 'default']
#     withoutGNMedia = withoutGN[withoutGN["message"] != '<Media omitted>\n']

#     stopWords = open("stopwords-hinglish.txt", "r").read()

#     words = []

#     for message in withoutGNMedia['message']:
#         if isinstance(message, str):
#             for word in message.lower().split():
#                 if word not in stopWords:
#                     words.append(word)

#     mC = Counter(words).most_common(20)
#     mostCommon = pd.DataFrame(mC)
#     mostCommon = mostCommon.rename(columns={0: 'Message', 1: 'Frequency'})

#     return mostCommon


# def mostEmoji(selectedUser, x):
#     if selectedUser != 'Overall':
#         x = x[x['user'] == selectedUser]
#     emojis = []
#     for message in x['message']:
#         if isinstance(message, str):
#             message_emojized = emoji.emojize(message, language='alias')
#             emojis.extend(
#                 [c for c in message_emojized if c in emoji.UNICODE_EMOJI['en']])

#     emoji_counts = Counter(emojis)
#     emoji_df = pd.DataFrame(list(emoji_counts.items()),
#                             columns=['Emoji', 'Count'])
#     emoji_df['Emoji'] = emoji_df['Emoji'].apply(
#         lambda x: emoji.emojize(x, language='alias'))
#     emoji_df = emoji_df.sort_values(
#         'Count', ascending=False).reset_index(drop=True)

#     return emoji_df


# def monthlyTimeline(selectedUser, x):
#     if selectedUser != "Overall":
#         x = x[x['user'] == selectedUser]
#     timeline = x.groupby(['year', 'monthNum', 'month']).count()[
#         'message'].reset_index()

#     time = []
#     for i in range(timeline.shape[0]):
#         time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
#     timeline['time'] = time
#     return timeline


# def dailyTimeline(selectedUser, x):
#     if selectedUser != "Overall":
#         x = x[x['user'] == selectedUser]
#     x['onlyDate'] = pd.to_datetime(x['date']).dt.date
#     dailyTimeline = x.groupby("onlyDate").count()['message'].reset_index()
#     return dailyTimeline


# def weekActivity(selectedUser, x):
#     if selectedUser != "Overall":
#         x = x[x['user'] == selectedUser]
#     weekActivity = x.groupby("dayName").count()['message'].reset_index()
#     return x['dayName'].value_counts(), weekActivity


# def monthActivity(selectedUser, x):
#     if selectedUser != "Overall":
#         x = x[x['user'] == selectedUser]
#     monthActivity = x.groupby("monthName").count()['message'].reset_index()
#     return x['monthName'].value_counts(), monthActivity


# def hourActivity(selectedUser, x):
#     if selectedUser != "Overall":
#         x = x[x['user'] == selectedUser]
#     return x.groupby(['dayName', 'hour'])['message'].count(), x.groupby(['dayName', 'hour'])['message'].count().reset_index()



# def messageExtractor (selectedUser, x, inputDate):
#     #inputDate = "20-04-2023"
#     if selectedUser != "Overall":
#         x = x[x['user'] == selectedUser]
#     if (len(inputDate)==10):
#         dd = inputDate[0:2]
#         mm = inputDate[3:5]
#         yyyy = inputDate[6:]
#         if (dd[0]=='0'): dd = dd[1]
#         if (mm[0]=='0'): mm = mm[1]
#         mask = (x['day'].astype(str) == dd) & (x['monthNum'].astype(str) == mm) & (x['year'].astype(str) == yyyy)
#         messageExtract = pd.DataFrame(x[mask])[['user', 'message']]
#         if (messageExtract.shape[0]>0):
#             messageExtract['time'] = x['hour'].astype(str) + ':' + x['minute'].astype(str)
#             messageExtract['message'] = messageExtract['message'].str.replace('\n', '')
#         #st.dataframe(messageExtract)

#         return messageExtract

# def activity (selectedUser, x):
#     if selectedUser != "Overall":
#         x = x[x['user'] == selectedUser]
#     activityX = x.groupby("period").count()['message'].reset_index()
#     return activityX

# def replyTime (selectedUser, x):
#     timeSelected = pd.Timedelta(0)
#     timeDifference = x.groupby('user')['replyTime'].mean().reset_index().sort_values('replyTime', ascending=True).head(5)
#     timeDifference = timeDifference[timeDifference['user'] != 'default']
#     if selectedUser != "Overall":
#         x = x[x['user'] == selectedUser]
#         timeSelected = timeDifference[timeDifference['user'] == selectedUser]['replyTime'].iloc[0]

#     return timeDifference, timeSelected


from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
import streamlit as st
from datetime import datetime


def fetch_stats(selected_user, data_frame):
    # Filter data for the selected user
    if selected_user != "Overall":
        data_frame = data_frame[data_frame['user'] == selected_user]
    
    # Calculate total messages, words, media shares, and URLs
    total_messages = data_frame.shape[0]
    words = [word for message in data_frame['message'] if isinstance(message, str) for word in message.split()]
    total_words = len(words)
    total_media = data_frame[data_frame['message'] == '<Media omitted>\n'].shape[0]

    extractor = URLExtract()
    urls = extractor.find_urls(" ".join(words))
    total_urls = len(urls)

    return total_messages, total_words, total_media, total_urls


def most_busy(data_frame):
    # Find top active users
    top_chatter = data_frame['user'].value_counts().head()
    top_chatter_percent = round((data_frame['user'].value_counts() / data_frame.shape[0]) * 100, 2)
    top_chatter_percent = top_chatter_percent.reset_index().rename(columns={'index': "Name", 'user': 'Percentage'})

    return top_chatter, top_chatter_percent


def most_common(selected_user, data_frame):
    # Filter data for the selected user and remove group notifications and media messages
    if selected_user != "Overall":
        data_frame = data_frame[data_frame['user'] == selected_user]
    without_gn = data_frame[data_frame['user'] != 'default']
    without_gn_media = without_gn[without_gn["message"] != '<Media omitted>\n']

    # Load stopwords and find most common words
    with open("stopwords-hinglish.txt", "r") as f:
        stopwords = f.read().splitlines()
    
    words = [word for message in without_gn_media['message'] if isinstance(message, str) 
             for word in message.lower().split() if word not in stopwords]
    
    most_common_words = pd.DataFrame(Counter(words).most_common(20), columns=['Message', 'Frequency'])

    return most_common_words


def most_emoji(selected_user, data_frame):
    # Filter data for the selected user
    if selected_user != 'Overall':
        data_frame = data_frame[data_frame['user'] == selected_user]
    
    # Find emojis in messages
    emojis = [c for message in data_frame['message'] if isinstance(message, str)
              for c in emoji.emojize(message, language='alias') if c in emoji.UNICODE_EMOJI['en']]
    
    emoji_counts = pd.DataFrame(list(Counter(emojis).items()), columns=['Emoji', 'Count'])
    emoji_counts['Emoji'] = emoji_counts['Emoji'].apply(lambda x: emoji.emojize(x, language='alias'))
    emoji_counts = emoji_counts.sort_values('Count', ascending=False).reset_index(drop=True)

    return emoji_counts


def monthly_timeline(selected_user, data_frame):
    # Filter data for the selected user
    if selected_user != "Overall":
        data_frame = data_frame[data_frame['user'] == selected_user]
    
    # Create monthly message count timeline
    timeline = data_frame.groupby(['year', 'monthNum', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline.apply(lambda row: f"{row['month']}-{row['year']}", axis=1)

    return timeline


def daily_timeline(selected_user, data_frame):
    # Filter data for the selected user
    if selected_user != "Overall":
        data_frame = data_frame[data_frame['user'] == selected_user]
    
    # Create daily message count timeline
    data_frame['onlyDate'] = pd.to_datetime(data_frame['date']).dt.date
    daily_timeline = data_frame.groupby("onlyDate").count()['message'].reset_index()

    return daily_timeline


def week_activity(selected_user, data_frame):
    # Filter data for the selected user
    if selected_user != "Overall":
        data_frame = data_frame[data_frame['user'] == selected_user]
    
    # Count messages by day of the week
    week_activity = data_frame.groupby("dayName").count()['message'].reset_index()

    return data_frame['dayName'].value_counts(), week_activity


def month_activity(selected_user, data_frame):
    # Filter data for the selected user
    if selected_user != "Overall":
        data_frame = data_frame[data_frame['user'] == selected_user]
    
    # Count messages by month
    month_activity = data_frame.groupby("monthName").count()['message'].reset_index()

    return data_frame['monthName'].value_counts(), month_activity


def hour_activity(selected_user, data_frame):
    # Filter data for the selected user
    if selected_user != "Overall":
        data_frame = data_frame[data_frame['user'] == selected_user]
    
    # Count messages by hour and day of the week
    activity = data_frame.groupby(['dayName', 'hour'])['message'].count()
    return activity, activity.reset_index()


def message_extractor(selected_user, data_frame, input_date):
    # Extract messages based on input date
    if selected_user != "Overall":
        data_frame = data_frame[data_frame['user'] == selected_user]
    
    if len(input_date) == 10:
        dd, mm, yyyy = input_date.split('-')
        mask = (data_frame['day'].astype(str) == dd.lstrip('0')) & \
               (data_frame['monthNum'].astype(str) == mm.lstrip('0')) & \
               (data_frame['year'].astype(str) == yyyy)
        
        extracted_messages = data_frame[mask][['user', 'message']]
        if not extracted_messages.empty:
            extracted_messages['time'] = data_frame['hour'].astype(str) + ':' + data_frame['minute'].astype(str)
            extracted_messages['message'] = extracted_messages['message'].str.replace('\n', '')

        return extracted_messages


def activity(selected_user, data_frame):
    # Filter data for the selected user
    if selected_user != "Overall":
        data_frame = data_frame[data_frame['user'] == selected_user]
    
    # Count messages by time period
    activity_data = data_frame.groupby("period").count()['message'].reset_index()

    return activity_data


def reply_time(selected_user, data_frame):
    # Calculate average reply time per user
    time_difference = data_frame.groupby('user')['replyTime'].mean().reset_index()
    time_difference = time_difference.sort_values('replyTime', ascending=True).head(5)
    time_difference = time_difference[time_difference['user'] != 'default']
    
    time_selected = pd.Timedelta(0)
    if selected_user != "Overall":
        data_frame = data_frame[data_frame['user'] == selected_user]
        time_selected = time_difference[time_difference['user'] == selected_user]['replyTime'].iloc[0]

    return time_difference, time_selected
