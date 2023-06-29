import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image


@st.cache_resource
def get_data_from_json(kdata):
    kpdf=kdata[['koispe_id','year']]
    

    # kpdf['year']=kpdf['year'].astype(str)
    kpdf['D1'] = kdata['profile.meli_a']
    kpdf['D3'] = kdata['profile.employee_general.sum']
    kpdf['D5'] = kdata['profile.employee.sum']
    kpdf['D7'] = kdata['profile.eko.sum']
    #Calculation from function
    kpdf['D9']=kpdf.apply(calculate_d9, axis=1)
    kpdf['D10']=kpdf.apply(calculate_d10, axis=1)
    kpdf['D11']=kpdf.apply(calculate_d11, axis=1)
    #ores apasxolisis
    kpdf['D12']=(kdata['profile.eme.sum'].astype(int))*2080
    kpdf['D13']=(kdata['profile.eme_eko.sum'].astype(int))*2080
    kpdf['D14']=kpdf.apply(calculate_d14, axis=1)
    kpdf['D15']=kpdf.apply(calculate_d15, axis=1)
    kpdf['D16']=round((kpdf['D12'].pct_change() * 100),1)
    kpdf['D17']=round((kpdf['D13'].pct_change() * 100),1)
    #etisies monades ergasias
    kpdf['D18']=kdata['profile.sum_eme_kispe']
    kpdf['D19']=kpdf.apply(calculate_d19, axis=1)
    kpdf['D20']=round((kdata['profile.eme.sum'].astype(int).pct_change()*100),1)
    kpdf['D21']=round((kdata['profile.eme_eko.sum'].astype(int).pct_change()*100),1)
    kpdf['D22']=round(((kdata['profile.eme.sum'].astype(int))/(kdata['profile.sum_eme_kispe'].astype(int))*100),1)
    kpdf['D23']=round(((kdata['profile.eme_eko.sum'].astype(int))/(kdata['profile.sum_eme_kispe'].astype(int))*100),1)

    #Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος
    kpdf['D24']=kdata['report.turnover_total']
    #search for kad starts from .81

    matching_columns = kdata.columns[kdata.columns.str.startswith("report.kad.81.")]
    kdata[matching_columns] = kdata[matching_columns].astype(int)

    kpdf['D26'] = kdata.apply(lambda row: calculate_d26_d27(row, matching_columns), axis=1)
    #search for kad starts from .56
    matching_columns2 = kdata.columns[kdata.columns.str.startswith("report.kad.56.")]
    kdata[matching_columns2] = kdata[matching_columns2].astype(int)
    
    kpdf['D27'] = kdata.apply(lambda row: calculate_d26_d27(row, matching_columns2), axis=1)

    kpdf['D28'] = kdata['report.turnover_other']

    #% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος
    kpdf['D29'] = round((kdata['report.turnover_total'].astype(int).pct_change()*100),1)

    kpdf['D30'] = round((kpdf['D26'].astype(int).pct_change()*100),1)
    kpdf['D31'] = round((kpdf['D27'].astype(int).pct_change()*100),1)
    kpdf['D32'] = round((kpdf['D28'].astype(int).pct_change()*100),1)
    kpdf['D36'] = round((kdata['report.overall'].astype(int).pct_change()*100),1)

    return kpdf


def calculate_d26_d27(row,matching_columns):
    st.write("mpike")
    st.write(matching_columns)
    values = row[matching_columns]
    column_sum = values.sum()
    st.write(column_sum)
    d26=column_sum
    return d26






def calculate_d19(row):
    d18=row['D18']
    d3 = row['D3']
    d5 = row['D5']
    d7 = row['D7']
    return round((int(d18) / (int(d3) + int(d5) + int(d7))),1)



def calculate_d15(row):    
    d7 = row['D7']
    d13 = row['D13']
  
    return int(d13) / int(d7) 




def calculate_d14(row):    
    d5 = row['D5']
    d12 = row['D12']
  
    return int(d12) / int(d5) 



def calculate_d11(row):    
    d3 = row['D3']
    d5 = row['D5']
    d7 = row['D7']
    return round((int(d7) / (int(d3) + int(d5) + int(d7))*100),1)

def calculate_d10(row):    
    d3 = row['D3']
    d5 = row['D5']
    d7 = row['D7']
    return round((int(d5) / (int(d3) + int(d5) + int(d7))*100),1)

def calculate_d9(row):    
    d3 = row['D3']
    d5 = row['D5']
    d7 = row['D7']
    return round((int(d3) / (int(d3) + int(d5) + int(d7))*100),1)


def format_year(year):
    return "{:d}".format(year)  # Removes the comma separator

