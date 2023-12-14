import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def q4_distribution(df):
    '''
    This function takes in a dataframe and plot the distribution of amount of IP addresses belong to users
    '''
    # Creating a dataframe with unique user id and each id's IP address amount
    ip = pd.DataFrame(df.groupby('user').ip.nunique(), columns = ['ip'])
    # Visualize distribution
    kwargs = dict(hist_kws={'alpha':.6}, kde_kws={'linewidth':2})
    plt.figure(figsize=(16,8), dpi= 80)
    plt.title('IP Address Amount per User Distribution')
    sns.distplot(x=ip['ip'], **kwargs, color = '#004987')

def q4_upperbound(df):
    '''
    This funciton prints out the upper_bound of the IP address amount
    '''
    # Creating a dataframe with unique user id and each id's IP address amount
    ip = pd.DataFrame(df.groupby('user').ip.nunique(), columns = ['ip'])
    q1 = ip['ip'].quantile(0.25)
    q3 = ip['ip'].quantile(0.75)
    iqr = q3-q1
    upper_bound = q3 + 3*iqr
    print('The upper bound of IP address amount is: ', upper_bound)

def q4_abnormal_ip(df):
    '''
    THis function plot the top 6 users with abnormal amount of IP address
    '''
    plt.figure(figsize = (16,16))
    plt.subplot(321)
    pages_228 = df[df.user == 228]['path'].resample('d').count()
    pages_228.plot(color = '#004B57')
    plt.title('User 228 Activity Over Time', fontsize = 20)

    plt.subplot(322)
    pages_843 = df[df.user == 843]['path'].resample('d').count()
    pages_843.plot(color = '#006A89')
    plt.title('User 843 Activity Over Time', fontsize = 20)

    plt.subplot(323)
    pages_690 = df[df.user == 690]['path'].resample('d').count()
    pages_690.plot(color = '#009AA2')
    plt.title('User 690 Activity Over Time', fontsize = 20)

    plt.subplot(324)
    pages_533 = df[df.user == 533]['path'].resample('d').count()
    pages_533.plot(color = '#008DC0')
    plt.title('User 533 Activity Over Time', fontsize = 20)

    plt.subplot(325)
    pages_226 = df[df.user == 226]['path'].resample('d').count()
    pages_226.plot(color = '#009DCF')
    plt.title('User 226 Activity Over Time', fontsize = 20)

    plt.subplot(326)
    pages_460 = df[df.user == 460]['path'].resample('d').count()
    pages_460.plot(color = '#86BEDA')
    plt.title('User 460 Activity Over Time', fontsize = 20)
    plt.tight_layout()

    
    
    
    
    
    
    
    
    
    
    
    
def one_user_df_prep(df, user):
    '''
    This function returns a dataframe consisting of data for only a single defined user
    '''
    df = df[df.user_id == user]
    pages_per_user = df['path'].resample('d').count()
    return pages_per_user

def compute_pct_b(pages_per_user, span, weight, user):
    '''
    This function adds the %b of a bollinger band range for the page views of a single user's log activity
    '''
    # Calculate upper and lower bollinger band
    midband = pages_per_user.ewm(span=span).mean()
    stdev = pages_per_user.ewm(span=span).std()
    ub = midband + stdev*weight
    lb = midband - stdev*weight
    
    # Add upper and lower band values to dataframe
    bb = pd.concat([ub, lb], axis=1)
    
    # Combine all data into a single dataframe
    my_df = pd.concat([pages_per_user, midband, bb], axis=1)
    my_df.columns = ['pages_per_user', 'midband', 'ub', 'lb']
    
    # Calculate percent b and relevant user id to dataframe
    my_df['pct_b'] = (my_df['pages_per_user'] - my_df['lb'])/(my_df['ub'] - my_df['lb'])
    my_df['user_id'] = user
    return my_df

def plot_bands(my_df, user):
    '''
    This function plots the bolliger bands of the page views for a single user
    '''
    fig, ax = plt.subplots(figsize=(12,8))
    ax.plot(my_df.index, my_df.pages_per_user, label='Number of Pages, User: '+str(user))
    ax.plot(my_df.index, my_df.midband, label = 'EMA/midband')
    ax.plot(my_df.index, my_df.ub, label = 'Upper Band')
    ax.plot(my_df.index, my_df.lb, label = 'Lower Band')
    ax.legend(loc='best')
    ax.set_ylabel('Number of Pages')
    plt.show()

