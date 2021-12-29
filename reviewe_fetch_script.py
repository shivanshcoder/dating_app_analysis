# %%
# !pip install google-play-scraper
# !pip install tqdm

# %%
from google_play_scraper import app, reviews, Sort
import pandas as pd
import time
import string
import random
import os


# %%
def fetch_reviews(app_name, app_id):
    # Empty list for storing reviews
    app_reviews = []
    
    try:
        os.mkdir(app_name)
    except FileExistsError:
        pass
    
    break_off = False
    # Number of reviews to scrape per batch
    count = 200
    
    # To keep track of how many batches have been completed
    batch_num = 0
    
    
    # Retrieve reviews (and continuation_token) with reviews function
    rvws, token = reviews(
        app_id,           # found in app's url
        lang='en',        # defaults to 'en'
        country='us',     # defaults to 'us'
        sort=Sort.NEWEST, # start with most recent
        count=count       # batch size
    )
     
    
    # Add the list of review dicts to overall list
    app_reviews.extend(rvws)
    print(f'Batch {batch_num} completed.')
    
    # Increase batch count by one
    batch_num +=1 
    
    # Wait 1 to 5 seconds to start next batch
    time.sleep(random.randint(1,5))
    
    
    
    # Append review IDs to list prior to starting next batch
    pre_review_ids = []
    for rvw in app_reviews:
        pre_review_ids.append(rvw['reviewId'])
    
    
    # Loop through at most max number of batches
    for batch in range(4999):
    # for batch in range(2):
        rvws, token = reviews( # store continuation_token
            app_id,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=count,
            # using token obtained from previous batch
            continuation_token=token
        )
        
        # Append unique review IDs from current batch to new list
        new_review_ids = []
        for r in rvws:
            new_review_ids.append(r['reviewId'])
            
     
        # Add the list of review dicts to main app_reviews list
        app_reviews.extend(rvws)
        
        # Increase batch count by one
        batch_num +=1
        
        # Break loop and stop scraping for current app if most recent batch
          # did not add any unique reviews
        all_review_ids = pre_review_ids + new_review_ids
        if len(set(pre_review_ids)) == len(set(all_review_ids)):
            print(f'No reviews left to scrape. Completed {batch_num} batches.\n')
            break_off = True
        
        # all_review_ids becomes pre_review_ids to check against 
          # for next batch
        pre_review_ids = all_review_ids
        
        
        print(f'Batch {batch_num} completed.')
        # At every 100th batch
        if batch_num%100==0 or break_off:
        # if True:
            
            # print update on number of batches
            
            df = pd.DataFrame(app_reviews)
            # df = df[['content', 'thumbsUpCount', 'score']]
            
            ran = app_name + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))    
            
            df.to_csv(f"./{app_name}/{ran}.csv")
            
            # empty our list for next round of 100 batches
            app_reviews = []

            if(break_off):
                return
        
        # Wait 1 to 5 seconds to start next batch
        time.sleep(random.randint(1,5))
      
fetch_reviews('tinder', 'com.tinder')
    

