import streamlit as st
import pandas as pd

st.title("Lead Prioritization Demo – 3D In-Vitro Models")

file = st.file_uploader("Upload Lead CSV", type=["csv"])

def score_row(row):
    score = 0
    if any(x in row['Title'].lower() for x in ['toxicology', 'safety', '3d']):
        score += 30
    if row['FundingStage'] in ['Series A', 'Series B']:
        score += 20
    if 'in-vitro' in row['Keywords'].lower():
        score += 15
    if row['Location'] in ['Boston', 'Cambridge', 'Bay Area', 'UK']:
        score += 10
    if row['RecentPaper'] == 'Yes':
        score += 40
    return min(score, 100)

if file:
    df = pd.read_csv(file)
    df['Probability Score'] = df.apply(score_row, axis=1)
    df = df.sort_values(by='Probability Score', ascending=False)

    search = st.text_input("Search (Location / Keyword)")
    if search:
        df = df[df.apply(lambda r: search.lower() in r.astype(str).str.lower().to_string(), axis=1)]

    st.dataframe(df)
    st.download_button("Download CSV", df.to_csv(index=False), "ranked_leads.csv")
