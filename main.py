import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# set page config
st.set_page_config(page_title = "Data Visualiser", layout="centered",page_icon="📊 ")

#title 
st.title(" 📊 - Data Visualiser Application")

# getting working dir
workingdir = os.path.dirname(os.path.abspath(__file__))

# getting folder path
folderpath = f"{workingdir}/dataVisualiser/data"

# list of files present in "data" folder
files = [fil for fil in os.listdir(folderpath) if fil.endswith(".csv")]

# creating a dropdown for selecting files
selected_file = st.selectbox("Select a file", files, index=None)

st.write(selected_file)

# operations after selecting the file: locating, reading etc

if selected_file:
    # get the comp path
    file_path = os.path.join(folderpath,selected_file)

    # reading the csv file as a df
    df = pd.read_csv(file_path)

    col1, col2 =st.columns(2)

    columns = df.columns.tolist()

    with col1:
        st.write("")
        st.write(df.head())

    with col2:
        #user selection of df columns
        x_axis = st.selectbox("Select x-axis",options=columns+ ["None"],index=None)
        y_axis = st.selectbox("Select y-axis",options=columns+ ["None"],index=None)

        # select the type of plot 
        plot_list = ["Correlation Matrix","Pair plot", "Line plot", "Bar chart", "Scatter plot", "Distribution plot", "Count plot"]

        selected_plot = st.selectbox("Select a plot", options=plot_list,index=None)

        #st.write(x_axis)
        #st.write(y_axis)
        #st.write(selected_plot)

    if st.button("Generate Plot"):
        if selected_plot == "Correlation Matrix":
            numeric_df = df.select_dtypes(include=['float64', 'int64'])  # Selecting only numeric columns
            st.write("Correlation Matrix:")
            st.write(numeric_df.corr())

            # Plot heatmap
            st.write("Heatmap:")
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='Blues', fmt=".2f", linewidths=.5, ax=ax)
            st.pyplot(fig)

        elif selected_plot == "Pair plot":
            st.write("Pairplot:")
            st.pyplot(sns.pairplot(df))

        else:
            fig, ax = plt.subplots(figsize=(6, 4))

            if selected_plot == "Line plot":
                sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)

            elif selected_plot == "Scatter plot":
                sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)

            elif selected_plot == "Bar chart":
                sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)

            elif selected_plot == "Distribution plot":
                sns.histplot(x=df[x_axis], kde=True, ax=ax)

            elif selected_plot == "Count plot":
                sns.countplot(x=df[x_axis], ax=ax)

            # adjust label sizes
            ax.tick_params(axis="x", labelsize=10)
            ax.tick_params(axis="y", labelsize=10)

            # title axis labels
            plt.title(f"{selected_plot} of {y_axis} and {x_axis}", fontsize=12)
            plt.xlabel(x_axis, fontsize=10)
            plt.ylabel(y_axis, fontsize=10)

            st.pyplot(fig)


