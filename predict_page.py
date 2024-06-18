import streamlit as st 
import pickle 
import numpy as np


def load_model():
   with open("saved_steps.pkl", "rb") as file:
      data = pickle.load(file)
   return data 

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

#    ### is h3 markdown
def show_predict_page():
   st.title("Welcome To Software Developer Salary Prediction App")
   st.write("""### we need some information to predict the salary""")

   countries = {
      "India",
      "Australia",
      "Brazil",
      "Canada",
      "Denmark",
      "France",
      "Germany",
      "Israel",
      "Italy",
      "Netherlands",
      "Norway",
      "Poland",
      "Spain",
      "Sweden",
      "Switzerland",
      "United Kingdom of Great Britain and Northern Ireland",
      "United States of America"
   }

   education = {
      "Less than a Bachelors",
      "Master's degree",
      "Post grad",
      # "Student"
   }
   country = st.selectbox("Country", countries)
   education = st.selectbox("Education", education)
   experience = st.slider("Years of Experience", 0, 50, 3)

   ok = st.button("Predict Salary")
   if ok:
      x = np.array([[country, education, experience]])
      x[:, 0] = le_country.transform(x[:, 0])
      x[:, 1] = le_education.transform(x[:, 1])
      x = x.astype(float)

      salary = regressor.predict(x)
      st.subheader(f"The estimated salary is ${salary[0]:.2f}")