def find_anomalies(df, user, span, weight, plot=False):
    '''
    This function returns the records where a user's daily activity exceeded the upper limit of a bollinger band range
    '''
    
    # Reduce dataframe to represent a single user
    pages_per_user = one_user_df_prep(df, user)
    
    # Add bollinger band data to dataframe
    my_df = compute_pct_b(pages_per_user, span, weight, user)
    
    # Plot data if requested (plot=True)
    if plot:
        plot_bands(my_df, user)
    
    # Return only records that sit outside of bollinger band upper limit
    return my_df[my_df.pct_b>1]

def q4_abnormal_users(df):
    '''
    This function plot the top 6 users with abnormal amount of page visit and abnormal activity patterns
    '''
    plt.figure(figsize = (20,20))
    plt.subplot(321)
    df_341 = one_user_df_prep(df, 341)
    df_341.plot(color = '#003F5D')
    plt.title('User 341 Activity Over Time', fontsize = 20)

    plt.subplot(322)
    df_138 = one_user_df_prep(df,138)
    df_138.plot(color = '#00527C')
    plt.title('User 341 Activity Over Time', fontsize = 20)

    plt.subplot(323)
    df_526 = one_user_df_prep(df,526)
    df_526.plot(color = '#00609C')
    plt.title('User 526 Activity Over Time', fontsize = 20)

    plt.subplot(324)
    df_658 = one_user_df_prep(df,658)
    df_658.plot(color = '#006DB2')
    plt.title('User 658 Activity Over Time', fontsize = 20)

    plt.subplot(325)
    df_521 = one_user_df_prep(df,521)
    df_521.plot(color = '#4E97D1')
    plt.title('User 521 Activity Over Time', fontsize = 20)

    plt.subplot(326)
    df_223 = one_user_df_prep(df,521)
    df_223.plot(color = '#7BB4E3')
    plt.title('User 223 Activity Over Time', fontsize = 20)
    plt.tight_layout()

def q5(df):
    '''
    This function takes in a dataframe and return 2 dataframes based on the program
    '''
    # create data science data frame
    ds = df[df.program_id == 3]
    # create program 1 web dev dataframe
    wd1 = df[df.program_id == 1]
    # create program 2 webdev data frame
    wd2 = df[df.program_id == 2]
    # concatenate both web dev data frames into one df
    wd = pd.concat([wd1, wd2])

    # return most popular web dev paths viewed
    return ds, wd
def q5_ds(ds):
    '''
    This function plots the data science access activity to web dep curriculum
    '''
    ds_pages = ds[(ds['path'] == 'java-i') | (ds['path'] == 'java-ii') | (ds['path'] == 'java-ii') | (ds['path'] == 'java-iii') | (ds['path'] == 'jquery')]['path'].resample('d').count()
    plt.figure(figsize = (12,6))
    ds_pages.plot(title='Data Science Student Access to Web Devlopment Curriculum', color = '#003B85')

def q5_wd(wd):
    '''
    This function plots the web devlopemnt student access activity to data science curriculum
    '''
    wd_pages = wd[(wd['path'] == 'classification/overview') | (wd['path'] == 'fundamentals/intro-to-data-science') | (wd['path'] == 'stats/compare-means')]['path'].resample('d').count()
    plt.figure(figsize = (12,6))
    wd_pages.plot(title='Web Development Student Access to Data Science Curriculum', color = '#f09c1a')
def q6(df):
    grads = pd.DataFrame(df[df.date>df.end_date].program.value_counts())
    grads = grads.reset_index()
    plt.figure(figsize=(16,8))
    sns.barplot(x=grads['program'], y=grads['count'],palette = 'mako')
    plt.title('Post Graduation Number of Logs per Program', fontsize = 20)
    plt.xlabel('Program', fontsize = 15)
    plt.ylabel('No. of Log Entry', fontsize = 15)