def main():
    

    #st.write(home())
    st.set_page_config(
        page_title="Koispe Dashboard",
        page_icon="✅",
        layout="wide",
    )    

    st.sidebar.title("Menu")
    id=get_url_params()

    st.write("ID from Flask application: ",id)
    # image = Image.open('https://dreamleague-soccerkits.com/wp-content/uploads/2021/07/Real-Madrid-Logo.png','rb')

    st.image("https://dreamleague-soccerkits.com/wp-content/uploads/2021/07/Real-Madrid-Logo.png", width=120)

    response = json.loads(requests.get("https://cmtprooptiki.gr/api/getkoisenew.json").text)
    response2 = json.loads(requests.get("https://cmtprooptiki.gr/api/getemploymentcmt.json").text)
    response3 = json.loads(requests.get("https://cmtprooptiki.gr/api/getfinancial.json").text)


    df=pd.json_normalize(response, max_level=2)
    df['year'] = df['year'].apply(format_year)

    df2=pd.json_normalize(response2, max_level=2)
    df2['year'] = df2['year'].apply(format_year)

    df3=pd.json_normalize(response3, max_level=2)
    df3['year'] = df3['year'].apply(format_year)

    st.write(df)
    st.write(df2)
    st.write(df3)

    merged= pd.merge(pd.merge(df, df2, on=['koispe_id', 'year']), df3, on=['koispe_id', 'year'])
    # merged= pd.merge([df, df2, df3], on=['koispe_id', 'year'])

    # merged=pd.merge(dfs,on=['koispe_id','year'])
    st.write(merged)
    kdata=merged[merged['koispe_id']==int(id)]


    kdata.drop(columns=['id_x', 'id_y','id'],inplace=True)
    st.write(kdata)
    ###Start Creating DiktesDataframe

    kpdf=get_data_from_json(kdata)

   

    st.write(kpdf)
    st.write(kpdf)


    ad_expander = st.sidebar.expander("Ανθρώπινο Δυναμικό")
    with ad_expander:
        selected_option1 = st.button("Εργαζόμενοι")
        selected_option2 = st.button("Ώρες Απασχόλησης")
        selected_option3 = st.button("Ετήσιες Μονάδες Εργασίας")
        selected_option4 = st.button("Συνεταιριστές")

    e_expander = st.sidebar.expander("Επιχειρηματικότητα")
    with e_expander:
        selected_option5 = st.button("Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος")
        selected_option6 = st.button("% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος")
        selected_option7 = st.button("Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος")
    
    selected_option8 = st.sidebar.button("Αναλυτικός Πίνακας Δεδομένων")


    # selected_item = st.sidebar.selectbox("", ["ad", "e", "pinkas"])
    
    if selected_option1:
        ad_button1(id,kpdf)
    elif selected_option2:
        ad_button2(id,kpdf)
    elif selected_option3:
        ad_button3(id,kpdf)
    elif selected_option4:
        ad_button4(id)

    #Buttons epixirimatikotita    
    elif selected_option5:
        e_button5(id,kpdf)
    elif selected_option6:
        e_button6(id,kpdf)
    elif selected_option7:
        e_button7(id)
    elif selected_option8:
        display_pinkas_submenu(id)



def ad_button1(id,kpdf):
    st.subheader("button1 Submenu")
    # response = json.loads(requests.get("https://cmtprooptiki.gr/api/getkoispe.json").text)



    # df=pd.json_normalize(response, max_level=1)
    # st.write(df)
    # data = json.loads(response.text)
    
    # Convert the JSON data to a list of dictionaries


    # records = []
    # for key, value in response.items():
    #     value['id'] = key
    #     records.append(value)
    
    # Create a dataframe from the list of dictionaries
    #df = pd.DataFrame(records)
    # df=pd.json_normalize(records, max_level=2)
    # year_filter = st.selectbox("Select the Job", pd.unique(df["year"]))
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    
    st.write("Content of button1")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('Col1 show D1')
            st.metric(label="Συνολο Μελών "+str(kpdf['D1'][kpdf['year']==str(year_filter)][0]), value=int(kpdf['D1'][kpdf['year']==str(year_filter)][0]), delta=-0.5,delta_color="inverse")

        with col2:
            st.write('Col2 Caption for first chart')

          
        with col3:
            st.write('Col3 Caption for first chart')

            st.write("Content of column3")

    with st.container():
        col1, col2,col3 = st.columns(3)

        with col1:
            st.write('Col1 Caption for second chart')
            
            # Select the relevant columns
            columns = ['D9', 'D10', 'D11']
            df_selected = kpdf[columns]

            # Calculate the percentage values for each column
            # df_percent = df_selected.div(df_selected.sum(axis=1), axis=0) * 100

            # Create the stacked bar plot using Plotly
            fig = go.Figure()

            for col in columns:
                fig.add_trace(go.Bar(
                    name=col,
                    x=kpdf['year'].apply(str),
                    y=df_selected[col],
                    text=kpdf[col],
                    textposition='inside'

                ))

            # Update the layout
            fig.update_layout(barmode='stack', title='100% Stacked Bar Plot', xaxis_title='Year',yaxis_title='Percentage')
            # Show the plot

            st.plotly_chart(fig)

            





        with col2:
            st.write('Col2 Caption for second chart col2')
            st.line_chart((1,0), height=100)
        with col3:
            st.write('Col3 Caption for second chart col3')
            st.line_chart((1,0), height=100)



