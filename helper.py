from urlextract import URLExtract
from wordcloud import WordCloud
extract = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        num_messages = df.shape[0]
        #2. number of words
        words = []
        for messages in df['message']:
            words.extend(messages.split())

        # fetch number of media message
        num_media_messages = df[df['message'] == '<Media Omitted>\n'].shape[0]
        # print("Number of media messages:", num_media_messages)

        # fetch no. of links
        links = []
        for messages in df['message']:
            links.extend(extract.find_urls(messages))
            # print("Number of links:", len(links))

        return num_messages, len(words), num_media_messages, len(links)
    
def most_busy_users(df):
    x,new_df = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns={'index': 'name', 'user':'percent'})
    return x,df

def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc

# def most_common_words(selected_user, df):
    
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     temp = df[df['user'] != 'group_notification']
#     temp = df[df['message'] != '<Media omitted>\n']

#     words = []

#     for messages in temp['message']:
#         for word in messages.lower().split():
#             if word not in stop_words:
#                 words.append(word)