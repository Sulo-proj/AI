import streamlit as st
# import pandas as pd
import pickle
import utils
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Configuration and Theme
st.set_page_config(page_title="News Impact Prediction System", layout="wide")
sns.set_theme(style="white", palette="muted")
st.title("Fin News Topic & Impact Prediction System")

# Cache data loading and heavy preprocessing
@st.cache_data
def get_processed_data():
    file_path = "IndianFinancialNews.csv"
    index_col = 'Unnamed: 0'
    df = utils.load_and_preprocess_data(file_path, index_col)
    
    # Load K-Means and Vectorizer
    loaded_vectorizer = pickle.load(open("final_vectorizer.sav", 'rb'))
    loaded_kmeans = pickle.load(open("kmeans.sav", 'rb'))
    
    # Efficient transform and labeling
    X_tfidf = loaded_vectorizer.transform(df['Cleaned_Desc']) # Use transform, not fit_transform
    df['Topic_Cluster'] = loaded_kmeans.predict(X_tfidf)
    
    topic_map = {0: "Markets", 1: "Policy", 2: "Earnings", 3: "Rates", 4: "Insurance", 5: "Banks"}
    df['Topic_Label'] = df['Topic_Cluster'].map(topic_map)
    
    # Apply impact logic
    df['Impact_name'] = df.apply(lambda row: utils.impact_label(row['Cleaned_Desc'], row['Topic_Label']), axis=1)
    df['Year'] = df['Date'].dt.year
    df['Day_Name'] = df['Date'].dt.day_name()
    return df

# Cache model loading
@st.cache_resource
def load_prediction_models():
    vec = pickle.load(open("model_vectorizer.sav", 'rb'))
    model = pickle.load(open("final_model.sav", 'rb'))
    return vec, model

dataset = get_processed_data()
model_vectorizer, final_model = load_prediction_models()

tab_dataset, tab_impact, tab_visualizations = st.tabs(["Dataset", "Impact Prediction", "Visualizations"])

with tab_dataset:
    st.subheader("News Dataset")
    # Unified display configuration
    st.dataframe(
        dataset[["Date", 'Title', "Description", "Topic_Label", "Impact_name"]], 
        hide_index=True,
        column_config={
            "Date": st.column_config.DateColumn("Date", format="DD-MMM-YYYY"),
            "Title": st.column_config.TextColumn("Title"),
            "Description": st.column_config.TextColumn("Description", width="large")
        }
    )

with tab_impact:
    st.subheader("Predicting News Impact")
    user_input = st.text_input("Enter news description:", value="say bank would provide information matter cbi couple day")

    if st.button("Predict Impact"):
        single_vec = model_vectorizer.transform([user_input])
        prediction = final_model.predict(single_vec)
        res = "High Impact" if prediction[0] == 1 else "Routine"
        st.success(f"Predicted Impact: **{res}**")

with tab_visualizations:
    st.subheader("News Analysis Dashboard")
    
    # Row 1: Global Distributions
    c1, c2 = st.columns(2)
    with c1:
        fig1, ax1 = plt.subplots()
        sns.countplot(data=dataset, x='Impact_name', ax=ax1, hue='Impact_name', legend=False)
        st.pyplot(fig1)
    with c2:
        fig2, ax2 = plt.subplots()
        counts = dataset['Topic_Label'].value_counts()
        ax2.pie(counts, labels=counts.index, autopct='%.0f%%')
        st.pyplot(fig2)

    # Row 2: Temporal Trends
    st.subheader("Yearly Topic Trends")
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    sns.countplot(data=dataset, x='Year', hue='Topic_Label', ax=ax3)
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # Row 3: Relationship Analysis
    c3, c4 = st.columns(2)
    with c3:
        st.subheader("Topics vs. Impact")
        fig4, ax4 = plt.subplots()
        sns.countplot(data=dataset, x='Topic_Label', hue='Impact_name', ax=ax4)
        plt.xticks(rotation=45)
        st.pyplot(fig4)
    with c4:
        st.subheader("Weekly Patterns")
        fig5, ax5 = plt.subplots()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        sns.countplot(data=dataset, x='Day_Name', hue='Impact_name', order=days, ax=ax5)
        plt.xticks(rotation=45)
        st.pyplot(fig5)

    # Row 4: Text Content
    st.subheader("Keyword Word Cloud")
    text = " ".join(dataset['Cleaned_Desc'].dropna().iloc[::50])
    wc = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig6, ax6 = plt.subplots(figsize=(10, 5))
    ax6.imshow(wc, interpolation='bilinear')
    ax6.axis("off")
    st.pyplot(fig6)