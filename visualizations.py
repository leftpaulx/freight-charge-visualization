import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

def show_pivot(df,column):
    pivot=pd.pivot_table(data=df,index='Week',columns=column,values='Freight',aggfunc=np.mean)
    return pivot.apply(lambda x: x.apply(lambda y: '${:.2f}'.format(y) if pd.notna(y) else y))

def show_agg(df,column):
    agg_df=df.groupby(column).agg({'Freight':['mean','count']})['Freight']
    agg_df.columns=['Freight','Orders']
    agg_df['Freight']=agg_df['Freight'].apply(lambda x: '${:.2f}'.format(x))
    agg_df.sort_values('Orders',ascending=False,inplace=True)
    return agg_df

def show_lineplot(df,column):
    all_items=df.value_counts(column)
    items_to_use=all_items[all_items>5].index
    df_to_use=df[df[column].isin(items_to_use)]
    grouped_df=df_to_use.groupby(['Week',column])['Freight'].mean().reset_index()
    fig=px.line(grouped_df,x='Week',y='Freight',color=column,title=f'Freight by {column}')
    fig.update_layout( yaxis={'tickformat': '$.2f'})
    st.plotly_chart(fig)

def show_barplot(df,column,color):
    all_items=df.value_counts(column)
    items_to_use=all_items[all_items>5].index
    df_to_use=df[df[column].isin(items_to_use)]
    grouped_df=df_to_use.groupby(column).agg({'Freight':['mean','count']})['Freight']
    grouped_df.columns=['Freight','Orders']
    grouped_df['Color Index']=np.log(grouped_df['Orders'])
    fig=px.bar(grouped_df,x=grouped_df.index,y='Freight',color='Color Index',color_continuous_scale=color,hover_data=['Freight','Orders'],title=f'Freight by {column}')
    fig.update_layout( yaxis={'tickformat': '$.2f'})
    fig.update_xaxes(type='category')
    st.plotly_chart(fig)
