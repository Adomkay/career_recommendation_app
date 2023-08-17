import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Loading necessary data files
occupation_data_df = pd.read_excel("Occupation Data.xlsx")
oip_transformed_df = pd.read_csv("oip_transformed.csv")

def calculate_riasec_scores(responses):
    riasec_mapping = {
        "R": [1, 2, 13, 24, 25, 26, 38, 49, 50, 60],
        "I": [3, 4, 15, 16, 28, 39, 40, 52, 53, 54],
        "A": [5, 6, 17, 18, 29, 30, 41, 42, 55, 56],
        "S": [7, 8, 19, 20, 31, 32, 43, 44, 57, 58],
        "E": [9, 10, 21, 22, 33, 34, 45, 46, 47, 59],
        "C": [11, 12, 14, 23, 27, 35, 36, 37, 48, 51]
    }
    riasec_scores = {key: sum(responses[val - 1] for val in values) for key, values in riasec_mapping.items()}
    return riasec_scores

def calculate_correlations(user_riasec_scores):
    user_scores_vector = np.array(list(user_riasec_scores.values()))
    correlations = {}
    for index, row in oip_transformed_df.iterrows():
        occupation_scores_vector = np.array([row['Realistic'], row['Investigative'], row['Artistic'], row['Social'], row['Enterprising'], row['Conventional']])
        correlation = np.corrcoef(user_scores_vector, occupation_scores_vector)[0, 1]
        occupation_code = row['O*NET-SOC Code']
        correlations[occupation_code] = correlation
    return correlations

def plot_charts(riasec_scores):
    categories = list(riasec_scores.keys())
    scores = list(riasec_scores.values())

    # Bar chart
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.bar(categories, scores)
    plt.xlabel('RIASEC Categories')
    plt.ylabel('Scores')
    plt.title('Interest Profile')

    # Radar chart
    plt.subplot(1, 2, 2, polar=True)
    angles = [n / 6 * 2 * np.pi for n in range(6)]
    scores += scores[:1]
    angles += angles[:1]
    plt.plot(angles, scores, linewidth=2)
    plt.fill(angles, scores, alpha=0.25)
    plt.title('Interest Profile')
    plt.xticks(angles[:-1], categories)

    st.pyplot()

def assessment():
    st.title("🧭 Jifunza Afrika")
    st.title("📝 Interest Assessment")
    st.write("""
    Please respond to the following 60 questions. Indicate your interest in each activity by selecting the appropriate option:
    - Strongly Dislike
    - Dislike
    - Unsure
    - Like
    - Strongly Like
    """)
    questions = [
        "Build kitchen cabinets", "Lay brick or tile", "Develop a new medicine", #... Add all 60 questions here
        "Study ways to reduce water pollution", "Write books or plays", "Play a musical instrument",
        "Teach an individual an exercise routine", "Help people with personal or emotional problems",
        "Buy and sell stocks and bonds", "Manage a retail store", "Develop a spreadsheet using computer software",
        "Proofread records or forms", "Repair household appliances", "Raise fish in a fish hatchery",
        "Conduct chemical experiments", "Study the movement of planets", "Compose or arrange music",
        "Draw pictures", "Give career guidance to people", "Perform rehabilitation therapy",
        "Operate a beauty salon or barber shop", "Manage a department within a large company",
        "Install software across computers on a large network", "Operate a calculator",
        "Assemble electronic parts", "Drive a truck to deliver packages to offices and homes",
        "Examine blood samples using a microscope", "Investigate the cause of a fire",
        "Create special effects for movies", "Paint sets for plays", "Do volunteer work at a non-profit organization",
        "Teach children how to play sports", "Start your own business", "Negotiate business contracts",
        "Keep shipping and receiving records", "Calculate the wages of employees", "Test the quality of parts before shipment",
        "Repair and install locks", "Develop a way to better predict the weather", "Work in a biology lab",
        "Write scripts for movies or television shows", "Perform jazz or tap dance",
        "Teach sign language to people who are deaf or hard of hearing", "Help conduct a group therapy session",
        "Represent a client in a lawsuit", "Market a new line of clothing", "Inventory supplies using a hand-held computer",
        "Record rent payment", "Set up and operate machines to make products", "Put out forest fires",
        "Invent a replacement for sugar", "Do laboratory tests to identify diseases", "Sing in a band",
        "Edit movies", "Take care of children at a day-care center", "Teach a high-school class",
        "Sell merchandise at a department store", "Manage a clothing store", "Keep inventory records",
        "Stamp, sort, and distribute mail for an organization"
    ]
    response_mapping = {"Strongly Dislike": 0, "Dislike": 1, "Unsure": 2, "Like": 3, "Strongly Like": 4}
    responses = [st.selectbox(question, list(response_mapping.keys())) for question in questions]
    responses_scores = [response_mapping[response] for response in responses]
    riasec_scores = calculate_riasec_scores(responses_scores)
    st.subheader("Your RIASEC Scores")
    st.write(riasec_scores)

    plot_charts(riasec_scores)
    
    correlations = calculate_correlations(riasec_scores)
    sorted_correlations = sorted(correlations.items(), key=lambda x: x[1], reverse=True)

    num_recommendations = st.selectbox("Select the number of recommended occupations to display:", options=range(1, 21), index=4)

    top_recommendations = sorted_correlations[:num_recommendations]

    st.subheader(f"Top {num_recommendations} Recommended Occupations")
    recommended_data = []
    for occupation_code, correlation in top_recommendations:
        occupation_row = occupation_data_df[occupation_data_df['O*NET-SOC Code'] == occupation_code].iloc[0]
        occupation_name = occupation_row['Title']
        description = occupation_row['Description']
        recommended_data.append([occupation_name, description])

    recommended_df = pd.DataFrame(recommended_data, columns=['Occupation', 'Description'])
    st.table(recommended_df)

# App navigation
st.sidebar.title("🧭 Career Recommendation")
section = st.sidebar.radio("Choose a section:", ["📝 Interest Assessment"])

if section == "📝 Interest Assessment":
    assessment()
