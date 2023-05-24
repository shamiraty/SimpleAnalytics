import streamlit as st
import pandas as pd 
import time


#page behaviour
st.set_page_config(page_title="Descriptive Analytics ", page_icon="🌎", layout="wide")  

#remove default theme
theme_plotly = None # None or streamlit

 
# CSS Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

#load excel file
df=pd.read_csv('data.csv')


#2. switcher
st.sidebar.header("Please Filter Here:")
region= st.sidebar.multiselect(
    "Select the Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)
location = st.sidebar.multiselect(
    "Select the Location:",
    options=df["Location"].unique(),
    default=df["Location"].unique(),
)
construction = st.sidebar.multiselect(
    "Select the Construction:",
    options=df["Construction"].unique(),
    default=df["Construction"].unique()
     
    
)
df_selection = df.query(
    "Region == @region & Location ==@location & Construction == @construction"
)

#method/function

def HomePage():
  #1. print dataframe
 with st.expander("🧭 My database"):
  #st.dataframe(df_selection,use_container_width=True)
  shwdata = st.multiselect('Filter :', df_selection.columns, default=["Location","State","Region","Investment","Construction","BusinessType","Earthquake"])
  st.dataframe(df_selection[shwdata],use_container_width=True)

 #2. compute top Analytics
 
 total_investment = float(df_selection['Investment'].sum())
 investment_mode = float(df_selection['Investment'].mode())
 investment_mean = float(df_selection['Investment'].mean())
 investment_median= float(df_selection['Investment'].median()) 
 rating = float(df_selection['Rating'].sum())

 #3. columns
 total1,total2,total3,total4 = st.columns(4,gap='large')
 with total1:

    st.info('Total Investment', icon="🔍")
    st.metric(label = 'sum TZS', value= f"{total_investment:,.0f}")
    
 with total2:
    st.info('Most frequently', icon="🔍")
    st.metric(label='Mode TZS', value=f"{investment_mode:,.0f}")

 with total3:
    st.info('Investment Average', icon="🔍")
    st.metric(label= 'Mean TZS',value=f"{investment_mean:,.0f}")

 with total4:
    st.info('Investment Marging', icon="🔍")
    st.metric(label='Median TZS',value=f"{investment_median:,.0f}")


    
 st.markdown("""---""")

 #graphs
 
def Graphs():
 total_investments = int(df_selection["Investment"].sum())
 average_rating = round(df_selection["Rating"].mean(), 1)
 star_rating = ":star:" * int(round(average_rating, 0))
 average_investment = round(df_selection["Investment"].mean(), 2)



#-----PROGRESS BAR-----

def ProgressBar():
  st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
  target=3000000000
  current=df_selection['Investment'].sum()
  percent=round((current/target*100))
  my_bar = st.progress(0)

  if percent>100:
    st.subheader("Target 100 complited")
  else:
   st.write("you have ", percent, " % " ," of ", (format(target, ',d')), " TZS")
   for percent_complete in range(percent):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1,text="Target percentage")

#-----SIDE BAR-----
 
HomePage()
Graphs()
ProgressBar()

footer="""<style>
 

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
height:10%;
bottom: 0;
width: 100%;
background-color: #D0D0D0;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with  ❤ by samir <a style='display: block; text-align: center;' href="https://www.heflin.dev/" target="_blank">Samir.s.s</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
