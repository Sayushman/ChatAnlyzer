import re
import pandas as pd

def preprocess(data):
    pattern_date = '(\d{1,2}/\d{1,2}/\d{2}),\s(\d{1,2}:\d{2})\s(AM|PM)\s'
    pattern_msg = '([A-Za-z\s]+:)\s(.*)'

    dates = re.findall(pattern_date, data)[:100]
    msg = re.findall(pattern_msg, data)[:100]

    df = pd.DataFrame({'user_msg': msg, 'user_date': dates})

    # Convert each tuple element to datetime
    df['user_date'] = df['user_date'].apply(lambda x: pd.to_datetime(' '.join(x), format='%m/%d/%y %I:%M %p'))

    # Convert 'message' column to string type
    df['user_msg'] = df['user_msg'].astype(str)

    # Rename the column
    df.rename(columns={'user_date': 'date'}, inplace=True)

    # Separate sender and messages
    users = []
    messages = []
    for msg in df['user_msg']:
        # entry = re.findall('([\w\W\s]+),', msg)
        entry = re.split('([\w\W\s]+),', msg)
        # entry = re.findall('([\w\W\s]+:)\s(.*)', msg)
        print(entry)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])  # Extract message excluding sender name
        else:
            users.append('group_notification')
            messages.append(msg)
            # messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_msg'], inplace=True)

    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['minute'] = df['date'].dt.minute
    df['hour'] = df['date'].dt.time


    return df



