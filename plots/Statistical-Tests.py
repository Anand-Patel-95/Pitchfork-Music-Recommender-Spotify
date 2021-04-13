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
"""
How different is our team members musical preferences?

--Musical differences are difficult to asses, but spotify provides a number of features for each track that can be
used to compare musical differences between each team member
"""

""" 
Make two grid plots- 
- For Numerical Variables
---One comparing the distributions for each member given the variable in question 
---Another one making the box plots for each member given the variable in question 

- Deliverables
---Table of statistical test for each one of the numerical variables
---Analysis of the characteristics that have more impact in our musical preferences

Kruskal-Wallis H-test
https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.kruskal.html
The Kruskal-Wallis H-test tests the null hypothesis that the population median of all of the groups are equal.
 It is a non-parametric version of ANOVA. The test works on 2 or more independent samples,
 which may have different sizes. 

"""

##Numerical Variables used in this section
analysis_variables= ['username']
numerical_variables= tracks.dtypes[tracks.dtypes== 'float64']
numerical_variables= list(numerical_variables.index)
[analysis_variables.append(i) for i in numerical_variables]
analysis_variables.append('popularity')
analysis_variables.append('duration_ms')


##General dataset of numerical variables
musical_preferences = tracks[analysis_variables]

##Analysis Variables by username
LinaTracks= tracks[tracks['username']=='Lina'][analysis_variables]
AndresTracks= tracks[tracks['username']=='Andres'][analysis_variables]
AnandTracks= tracks[tracks['username']=='Anand'][analysis_variables]

##For each one of our numerical variables
stats.kruskal(LinaTracks.iloc[:,1], AndresTracks.iloc[:,1], AnandTracks.iloc[:,1])


def create_p_value_table():
    p_value_results= {}
    for i in range(1,len(analysis_variables)):
        p_value=stats.kruskal(LinaTracks.iloc[:,i],
                              AndresTracks.iloc[:,i],
                              AnandTracks.iloc[:,i])[1]
        p_value_results[analysis_variables[i]] = p_value
    return p_value_results

Kruskal_Results= pd.DataFrame(create_p_value_table(), index=[0]).T
Kruskal_Results= Kruskal_Results.reset_index()
Kruskal_Results.columns = ['characteristic', 'P-Value']

##Adding the conclusion based on a significant level of 0.05
Kruskal_Results['Conclusion-KW'] = Kruskal_Results['P-Value']<0.05

"""
Create more variables such as, who listen to the most and least in each category- Andres doesnt like
songs with explicit contain. 

Think about putting images on the presentation
"""

song_matrix= tracks
song_matrix.set_index('username')

def descriptive_matrix():
    maximun_value= {}
    minimun_value= {}
    for i in range(1,len(analysis_variables)):
        max_username_selection= musical_preferences.iloc[:,0][musical_preferences.iloc[:,i] == musical_preferences.iloc[:,i].max()].tolist()[0]
        min_username_selection= musical_preferences.iloc[:,0][musical_preferences.iloc[:,i] == musical_preferences.iloc[:,i].min()].tolist()[0]
        maximun_value[analysis_variables[i]] = max_username_selection
        minimun_value[analysis_variables[i]] = min_username_selection
    minimun_value= pd.DataFrame(minimun_value, index=['min_username']).T
    maximun_value= pd.DataFrame(maximun_value, index=['max_username']).T
    results_matrix= pd.merge(minimun_value, maximun_value, left_index=True, right_index=True)
    return results_matrix


results_matrixx = pd.DataFrame(descriptive_matrix())
results_matrixx= results_matrixx.reset_index()
results_matrixx.columns.values[0] = 'characteristic'
Kruskal_Results.columns.values[0] = 'characteristic'

#Don't know why this is not merging, but continue the analysis
final_matrix= pd.merge(results_matrixx, Kruskal_Results,on='characteristic')


final_matrix.to_csv('tabla_final.csv')
