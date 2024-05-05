#import the required libraries 

import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px  

st.image("https://i0.wp.com/gbsn.org/wp-content/uploads/2020/07/AUB-logo.png?ssl=1")

#Welcome Message 

st.title('Students Performance Dashboard')
st.write('## "This dashboard allows the instructors to visually moniter that performance of students using several metrics and across multiple attributes" ')
# streamlit expander, useful if mor info is wanted about something but
# you dont want to clutter the page up
st.write("### Quick Guide: You can check students performance across the attributes by selecting the attribute from the side bar on the left, and read more info about the dataset and see a sample using the buttons below:")
with st.expander("Click for more information on the student performence dataset:"):
    st.write("The student performence data set is a multivariate data set that represents students scores across 3 subjects, Math, reading, and writing, and ever student belongs to one of the 5 groups: A, B, C, D, or E")
    st.write("The data set consists of 990 students.")

#loading the data set from google drive 
url = "https://drive.google.com/file/d/1hQWxWvBo_e8Kk5xnP4RnItm_M5eUC9Ep/view?usp=sharing"
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)

attribute = st.sidebar.radio('Which Attribute?',
                 ('Groups', 'Gender',
                  'Pass/Fail', 'Subject Averages'))
    

#drop unnecessary columns
df.drop(columns = ['parental level of education', 'lunch', 'test preparation course'], inplace = True)

#create age and total columns 
df['total'] = df['math score'] + df['reading score'] + df['writing score']
df['age'] = np.random.randint(11,17, size = len(df))

if st.button('Show a sample of the data'):
    st.write(df.head())

#calculate the total score of each group
a_total = df.loc[df['team'] == 'group A', 'total'].sum()
b_total = df.loc[df['team'] == 'group B', 'total'].sum()
c_total = df.loc[df['team'] == 'group C', 'total'].sum()
d_total = df.loc[df['team'] == 'group D', 'total'].sum()
e_total = df.loc[df['team'] == 'group E', 'total'].sum()

scores_data = {'Name': ['Group A', 'Group B', 'Group C', 'Group D', 'Group E'], 'Total Scores': [a_total, b_total, c_total, d_total, e_total]}
scores_df = pd.DataFrame(scores_data)

#create scores bar chart 
scores_bar_chart = px.bar(scores_df, x='Name', y='Total Scores', color='Name', title='Students Total Scores in Each Group',
      labels={'Name': 'Group Name', 'Student Total': 'Group Total Score'})

#calculate the total number of students in each group
a_total_students = df.loc[df['team'] == 'group A', 'name'].count()
b_total_students = df.loc[df['team'] == 'group B', 'name'].count()
c_total_students = df.loc[df['team'] == 'group C', 'name'].count()
d_total_students = df.loc[df['team'] == 'group D', 'name'].count()
e_total_students = df.loc[df['team'] == 'group E', 'name'].count()

bubble_data = {'Name': ['Group A', 'Group B', 'Group C', 'Group D', 'Group E'], 'Student Total': [a_total_students, b_total_students, c_total_students, d_total_students, e_total_students]}
bubble_df = pd.DataFrame(bubble_data)

#create pie chart of the total number of students
total_number_pie_chart = px.pie(bubble_df, values='Student Total', names='Name', title ='Total Number of Students in each group')

student_bar_chart = px.bar(bubble_df, x='Name', y='Student Total', color='Name', title='Number of Students in Each Group',
      labels={'Name': 'Group Name', 'Student Total': 'Group Size'})


if attribute == 'Groups':
    st.balloons()
    st.subheader('Students Total Scores in Each Group')
    st.plotly_chart(scores_bar_chart)
    st.subheader('Total Number of Students in Each Group')

    choice1 = st.radio('What type of Chart?', ('Pie Chart', 'Bar Chart'))
    if choice1 == 'Bar Chart':
        st.plotly_chart(student_bar_chart)
    elif choice1 == 'Pie Chart':
        st.plotly_chart(total_number_pie_chart)


# setting a passing mark for the students to pass on the three subjects individually
passmarks = 50

# creating a new column pass_math, this column will tell us whether the students are pass or fail
df['pass_math'] = np.where(df['math score']< passmarks, 'Fail', 'Pass')
df['pass_reading'] = np.where(df['reading score']< passmarks, 'Fail', 'Pass')
df['pass_writing'] = np.where(df['writing score']< passmarks, 'Fail', 'Pass')