def q6_p1(df):
    '''
    This function visualize the most frequently visited topics for full stack java program
    '''
    p1 = pd.DataFrame(df[(df.date>df.end_date)&(df.program_id == 1)].path.value_counts().head(10))
    # Visualizing full stack java most frequent lesson
    p1 = p1.reset_index()
    plt.figure(figsize=(16,8))
    sns.barplot(x=p1['path'], y=p1['count'],palette = 'mako')
    plt.title('Most Frequently Visited Topics Post Graduation - Full Stack Java Program', fontsize = 20)
    plt.xlabel('No. of Log Entry', fontsize = 15)
    plt.ylabel('Topics', fontsize = 15)

def q6_p2(df):
    '''
    This function visualize the most frequently visited topics for full stack php program
    '''
    p2 = pd.DataFrame(df[(df.date>df.end_date)&(df.program_id == 2)].path.value_counts().head(10))
    # Visualizing full stack php most frequent lesson
    p2 = p2.reset_index()
    plt.figure(figsize=(16,8))
    sns.barplot(x=p2['path'], y=p2['count'],palette = 'mako')
    plt.title('Most Frequently Visited Topics Post Graduation - Full Stack PHP Program', fontsize = 20)
    plt.xlabel('Topics', fontsize = 15)
    plt.ylabel('No. of Log Entry', fontsize = 15)

def q6_p3(df):
    '''
    This function visualize the most frequently visited topics for data science program
    '''
    p3 = pd.DataFrame([ ['Anomaly Detection', 384],['MySQL', 275], ['Classification', 266], ['Feature Scaling', 219],
                  ['AL-ML-DL-timeline', 189], ['Modern_Data_Scientist.jpg', 187], ['Intro to Data Science', 184], ['SQL Database Design', 84]], columns = ['Lesson', 'Count'])
    
    # Visualizing full stack php most frequent lesson
    plt.figure(figsize=(20,8))
    sns.barplot(x=p3['Lesson'], y=p3['Count'],palette = 'mako')
    plt.title('Most Frequently Visited Topics Post Graduation - Data Science Program', fontsize = 20)
    plt.xlabel('Topics', fontsize = 15)
    plt.ylabel('No. of Log Entry', fontsize = 15)

def q6_p4(df):
    '''
    This function visualize the most frequently visited topics for front end program
    '''
    p4 = pd.DataFrame(df[(df.date>df.end_date)&(df.program_id == 4)].path.value_counts().head())
    p4 = p4.reset_index()
    # Visualizing full stack php most frequent lesson
    plt.figure(figsize=(16,8))
    sns.barplot(x=p4['path'], y=p4['count'],palette = 'mako')
    plt.title('Most Frequently Visited Topics Post Graduation - Front End Program', fontsize = 20)
    plt.xlabel('Topics', fontsize = 15)
    plt.ylabel('No. of Log Entry', fontsize = 15)

def q7_p1(df):
    '''
    This function visualize the topics that got accessed the least for web dep students
    '''
    wb_plot = pd.DataFrame([['JavaScript Working with Variables', 1], ['Java-i', 1], ['HTML', 1], ['HTML-CSS Introduction', 1], ['Environment Setup', 1], ['Coding Challenges', 1]], columns = ['Lesson', 'Count'])
    plt.figure(figsize=(16,8))
    sns.barplot(x=wb_plot['Lesson'], y=wb_plot['Count'],palette = 'mako')
    plt.title('Topics Accessed the Least - Web Development Programs', fontsize = 20)
    plt.xlabel('Topics', fontsize = 15)
    plt.ylabel('No. of Log Entry', fontsize = 15)

def q7_p2(df):
    '''
    This function visualize the topics that got accessed the least for data science students
    '''
    ds_plot = pd.DataFrame([['Introduction to Python', 1], ['Creating Charts',1], ['Case Statements', 1], ['ML Methodologies Drawing', 1], ['Tidy Data', 1], ['git/cli', 1], ['mySQL-Introduction', 1]], columns = ['Lesson', 'Count'])
    plt.figure(figsize=(16,8))
    sns.barplot(x=ds_plot['Lesson'], y=ds_plot['Count'],palette = 'mako')
    plt.title('Topics Accessed the Least - Data Science Programs', fontsize = 20)
    plt.xlabel('Topics', fontsize = 15)
    plt.ylabel('No. of Log Entry', fontsize = 15)