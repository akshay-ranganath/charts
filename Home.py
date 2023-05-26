import streamlit as st
import pandas as pd
from io import StringIO, BytesIO
#import plotly.figure_factory as ff
import plotly.express as px

st.set_page_config(
    page_title='Create Customer Usage Reports',    
    layout="wide",
    page_icon="./images/logo.jpg"
)

cols = st.columns([1,3])
with cols[0]:
    st.image('./images/logo.jpg',width=250)
with cols[1]:
    st.header('Create Customer Usage report')
    st.caption('Quickly generate reports for QBR / EBCs.')

st.subheader('Upload your Qlick Report')
uploded_file = st.file_uploader(
    label="",
    accept_multiple_files=False,
    help="Upload CSV"
)

if uploded_file != None: 
    print(uploded_file.type)
    if uploded_file.type.find('application/vnd.openxm')>-1:    
        st.success('File uploaded successfully.')        
        # https://stackoverflow.com/questions/47379476/how-to-convert-bytes-data-into-a-python-pandas-dataframe
        df = pd.read_excel(BytesIO(uploded_file.read()))  
        # add a column for the original resource storage - this does not come through from report
        df['Resource Storage (MB)'] = df['Total Storage (MB)'] - (df['Derived Resource Storage (MB)'] + df['Backup Storage (MB)'])
        # add another column to calculate the bandwidth for serving raw files
        df['Raw Bandwidth (MB)'] = df['Bandwidth (MB)'] - (df['Image Bandwidth (MB)'] + df['Video Bandwidth (MB)'])
        
        st.subheader('Transformations')
        st.caption('Transformations over time')
        fig = px.line(df, x='Year Month', y='Transformations')
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption('Transformations by type')
        fig = px.bar(df, x='Year Month', y=['Image Transformations','Video Transformations'])
        st.plotly_chart(fig, use_container_width=True)
        
        columns = ["Image", "Video"]
        values = [df['Image Transformations'].sum(), df['Video Transformations'].sum()]
        print(values)
                
        st.subheader('Storage')
        st.caption('Storage over time')
        fig = px.line(df, x='Year Month', y='Total Storage (MB)')
        st.plotly_chart(fig, use_container_width=True)

        st.caption('Storage by type')
        fig = px.bar(df, x='Year Month', y=['Resource Storage (MB)', 'Derived Resource Storage (MB)', 'Backup Storage (MB)'])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader('Bandwidth')
        st.caption('Bandwidth over time')
        fig = px.line(df, x='Year Month', y='Bandwidth (MB)')
        st.plotly_chart(fig, use_container_width=True)

        st.caption('Bandwidth by type')
        fig = px.bar(df, x='Year Month', y=['Image Bandwidth (MB)','Video Bandwidth (MB)', 'Raw Bandwidth (MB)'])
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error('Wrong file type! Please upload a CSV.')