# pie chart to represent the ratio of pass and fail status between the students
size = df['pass_writing'].value_counts()
labels = "pass", "fail"
explode = [0, 0.2]

writing_chart_grades = px.pie(data_frame = df, values = size, names = labels, color_discrete_sequence=px.colors.sequential.Oryel)
writing_chart_grades.update_traces(textposition='inside', textinfo='label+percent', pull = explode, title = 'Students Result for Writing')

size_math = df['pass_math'].value_counts()

pie_chart_grades = px.pie(data_frame = df, values = size_math, names = labels, color_discrete_sequence=px.colors.sequential.Darkmint)
pie_chart_grades.update_traces(textposition='inside', textinfo='label+percent', pull = explode, title = 'Students Result for Maths')

size_reading = df['pass_reading'].value_counts()
explode = [0, 0.2]


reading_chart_grades = px.pie(data_frame = df, values = size_reading, names = labels, color_discrete_sequence=px.colors.sequential.Pinkyl)
reading_chart_grades.update_traces(textposition='inside', textinfo='label+percent', pull = explode, title = 'Students Result for Reading')

pass_mark = 150
df['pass'] = np.where(df['total']< pass_mark, 'Fail', 'Pass')
sizee = df['pass'].value_counts()
labels = "pass", "fail"
explode = [0, 0.2]

pass_fail_pie = px.pie(data_frame = df, values = sizee, names = labels, color_discrete_sequence=px.colors.sequential.Cividis)
pass_fail_pie.update_traces(textposition='inside', textinfo='label+percent', pull = explode, title = 'Failing and Passing Students in Total Score')


if attribute == 'Pass/Fail':
    st.balloons()
    st.subheader('Total Ratio of the Passing and Failing Students')
    st.plotly_chart(pass_fail_pie)
    st.subheader('Passing and Fail Ratio in every subject')
    select_subject = st.selectbox("Which Subject?", ('Math', 'Reading', 'Writing'))
    if select_subject == 'Math':
        st.plotly_chart(pie_chart_grades)
    elif select_subject == 'Reading':
        st.plotly_chart(reading_chart_grades)
    elif select_subject == 'Writing':
        st.plotly_chart(writing_chart_grades)

gender_size = df['gender'].value_counts()
labelss = 'Female', 'Male'
gender_prop = px.pie(data_frame = df, values = gender_size, names = labelss, color_discrete_sequence=px.colors.sequential.Pinkyl)
gender_prop.update_traces(textposition='inside', textinfo='label+percent', pull = explode, title = 'Gender Proprtions in all groups')

df_group_a = df[df['team'] == 'group A']
gender_size_a = df_group_a['gender'].value_counts()
labelss = 'Female', 'Male'
gender_prop_a = px.pie(data_frame = df_group_a, values = gender_size_a, names = labelss, color_discrete_sequence=px.colors.sequential.Agsunset_r)
gender_prop_a.update_traces(textposition='inside', textinfo='label+percent', pull = explode, title = 'Gender Proprtions in group A')

df_group_b = df[df['team'] == 'group B']
gender_size_b = df_group_b['gender'].value_counts()
labelss = 'Female', 'Male'
gender_prop_b = px.pie(data_frame = df_group_b, values = gender_size_b, names = labelss, color_discrete_sequence=px.colors.sequential.Agsunset)
gender_prop_b.update_traces(textposition='inside', textinfo='label+percent', pull = explode, title = 'Gender Proprtions in group B')

df_group_c = df[df['team'] == 'group C']
gender_size_c = df_group_c['gender'].value_counts()
labelss = 'Female', 'Male'
gender_prop_c= px.pie(data_frame = df_group_c, values = gender_size_c, names = labelss, color_discrete_sequence=px.colors.sequential.Bluered)
gender_prop_c.update_traces(textposition='inside', textinfo='label+percent', pull = explode, title = 'Gender Proprtions in group C')

df_group_d = df[df['team'] == 'group D']
gender_size_d = df_group_d['gender'].value_counts()
labelss = 'Female', 'Male'
gender_prop_d= px.pie(data_frame = df_group_d, values = gender_size_d, names = labelss, color_discrete_sequence=px.colors.sequential.BuGn)
gender_prop_d.update_traces(textposition='inside', textinfo='label+percent', pull = explode, title = 'Gender Proprtions in group D')

