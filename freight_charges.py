import pandas as pd
import numpy as np
import streamlit as st
from visualizations import show_pivot,show_agg,show_barplot,show_lineplot
import plotly.graph_objects as go
from utils import brand_map,column_list

st.header('DCL Freight Cost Tracker 📉')
uploaded_file=st.file_uploader("Please upload the freight file",type='csv',accept_multiple_files=False)
if uploaded_file is not None:
    try:
        df=pd.read_csv(uploaded_file,parse_dates=['Ship Date'],encoding='Windows-1252')
        st.dataframe(df)
    except:
        st.warning('The file cannot be parsed, please check the file/data type')
    run=st.button('Visualize the Table')
    if run:
        # Check Table
        try:
            assert set(df.columns)==column_list
        except:
            st.warning('Please check your file columns, below columns must be included')
            st.warning('Acct #, Carrier, Delivery Date, Delivery Days, Delivery Status, Dimension, Freight, Order #, Rated Weight, Service, Ship Date, Ship To City,\
                        Ship To Country,Ship To State,Ship To Zip,Zone')
        # Table Cleaning
        if df['Rated Weight'].dtype!='float':
            df['Rated Weight']=df['Rated Weight'].str.replace(',','',regex=False)
            df['Rated Weight']=df['Rated Weight'].astype('float')
        if df['Freight'].dtype!='float':
            df['Freight']=df['Freight'].str.replace(',','',regex=False)
            df['Freight']=df['Freight'].astype('float')
        df['Weight Block']=pd.cut(df['Rated Weight'],[0,0.5,1,1.5,2,np.inf],right=False,labels=['0-0.5','0.5-1','1-1.5','1.5-2','2+'])
        df['Week']=pd.to_datetime(df['Ship Date'].dt.isocalendar().year.astype(str) + df['Ship Date'].dt.isocalendar().week.astype(str) + "1",format='%G%V%w')
        df['Brand']=df['Acct #'].map(brand_map)
        week_list=list(df['Week'].unique())
        week_list.sort()
        this_week_cost=df[df['Week']==week_list[-1]]['Freight'].mean()
        past_weeks_cost=df[df['Week']!=week_list[-1]]['Freight'].mean()
        delta=(this_week_cost-past_weeks_cost)/past_weeks_cost
        tab1,tab2,tab3,tab4,tab5,tab6,tab7=st.tabs(['Alert',"Weight", "Country", "Brand",'Carrier','Service','Zone'])
        with tab1:
            fig = go.Figure(go.Indicator(
                mode="number+delta",
                value = this_week_cost,
                number = {'prefix': "$"},
                delta  = {'reference': past_weeks_cost,'relative':True,"valueformat": ".2f",'suffix':'%','increasing.color':'red','decreasing.color':'green'}))
            st.plotly_chart(fig, use_container_width=True)
            st.header('Orders with service level mismatch')
            df_alert=df[(df['Rated Weight']<1) & (df['Service'].str.contains('PLUS'))]
            df_download=df_alert.to_csv(index=False).encode('utf-8')
            st.dataframe(df_alert)
            st.download_button('Download Mismatching Orders',data=df_download,file_name='Mismatching Orders.csv')

        with tab2:
            col1,col2=st.columns([0.8, 0.2])
            with col1:
                by_weight=show_pivot(df,'Weight Block')
                st.dataframe(by_weight)
            with col2:
                df1_download=by_weight.to_csv(index=False).encode('utf-8')
                st.download_button('Download Table',data=df1_download,file_name='Cost by Weight Block.csv')
            show_lineplot(df,'Weight Block')

        with tab3:
            col1,col2=st.columns([0.8, 0.2])
            with col1:
                by_country=show_agg(df,'Ship To Country')
                st.dataframe(by_country)
            with col2:
                df2_download=by_country.to_csv(index=False).encode('utf-8')
                st.download_button('Download Table',data=df2_download,file_name='Cost by Country.csv')
            show_barplot(df,'Ship To Country','Greens')    

        with tab4:
            col1,col2=st.columns([0.8, 0.2])
            with col1:
                by_brand=show_pivot(df,'Acct #')
                st.dataframe(by_brand)
            with col2:
                df3_download=by_brand.to_csv(index=False).encode('utf-8')
                st.download_button('Download Table',data=df3_download,file_name='Cost by Acct.csv')
            show_lineplot(df,'Brand')        
        
        with tab5:
            col1,col2=st.columns([0.8, 0.2])
            with col1:
                by_carrier=show_pivot(df,'Carrier')
                st.dataframe(by_carrier)
            with col2:
                df4_download=by_carrier.to_csv(index=False).encode('utf-8')
                st.download_button('Download Table',data=df4_download,file_name='Cost by Carrier.csv')
            show_lineplot(df,'Carrier')        
        
        with tab6:
            col1,col2=st.columns([0.8, 0.2])
            with col1:
                by_service=show_agg(df,'Service')
                st.dataframe(by_service)
            with col2:
                df5_download=by_service.to_csv(index=False).encode('utf-8')
                st.download_button('Download Table',data=df5_download,file_name='Cost by Service.csv')
            show_barplot(df,'Service','Blues')   

        with tab7:
            col1,col2=st.columns([0.8, 0.2])
            with col1:
                df_to_use=df[df['Ship To Country']=='UNITED_STATES']
                by_zone=show_agg(df_to_use,'Zone')
                st.dataframe(by_zone)
            with col2:
                df6_download=by_zone.to_csv(index=False).encode('utf-8')
                st.download_button('Download Table',data=df6_download,file_name='Cost by Zone.csv')
            show_barplot(df_to_use,'Zone','Reds')   




