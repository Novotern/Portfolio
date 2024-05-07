import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(layout="wide", page_title='Finance KPIs', page_icon='logo.png' ) 


with st.expander(':red[Finance KPIs]', expanded=True):
  power = """<iframe title="Report Section" width="1200" height="1000" 
              src="https://app.powerbi.com/view?r=eyJrIjoiMGVlOGFiYzYtZjM0MC00ZmNmLWJlYjAtNGVmOTNhY2E0ZGNjIiwidCI6ImNlMzBlNGMzLWM4NjItNGVlZC1hMzdjLWU3NmJjODNhY2ZmYSJ9" 
              frameborder="0" allowFullScreen="true"></iframe>"""
  components.html(power, height=1010, width=1800)
  
  
#   <iframe title="Panel analysis - Copy" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiMGVlOGFiYzYtZjM0MC00ZmNmLWJlYjAtNGVmOTNhY2E0ZGNjIiwidCI6ImNlMzBlNGMzLWM4NjItNGVlZC1hMzdjLWU3NmJjODNhY2ZmYSJ9" frameborder="0" allowFullScreen="true"></iframe>