import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt 

def clean_countries(categories, cutoff):
   categ_map = {}
   for i in range(len(categories)):
      if categories.values[i] >= cutoff:
         categ_map[categories.index[i]] = categories.index[i]
      else:
         categ_map[categories.index[i]] = "Other"
   return categ_map

def clean_experience(x):
   if x == "More than 50 years":
      return 50
   if x == "Less than 1 year":
      return 0.5
   return float(x)


def clean_education(x):
   if "Bachelor's degree" in x:
      return "Bachelor's Degree"
   if "Master's degree" in x:
      return "Master's degree"
   if "Professional degree" in x:
      return "Post grad"
   return "Less than a Bachelors"

# caching
@st.cache_data
def load_data():
   df = pd.read_csv("survey_results_public.csv")
   df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
   df = df.rename({"ConvertedCompYearly" : "Salary"}, axis = 1)
   df = df.rename({"YearsCodePro" : "Experience"}, axis = 1)
   df = df[df["Salary"].notnull()]
   df = df.dropna()
   df = df[df["Employment"] == "Employed, full-time"]
   df = df.drop("Employment", axis = 1)

   countries = clean_countries(df.Country.value_counts(), 400)
   df['Country'] = df["Country"].map(countries)
   df.Country.value_counts()
   df = df[df["Country"] != "Other"]

   df["Experience"] = df["Experience"].apply(clean_experience)
   df["EdLevel"] = df["EdLevel"].apply(clean_education)
   return df 

df = load_data()

def show_explore_page():
   st.title("Explore Software Engineer Salaries")
   st.write(
      """
      ### Stack Overflow Developer Survey 2023
      """
   )
   data = df["Country"].value_counts()
   fig1, ax1 = plt.subplots()
   ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
   ax1.axis("equal") # for circle

   st.write("""#### Number of Data from different Countries""")
   st.pyplot(fig1)

   st.write("""### Mean Salary Based On Country""")
   data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
   st.bar_chart(data)
   
   st.write("""### Mean Salary Based On Experience""")
   data = df.groupby(["Experience"])["Salary"].mean().sort_values(ascending=True)
   st.line_chart(data)
