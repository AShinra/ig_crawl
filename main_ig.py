import streamlit as st
import pandas as pd
import instaloader
import streamlit_shadcn_ui as ui
from datetime import datetime
import json


def get_influencers():

    # Opening JSON file
    f = open('influencers.json')

    # returns JSON object as a dictionary
    influencer_data = json.load(f)

    # Closing file
    f.close()

    return influencer_data


def main_crawl(profile_name, date_range):

    L = instaloader.Instaloader()

    # for private posts
    # Login to Instagram (optional, but necessary for private profiles)
    # L.login('your_username', 'your_password')

    url_list = []

    influencer = []
    account = []
    post_date = []
    post_url = []
    post_caption = []
    post_likes = []
        
    try:
        profile = instaloader.Profile.from_username(L.context, profile_name)
        # print(profile.full_name)
        # print(profile_name)
        posts = profile.get_posts()
        
    except Exception as msg_error:
        print('Limit Reached')
        df = pd.DataFrame()
        pass

    else:
        for post in posts:
            # date_limit = latest_date
            date_start = date_range[0]
            date_start = datetime.strptime(date_start, '%Y-%m-%d').date()

            date_end = date_range[1]
            date_end = datetime.strptime(date_end, '%Y-%m-%d').date()
            
            if (post.date).date() >= date_start and (post.date).date() <= date_end:
                _url = f'https://www.instagram.com/p/{post.shortcode}'
                if _url not in url_list:

                    url_list.append(_url)
                    # st.write(_url)
                    
                    influencer.append(profile.full_name)
                    account.append(profile_name)
                    post_date.append(post.date)
                    post_url.append(f'https://www.instagram.com/p/{post.shortcode}')
                    post_caption.append(post.caption)
                    post_likes.append(post.likes)
            
            else:
                break

       
        df = pd.DataFrame({'Influencer':influencer, 'Date':post_date, 'URL':post_url, 'Likes':post_likes, 'Caption':post_caption})

        if df.empty:
            st.write(f'No Latest IG Posts from {profile.full_name} or it may be :red[Private]')
        else:
            # df.to_excel(f'new_{profile_name}_posts.xlsx', index=False)
            st.write(f'{df.shape[0]} post/s found for {profile.full_name}')
    
    return df  




if __name__ == "__main__":

    influencers = get_influencers()
    # get influencer names
    influencer_names = []
    for k, v in influencers.items():
        influencer_names.append(k)
    
    # create page header
    st.header('**Instagram Crawler**')

    col1, col2, col3 = st.columns([3,2,2])
    with col1:
        # create date picker
        date_range = ui.date_picker(label='Select Date Range', mode='range', key='date_range', default_value=None)

        # create text box
        # st.text_input(label='**:blue[Influencer Account]**', key='influencer_account', )

        st.selectbox(label='**:blue[Influencer Name]**', key='influencer_name', options=influencer_names)

    # create button
    st.button(label='Get Posts', key='button_get_posts')

    if st.session_state['button_get_posts']:
        if date_range != None:
            influencer_account = influencers[st.session_state['influencer_name']]
            df = main_crawl(influencer_account, date_range)
            if df.empty:
                pass
            else:
                st.dataframe(df, hide_index=True)
        else:
            st.error('Please input date range!!!')



    
    
