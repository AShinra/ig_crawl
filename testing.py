import instaloader
import pandas as pd
from datetime import datetime
import time
import json


def get_influencers():
    # Opening JSON file
    f = open('influencers.json')

    # returns JSON object as a dictionary
    data = json.load(f)

    # Closing file
    f.close()

    return data


def get_archive():

    return pd.read_excel('IG_posts.xlsx')


def get_archive_data(archive):

    # get latest date
    date_column = archive['Date'].to_list()
    date_column.sort(reverse=True)
    date_latest = date_column[0].date()

    # get url list
    archive_url_list = archive['URL'].to_list()

    return date_latest, archive_url_list



def main_ig(latest_date, url_list, profile_name):

    # Create an instance of Instaloader
    L = instaloader.Instaloader()

    # for private posts
    # Login to Instagram (optional, but necessary for private profiles)
    # L.login('your_username', 'your_password')

    influencer = []
    account = []
    post_date = []
    post_url = []
    post_caption = []
    post_likes = []
        
    try:
        profile = instaloader.Profile.from_username(L.context, profile_name)
        print(profile.full_name)
        # print(profile_name)
        posts = profile.get_posts()
        
    except Exception as msg_error:
        print('Limit Reached')
        df = pd.DataFrame()
        pass

    else:
        for post in posts:
            date_limit = latest_date
            
            if (post.date).date() >= date_limit:
                _url = f'https://www.instagram.com/p/{post.shortcode}'
                if _url not in url_list:

                    url_list.append(_url)
                    # L.download_post(post, target=profile_name)
                    # print(f'Date: {post.date_local}')
                    print(_url)
                    # print(f'Caption: {post.caption}')
                    # print(f'Likes: {post.likes}')
                    # print('--------------------------------------')

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
            print(f'No Latest IG Posts from {profile.full_name}')
        else:
            df.to_excel(f'new_{profile_name}_posts.xlsx', index=False)

    
    return df

    
if __name__ == "__main__":

    archive = get_archive()
    
    # get data from archive
    latest_date, url_list = get_archive_data(archive)

    # get influencer list
    data = get_influencers()

    # Download a user's profile
    profile_names = [v for k, v in data.items()]
    

    for profile_name in profile_names:
    
        merged_df = []
    
        archive = get_archive()

        time.sleep(5)
        df = main_ig(latest_date, url_list, profile_name)

        if df.empty:
            continue
        else:
            if archive.empty:
                df.to_excel('IG_posts.xlsx', index=False)
            else:
                merged_df.append(df)
                merged_df.append(archive)

                # combine archive and new extacted links
                df_new = pd.concat(merged_df)
                df_new.sort_values(by=['Date'], ascending=False, inplace=True)
                df_new.to_excel('IG_posts.xlsx', index=False)

    