df_group_e = df[df['team'] == 'group E']
gender_size_e = df_group_e['gender'].value_counts()
labelss = 'Female', 'Male'
gender_prop_e= px.pie(data_frame = df_group_e, values = gender_size_e, names = labelss, color_discrete_sequence=px.colors.sequential.Brwnyl)
gender_prop_e.update_traces(textposition='inside', textinfo='label+percent', pull = explode, title = 'Gender Proprtions in group E')



if attribute == "Gender":
    st.balloons()
    st.subheader('Gender Ratio Across All Groups')
    st.plotly_chart(gender_prop)
    st.subheader('Gender Ratio Across Each Groups')
    select_group = st.selectbox("Which Group?", ('Group A', 'Group B', 'Group C', 'Group D', 'Group E'))
    if select_group == 'Group A':
        st.plotly_chart(gender_prop_a)
    elif select_group == 'Group B':
        st.plotly_chart(gender_prop_b)
    elif select_group == 'Group C':
        st.plotly_chart(gender_prop_c)
    elif select_group == 'Group D':
        st.plotly_chart(gender_prop_d)
    elif select_group == 'Group E':
        st.plotly_chart(gender_prop_e)

if attribute == 'Subject Averages':
    st.balloons()
    st.subheader('Average Grade by Subject')
    cols = st.columns(4)
    cols[0].metric("Math Average", value=df['math score'].mean().astype(int))
    cols[1].metric("Writing Average", value=df['writing score'].mean().astype(int))
    cols[2].metric("Reading Average", value=df['reading score'].mean().astype(int))
    cols[3].metric("Total Average", value=df['total'].mean().astype(int))
    st.subheader('Average Grades By Subject for Each Group')

    team_a = df[df['team'] == 'group A']
    team_b = df[df['team'] == 'group B']
    team_c = df[df['team'] == 'group C']
    team_d = df[df['team'] == 'group D']
    team_e = df[df['team'] == 'group E']
    st.subheader('Group A')
    with st.expander("Click for more information on the Average Grades By Subject for Group A"):
        coll =st.columns(4)
        coll[0].metric("Group A Math Average", value=team_a['math score'].mean().astype(int))
        coll[1].metric("Group A Writing Average", value=team_a['writing score'].mean().astype(int))
        coll[2].metric("Group A Reading Average", value=team_a['reading score'].mean().astype(int))
        coll[3].metric("Group A Total Average", value=team_a['total'].mean().astype(int))
    
    st.subheader('Group B')
    with st.expander("Click for more information on the Average Grades By Subject for Group A"):
        coll =st.columns(4)
        coll[0].metric("Group B Math Average", value=team_b['math score'].mean().astype(int))
        coll[1].metric("Group B Writing Average", value=team_b['writing score'].mean().astype(int))
        coll[2].metric("Group B Reading Average", value=team_b['reading score'].mean().astype(int))
        coll[3].metric("Group B Total Average", value=team_b['total'].mean().astype(int))

    st.subheader('Group C')
    with st.expander("Click for more information on the Average Grades By Subject for Group C"):
        coll =st.columns(4)
        coll[0].metric("Group C Math Average", value=team_c['math score'].mean().astype(int))
        coll[1].metric("Group C Writing Average", value=team_c['writing score'].mean().astype(int))
        coll[2].metric("Group C Reading Average", value=team_c['reading score'].mean().astype(int))
        coll[3].metric("Group C Total Average", value=team_c['total'].mean().astype(int))
    
    st.subheader('Group D')
    with st.expander("Click for more information on the Average Grades By Subject for Group D"):
        coll =st.columns(4)
        coll[0].metric("Group D Math Average", value=team_d['math score'].mean().astype(int))
        coll[1].metric("Group D Writing Average", value=team_d['writing score'].mean().astype(int))
        coll[2].metric("Group D Reading Average", value=team_d['reading score'].mean().astype(int))
        coll[3].metric("Group D Total Average", value=team_d['total'].mean().astype(int))

    st.subheader('Group E')
    with st.expander("Click for more information on the Average Grades By Subject for Group E"):
        coll =st.columns(4)
        coll[0].metric("Group E Math Average", value=team_e['math score'].mean().astype(int))
        coll[1].metric("Group E Writing Average", value=team_e['writing score'].mean().astype(int))
        coll[2].metric("Group E Reading Average", value=team_e['reading score'].mean().astype(int))
        coll[3].metric("Group E Total Average", value=team_e['total'].mean().astype(int))
    


