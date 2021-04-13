import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from scipy import stats

#Main question 
tracks = pd.read_csv('our_tracks.csv')

##Numerical Variables used in this section
analysis_variables= ['username']
numerical_variables= tracks.dtypes[tracks.dtypes== 'float64']
numerical_variables= list(numerical_variables.index)
[analysis_variables.append(i) for i in numerical_variables]
analysis_variables.append('popularity')
analysis_variables.append('duration_ms')


##General dataset of numerical variables
musical_preferences = tracks[analysis_variables]


#########First batch of plots####
fig, axs = plt.subplots(2, 2, figsize=(12, 6), gridspec_kw=dict(width_ratios=[6, 6]))
fig.suptitle('Music Features Differences')

sns.kdeplot(data=musical_preferences, x="valence"  ,
             hue="username",  cut=0, fill=True, 
            ax=axs[0,0]).set_title('Valence Differences')

sns.kdeplot(data=musical_preferences, x="popularity"  
            , hue="username",  cut=0, fill=True, 
            ax=axs[0,1]).set_title('Popularity Differences')

sns.kdeplot(data=musical_preferences, x="danceability"  ,
             hue="username",  cut=0, fill=True, 
            ax=axs[1,0]).set_title('Danceability Differences')

sns.kdeplot(data=musical_preferences, x="energy"  
            , hue="username",  cut=0, fill=True, 
            ax=axs[1,1]).set_title('Energy Differences*')

fig.tight_layout()


##Second batch of plots#####
fig, axs = plt.subplots(2, 2, figsize=(12, 6), gridspec_kw=dict(width_ratios=[6, 6]))
fig.suptitle('Music Features Differences- 2')

sns.kdeplot(data=musical_preferences, x="acousticness"  ,
             hue="username",  cut=0, fill=True, 
            ax=axs[0,0]).set_title('Acousticness Differences')

sns.kdeplot(data=musical_preferences, x="loudness"  
            , hue="username",  cut=0, fill=True, 
            ax=axs[0,1]).set_title('Loudness Differences')

sns.kdeplot(data=musical_preferences, x="instrumentalness"  ,
             hue="username",  cut=0, fill=True, 
            ax=axs[1,0]).set_title('Instrumentalness Differences')

sns.kdeplot(data=musical_preferences, x="liveness"  
            , hue="username",  cut=0, fill=True, 
            ax=axs[1,1]).set_title('Liveness Differences')

fig.tight_layout()


##Third batch of plots#####
fig, axs = plt.subplots(2, 2, figsize=(12, 6), gridspec_kw=dict(width_ratios=[6, 6]))
fig.suptitle('Music Features Differences- 3')

sns.kdeplot(data=musical_preferences, x="duration_ms"  ,
             hue="username",  cut=0, fill=True, 
            ax=axs[0,0]).set_title('Duration Differences')

sns.kdeplot(data=musical_preferences, x="tempo"  
            , hue="username",  cut=0, fill=True, 
            ax=axs[0,1]).set_title('Tempo Differences*')

sns.kdeplot(data=musical_preferences, x="speechiness"  ,
             hue="username",  cut=0, fill=True, 
            ax=axs[1,0]).set_title('Speechiness Differences*')


fig.tight_layout()



