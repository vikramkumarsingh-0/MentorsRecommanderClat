import streamlit as st
import pandas as pd
from mentor_recommender import MentorRecommender

# Page setup
st.set_page_config(page_title="CLAT Mentor Recommender", layout="wide")
st.title("CLAT Mentor Recommendation System")

# Load mentor data
@st.cache_data
def load_data():
    return pd.read_csv("mentors.csv")

mentor_df = load_data()
recommender = MentorRecommender(n_neighbors=20)
recommender.fit(mentor_df)

# Sidebar filters
st.sidebar.header("Your Preferences")

# Extract unique options
all_subjects = sorted(set(val.strip() for sublist in mentor_df["Expertise"].dropna().str.split(",") for val in sublist))
all_colleges = sorted(mentor_df["Alma Mater"].dropna().unique())
all_styles = sorted(set(val.strip() for sublist in mentor_df["Teaching Approach"].dropna().str.split(",") for val in sublist))

preferred_subjects = st.sidebar.multiselect("Preferred Subjects", all_subjects)
target_colleges = st.sidebar.multiselect("Target Law Colleges", all_colleges)
learning_styles = st.sidebar.multiselect("Preferred Learning Style", all_styles)

# Logic
if st.sidebar.button("🔎 Find Mentors"):
    try:
        recommendations = recommender.recommend(preferred_subjects, target_colleges, learning_styles)

        if recommendations.empty:
            st.warning("No mentors found matching your preferences. Try broadening your filters.")
        else:
            top_matches = recommendations.sort_values(by="Match Score", ascending=False).head(3)
            st.success(f"Top {len(top_matches)} best matching mentor(s) found.")
            st.dataframe(
                top_matches[["Name", "Expertise", "Alma Mater", "Teaching Approach"]],
                use_container_width=True
            )
    except Exception as e:
        st.error(f"❌ An error occurred while generating recommendations: {e}")
else:
    st.info("Select your preferences from the sidebar and click 'Find Mentors' to get started.")
