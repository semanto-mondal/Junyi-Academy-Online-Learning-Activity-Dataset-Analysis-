import streamlit as st
import pandas as pd
import plotly.express as px

# Setting the title and page icon
st.set_page_config(page_title="Online Learning", page_icon=":books:", layout="wide")
st.title(':technologist: Online Learning Activity Data Analysis')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('C:/Users/monda/Downloads/Streamlit Dashboard of Juniya Online Learning/cleaned_data_sampled.csv')
    return data

# Load the dataset
data = load_data()

# Sidebar header
st.sidebar.header("Filters")

# UUID filter
uuid_options = data['uuid'].unique().tolist()
selected_uuid = st.sidebar.multiselect("Select UUID", options=uuid_options)


# Overall Analysis
st.subheader("Overall Analysis")

# Create two columns
col1, col2 = st.columns(2)

# Column 1: Pie plot for gender distribution and bar plot for learning stages
with col1:
    # Pie plot for gender distribution
    gender_distribution = data['gender'].value_counts()
    fig_gender = px.pie(gender_distribution, values=gender_distribution.values, names=gender_distribution.index,
                        title="Gender Distribution")
    st.plotly_chart(fig_gender)

    # Distribution of learning stages
    learning_stage_distribution = data['learning_stage'].value_counts().reset_index()
    learning_stage_distribution.columns = ['Learning Stage', 'Count']
    fig_learning_stage = px.bar(learning_stage_distribution, x='Learning Stage', y='Count', title='Distribution of Learning Stages')
    st.plotly_chart(fig_learning_stage)

# Column 2: Bar plot for number of students per year and distribution of difficulty
with col2:
    # Number of students per year
    students_per_year = data['year'].value_counts().reset_index()
    students_per_year.columns = ['Year', 'Number of Students']
    fig_year = px.bar(students_per_year, x='Year', y='Number of Students', title='Number of Students per Year')
    st.plotly_chart(fig_year)

    # Distribution of difficulty
    difficulty_distribution = data['difficulty'].value_counts().reset_index()
    difficulty_distribution.columns = ['Difficulty', 'Count']
    fig_difficulty = px.bar(difficulty_distribution, x='Difficulty', y='Count', title='Distribution of Difficulty Levels')
    st.plotly_chart(fig_difficulty)

# Full-width section for the top five students table
st.subheader("Top 5 Students Based on Total Points (Unique UUIDs)")

# Top five students based on total points (grouped by UUID)
top_students = data.groupby('uuid')['points'].sum().reset_index().nlargest(5, 'points')
st.write(top_students)


# Apply the filter based on the selection
if selected_uuid:
    filtered_data = data[data['uuid'].isin(selected_uuid)]
    
    # Output 1: Show the student's gender
    student_gender = filtered_data['gender'].iloc[0]  # Assuming same gender for one student
    st.write(f"**Student Gender:** {student_gender}")
    
    # Output 2: Show the year of enrollment
    enrollment_year = filtered_data['year'].iloc[0]
    st.write(f"**Year of Enrollment:** {enrollment_year}")
    
    # Output 3: Show the learning stage of the student
    learning_stage = filtered_data['learning_stage'].iloc[0]
    st.write(f"**Learning Stage:** {learning_stage}")
    
    # Output 4: Distribution of exercises solved based on difficulty (Bar plot)
    difficulty_distribution = filtered_data['difficulty'].value_counts().reset_index()
    difficulty_distribution.columns = ['Difficulty', 'Count']
    fig_difficulty = px.bar(difficulty_distribution, x='Difficulty', y='Count', title='Distribution of Exercises by Difficulty')
    st.plotly_chart(fig_difficulty)
    
    # Output 5: Total points of the student
    total_points = filtered_data['points'].sum()
    st.write(f"**Total Points:** {total_points}")

    # Output 6: Total badges of the student
    total_badges = filtered_data['badges_cnt'].sum()
    st.write(f"**Total Badges:** {total_badges}")
    
    # Output 7: Total hints used by the student
    total_hints_used = filtered_data['used_hint_cnt'].sum()
    st.write(f"**Total Hints Used:** {total_hints_used}")
    
    # Output 8: Distribution of level of expertise (Bar plot)
    level_distribution = filtered_data['level'].value_counts().reset_index()
    level_distribution.columns = ['Level', 'Count']
    fig_level = px.bar(level_distribution, x='Level', y='Count', title='Distribution of Expertise Level')
    st.plotly_chart(fig_level)
    
    # Output 9: Number of correct and incorrect exercises (Bar plot)
    correct_distribution = filtered_data['is_correct'].value_counts().reset_index()
    correct_distribution.columns = ['Correct', 'Count']
    fig_correct = px.bar(correct_distribution, x='Correct', y='Count', title='Correct vs Incorrect Exercises')
    st.plotly_chart(fig_correct)

    st.subheader("Filtered Data")
    st.write(filtered_data)
    
else:
    st.write("Please select a UUID from the sidebar to view detailed statistics.")
