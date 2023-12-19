import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import time




def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    return data

def main():
    global geo

    st.title("Airbnb Paris Data Analysis September 2023")
    st.sidebar.success("Select a page above 👋🏼 !")

    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    data = load_data(uploaded_file)

    with st.spinner(text='In progress...'):
        time.sleep(3)

    st.subheader("Raw Data")
    st.write(data)


    ### PLOT 1 : Listings par arrondissement ###
    st.title('Number of Listings per Neighbourhood')
    grouped_data = data[["id", "neighbourhood"]].groupby("neighbourhood").count().sort_values(by="id", ascending=False)

    bar_chart = alt.Chart(grouped_data.reset_index()).mark_bar().encode(
            y=alt.Y('neighbourhood:N', title='Neighbourhood', sort='-x'),
            x=alt.X('id:Q', title='Number of Listings')
        ).properties(
            width=900,
            height=700
        )
    st.altair_chart(bar_chart, use_container_width=True)
        
    
    #### PLOT 2 : Moyenne des prix par arrondissements ###
    data['price'] = data['price'].replace('[\$,]', '', regex=True).astype(float)
    data['price_eur'] = data['price'] * 0.94
    moyennes_prix_par_arrondissement = data.groupby('neighbourhood')['price_eur'].mean()
    moyennes_prix_df = moyennes_prix_par_arrondissement.reset_index()
    mean_price_arr = round(moyennes_prix_df, 0)
    mean_price_arr = mean_price_arr.sort_values(by='price_eur', ascending=False)

    st.title('Mean Daily Price per Neighbourhood')

    chart = alt.Chart(mean_price_arr).mark_bar().encode(
        y=alt.Y('neighbourhood:N', title='Arrondissements'),
        x=alt.X('price_eur:Q', title='Prix journalier moyen (EUR)')
    ).properties(width=800, height=600, title='Prix journalier moyen (EUR) par arrondissement')

    st.altair_chart(chart, use_container_width=True)



        
    ### PLOT 3 : Listings par room type ###
    st.title('Number of Listings per Room Type 🧑🏻‍🦰👨🏼‍🦰')
    grouped_data_2 = data.groupby("room_type").count().loc[:,"id"]

    bar_chart_2 = alt.Chart(grouped_data_2.reset_index()).mark_bar().encode(
            x=alt.X('room_type:N', title='Room Type'),
            y=alt.Y('id:Q', title='Number of listings')
            
        ).properties(
            width=900,
            height=700
        )
    st.altair_chart(bar_chart_2, use_container_width=True)



    ### GEOMAP JSON : Listings ###
    st.title("Visual Representation Listings ")
    st.map(data)

    # LINK JUPYTER NOTEBOOK
    st.subheader("Lien suite de l'analyse (Jupyter Notebook)") 
    jupyter_notebook_url = 'https://nbviewer.org/github/mdoyenblec/Airbnb-Paris-Analysis-Notebook/blob/main/notebook.ipynb'
    link_markdown = f'[Click here to open notebook]({jupyter_notebook_url})'
    st.markdown(link_markdown, unsafe_allow_html=True)


if __name__ == "__main__":
    main()



        