def ad_button2(id,kpdf):
    st.subheader("button2 Submenu")
    st.write("Content of button2")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D12')
            st.metric(label="Συνολο"+str(kpdf['D12'][kpdf['year']=='2016'][0]), value=int(kpdf['D12'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")

        with col2:
            st.write('D13')
            st.metric(label="Συνολο"+str(kpdf['D13'][kpdf['year']=='2016'][0]), value=int(kpdf['D13'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")

  
        with col3:
            st.write('D14')
            st.write(kpdf['D14'])
            st.metric(label="Συνολο"+str(kpdf['D14'][kpdf['year']=='2016'][0]), value=int(kpdf['D14'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")
    with st.container():
        col1, col2,col3 = st.columns(3)

        with col1:
            st.write('D15')
            st.write(kpdf['D15'])
            st.metric(label="Συνολο"+str(kpdf['D15'][kpdf['year']=='2016'][0]), value=int(kpdf['D15'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")
        with col2:
            st.write('D16')
            st.write(kpdf['D16'])
        with col3:
            st.write('D17')
            st.write(kpdf['D17'])


          

   

def ad_button3(id,kpdf):
    st.subheader("button3 Submenu")
    st.write("Content of button3")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D18')
            st.write(kpdf['D18'])

        with col2:
            st.write('D19')
            st.write(kpdf['D19'])
        with col3:
            st.write('D20')
            st.write(kpdf['D20'])

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D21')
            st.write(kpdf['D21'])

        with col2:
            st.write('D22')
            st.write(kpdf['D22'])

        with col3:
            st.write('D23')
            st.write(kpdf['D23'])


          






def ad_button4(id):
    st.subheader("button4 Submenu")
    st.write("Content of button4")

def e_button5(id,kpdf):
    st.subheader("button5 Submenu")
    st.write("Content of button5")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D24')
            st.write(kpdf['D24'])
        with col2:
            st.write('D26')
            st.write(kpdf['D26'])
        with col3:
            st.write('D27')
            st.write(kpdf['D27'])
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D28')
            st.write(kpdf['D28'])




def e_button6(id,kpdf):
    st.subheader("button6 Submenu")
    st.write("Content of button6")
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D29')
            st.write(kpdf['D29'])
        with col2:
            st.write('D30')
            st.write(kpdf['D30'])
        with col3:
            st.write('D31')
            st.write(kpdf['D31'])
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.write('D32')
            st.write(kpdf['D32'])
        with col2:
            st.write('D36')
            st.write(kpdf['D36'])




def e_button7(id):
    st.subheader("button7 Submenu")
    st.write("Content of button7")

def display_pinkas_submenu(id):
    st.subheader("pinkas Submenu")
    st.write("Content for pinkas submenu")
    
    response = json.loads(requests.get("https://cmtprooptiki.gr/api/getemploymentcmt.json").text)
    df=pd.json_normalize(response, max_level=2)
    df['year'] = df['year'].apply(format_year)

    df1=df.groupby(['koispe_id','year'])['profile.eko.sum'].sum()
    dftest=pd.DataFrame(df1).reset_index()
    
    st.write(df)
    dffilter=dftest[dftest['koispe_id']==int(id)]
    # dffilter['year'] = dffilter['year'].apply(format_year)
    # dffilter
    # data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(dffilter, x=dffilter['year'].astype(str), y='profile.eko.sum',orientation='v')
    st.plotly_chart(fig)

    # Add content for pinkas submenu here




def get_url_params():
    query_params = st.experimental_get_query_params()
    id_received = query_params.get("id", [""])[0]
    
    return id_received
    # id_input = st.text_input("Enter ID", value=id_received)
    # if id_input:
    #     display_contents(id_input)

def display_contents(id_received):
    # Retrieve the contents of the specific ID (replace with your own logic)
    contents = {'id': id_received, 'name': 'John eseaas', 'email': 'john@example.com'}

    st.write(f'# Contents of ID: {id_received}')
    st.write(f'Name: {contents["name"]}')
    st.write(f'Email: {contents["email"]}')



if __name__ == "__main__":
    main()
    
