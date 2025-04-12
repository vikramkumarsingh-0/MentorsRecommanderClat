import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

class MentorRecommender:
    def __init__(self, n_neighbors=5):
        self.n_neighbors = n_neighbors
        self.df = None

    def fit(self, df):
        self.df = df.copy()

    def filter_mentors(self, preferred_subjects, target_colleges, learning_styles):
        df_filtered = self.df.copy()

        if preferred_subjects:
            df_filtered = df_filtered[df_filtered["Expertise"].str.contains('|'.join(preferred_subjects), case=False, na=False)]
        if target_colleges:
            df_filtered = df_filtered[df_filtered["Alma Mater"].isin(target_colleges)]
        if learning_styles:
            df_filtered = df_filtered[df_filtered["Teaching Approach"].str.contains('|'.join(learning_styles), case=False, na=False)]

        return df_filtered

    def recommend(self, preferred_subjects, target_colleges, learning_styles):
        df_filtered = self.df.copy()

        def score(row):
            score = 0
            score += sum(subj.strip() in row['Expertise'] for subj in preferred_subjects)
            score += sum(col in row['Alma Mater'] for col in target_colleges)
            score += sum(style.strip() in row['Teaching Approach'] for style in learning_styles)
            return score

        df_filtered["Match Score"] = df_filtered.apply(score, axis=1)

        df_filtered = df_filtered[df_filtered["Match Score"] > 0]  # to keep non-zero scores
        return df_filtered.sort_values(by="Match Score", ascending=False)

