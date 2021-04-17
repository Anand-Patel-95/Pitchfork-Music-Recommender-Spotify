#!/usr/bin/env python
# coding: utf-8

# ## Read this CSV back in as our DF to make sure things look right
# 
# Verifying that the utf-8 encoding is okay.

# In[2]:


import pandas as pd

p4k_reviews_fname = 'p4kreviews-2017-utf8sig.csv'

p4k_df_2017 = pd.read_csv(p4k_reviews_fname, index_col = 0)

p4k_df_2017.tail()


# ## See if we can get album names and artist names

# In[3]:


album_name_lst = list(p4k_df_2017.album)
artist_name_lst = list(p4k_df_2017.artist)


# ## Generate DataFrame CSV for Spotify Data on P4K 2017 Albums
# 
# Be VERY careful running the below code. It is prone to timing out, and do NOT overwrite data you want to keep.



# In[6]:


from search_Album_get_Tracks_functions import *


# In[7]:


# In[4]:


Found_Albums = Find_Albums(album_name_lst, artist_name_lst)
# print(json.dumps(Found_Albums, indent=4, ensure_ascii=False))  # reading back from JSON


# In[8]:


# In[6]:

for album_uri_key in Found_Albums:  # each album's uri
    albumSongs(album_uri_key, Found_Albums)
    print(
        "Album " + str(Found_Albums[album_uri_key]["album_name"]) + " songs has been added to Found_Albums dictionary")


# In[9]:


# Create a deep copy of Found_Data to preserve the original incase we get errors and don't want to mess up the data

import copy

Found_Albums_backup = copy.deepcopy(Found_Albums)


# In[10]:


# In[7]:


# print Found_Albums with track info
# print(json.dumps(Found_Albums, indent=4, ensure_ascii=False))  # reading back from JSON

# In[10]:


Add_Track_AudioFeatures(Found_Albums)
# print(json.dumps(Found_Albums, indent=4, ensure_ascii=False))  # reading back from JSON


# In[11]:


print(len(Found_Albums))


# In[ ]:





# In[ ]:




# In[12]:


dic_df = create_df_dict(Found_Albums)

# In[13]:



df = pd.DataFrame.from_dict(dic_df)
df

# ## Remove duplicates
# Spotify has a duplicate issue which we can only address by removing all but the most popular songs

# In[14]:


print(len(df))
final_df = df.sort_values('popularity', ascending=False).drop_duplicates('name_track').sort_index()
print(len(final_df))

# ## Save to CSV

# In[23]:


csv_save_filename = "sp-p4k-2017-tracks-final.csv"
final_df.to_csv(csv_save_filename, encoding='utf-8-sig')

# In[16]:


final_df

# In[18]:


# combine the albums
combined_albums_df = combine_albums(final_df)
combined_albums_df

# In[22]:


# save combined albums to csv
csv_save_filename = "sp-p4k-2017-albums-final.csv"
combined_albums_df.to_csv(csv_save_filename, encoding="utf-8-sig")

