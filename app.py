import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit.components.v1 import html

from packageKPS import *
from PIL import Image



def main():
    

    #st.write(home())
    st.set_page_config(
        page_title="Koispe Dashboard",
        page_icon="✅",
        layout="wide",
    )    

            # Load the JavaScript function code
    with open("animated_counter.js", "r") as file:
            js_code = file.read()


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

    # st.write(df)
    # st.write(df2)
    # st.write(df3)

    merged= pd.merge(pd.merge(df, df2, on=['koispe_id', 'year']), df3, on=['koispe_id', 'year'])
    # merged= pd.merge([df, df2, df3], on=['koispe_id', 'year'])

    # merged=pd.merge(dfs,on=['koispe_id','year'])

    st.write(merged)
    kdata=merged[merged['koispe_id']==int(id)]


    kdata.drop(columns=['id_x', 'id_y','id'],inplace=True)
    # st.write(kdata)
    ###Start Creating DiktesDataframe

    kpdf=get_data_from_json(kdata)
    st.title("Πίνακας Δεικτών")
    st.write(kpdf)
   #Radio button
    ad_expander = st.sidebar.expander("Ανθρώπινο Δυναμικό / Επιχειρηματικότητα")
    with ad_expander:
        selected_option1 = st.radio("Επιλέξτε:", ["Συνεταιριστές","Εργαζόμενοι", "Ώρες Απασχόλησης", "Ετήσιες Μονάδες Εργασίας","Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος", "% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος", "Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος"])
    
    # selected_option3 = st.sidebar.button("Αναλυτικός Πίνακας Δεδομένων")

    # ad_expander = st.sidebar.expander("Ανθρώπινο Δυναμικό")


    #Buttons
    # with ad_expander:
    #     selected_option1 = st.button("Εργαζόμενοι")
    #     selected_option2 = st.button("Ώρες Απασχόλησης")
    #     selected_option3 = st.button("Ετήσιες Μονάδες Εργασίας")
    #     selected_option4 = st.button("Συνεταιριστές")

    # e_expander = st.sidebar.expander("Επιχειρηματικότητα")
    # with e_expander:
    #     selected_option5 = st.button("Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος")
    #     selected_option6 = st.button("% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος")
    #     selected_option7 = st.button("Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος")
    
    # selected_option8 = st.sidebar.button("Αναλυτικός Πίνακας Δεδομένων")


    # selected_item = st.sidebar.selectbox("", ["ad", "e", "pinkas"])


    #RADIO OPTION ANTHROPINO DYNAMIKO
    if selected_option1=="Συνεταιριστές":
        ad_button1(id,kpdf,js_code)
    elif selected_option1=="Εργαζόμενοι":
        ad_button2(id,kpdf,js_code)
    elif selected_option1=="Ώρες Απασχόλησης":
        ad_button3(id,kpdf,js_code)
    elif selected_option1=="Ετήσιες Μονάδες Εργασίας":
        ad_button4(id,kpdf,js_code)

    #RADIO OPTION EPIXEIRIMATIKOTITA
    if selected_option1=="Σύνολο κύκλου εργασιών ανά τομέα & κατανομή ανά δραστηριότητα ανά έτος":
        e_button5(id,kpdf)
    elif selected_option1=="% μεταβολής κύκλου εργασιών ανά δραστηριότητα ανά έτος":
        e_button6(id,kpdf)
    elif selected_option1=="Κατανομή πλήθους ΚοιΣΠΕ βάσει προσίμου καθαρών ανά έτος":
        e_button7(id,kpdf)
   


    
    # if selected_option1:
    #     ad_button1(id,kpdf)
    # elif selected_option2:
    #     ad_button2(id,kpdf)
    # elif selected_option3:
    #     ad_button3(id,kpdf)
    # elif selected_option4:
    #     ad_button4(id)

    # #Buttons epixirimatikotita    
    # elif selected_option5:
    #     e_button5(id,kpdf)
    # elif selected_option6:
    #     e_button6(id,kpdf)
    # elif selected_option7:
    #     e_button7(id,kpdf)
    # elif selected_option8:
    #     display_pinkas_submenu(id)



def ad_button1(id,kpdf,js_code):
    st.subheader("Συνεταιριστες")

    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    
    with st.container():


        # Display the HTML and JavaScript code
       
        #st.write('Col1 show D1')
        val=kpdf['D1'][kpdf['year']==str(year_filter)].iloc[0]
        # text="Συνεταιριστες Κατηγορια Α: "+str(val)+" 👪" 
        #st.write(kpdf['D1'][kpdf['year']==str(year_filter)])
        st.markdown("<h3 style='text-align: center; color: grey;'>Συνεταιριστες Κατηγορια Α</h3>", unsafe_allow_html=True)

        html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(val)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )






def ad_button2(id,kpdf,js_code):
    st.subheader("Εργαζόμενοι")
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            
            text=str(kpdf['D3'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write('Δ3-Εργαζόμενοι Γενικού Πληθυσμού: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι Γ.Π.</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
            #st.write(kpdf['D3'][kpdf['year']==str(year_filter)])

        with col2:
            
            text=kpdf['D5'][kpdf['year']==str(year_filter)].iloc[0]
            # st.write('Δ5-Εργαζόμενοι ΛΥΨΥ: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΛΥΨΥ</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
            #st.write(kpdf['D5'][kpdf['year']==str(year_filter)])


          
        with col3:
            #st.write('D7-Εργαζόμενοι ΕΚΟ')
            text=kpdf['D7'][kpdf['year']==str(year_filter)].iloc[0]
            # st.write('D7-Εργαζόμενοι ΕΚΟ: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Εργαζόμενοι ΕΚΟ</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
            #st.write(kpdf['D7'][kpdf['year']==str(year_filter)])

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            # Filter the dataframe based on the selected year
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]

            # Select the value from the filtered dataframe
            d9_value = filtered_kpdf["D9"].iloc[0]

            # Create the figure and gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=d9_value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Εργαζόμενοι Γενικού Πληθυσμού (% επί του Συνόλου Εργαζομένων ΚοιΣΠΕ)"},
                number={'suffix': '%'}
            ))

            # Customize the appearance of the gauge chart
            fig.update_traces(
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "royalblue",'thickness': 0.7},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 100], 'color': 'whitesmoke'},
                        ]
                    },  # Set the range for the gauge axis
                title_font={'size': 10,'color': 'gray'},  # Set the title font size
                number_font={'size': 40},  # Set the number font size
            )
            fig.update_layout(
                height=300,  # Adjust the height of the chart
                width=400,   # Adjust the width of the chart
                # margin=dict(l=0, r=0, t=30, b=0, autoexpand=True),  # Set the margin to auto

                paper_bgcolor="white",
                font={'color': "gray", 'family': "Arial"}
            )
            st.plotly_chart(fig)

        with col2:
            # Filter the dataframe based on the selected year
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]

            # Select the value from the filtered dataframe
            d10_value = filtered_kpdf["D10"].iloc[0]

            # Create the figure and gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=d10_value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Εργαζόμενοι Γενικού ΛΥΨΥ (% επί του Συνόλου Εργαζομένων ΚοιΣΠΕ)"},
                number={'suffix': '%'}
            ))

            # Customize the appearance of the gauge chart
            fig.update_traces(
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "skyblue",'thickness': 0.7},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 100], 'color': 'whitesmoke'},
                        ]
                    },  # Set the range for the gauge axis
                title_font={'size': 10,'color': 'gray'},  # Set the title font size
                number_font={'size': 40},  # Set the number font size
            )
            fig.update_layout(
                height=300,  # Adjust the height of the chart
                width=400,   # Adjust the width of the chart
                # margin=dict(l=0, r=0, t=30, b=0, autoexpand=True),  # Set the margin to auto

                paper_bgcolor="white",
                font={'color': "gray", 'family': "Arial"}
            )
            
            st.plotly_chart(fig)
        with col3:
            # Filter the dataframe based on the selected year
            filtered_kpdf = kpdf[kpdf["year"] == str(year_filter)]

            # Select the value from the filtered dataframe
            d11_value = filtered_kpdf["D11"].iloc[0]

            # Create the figure and gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=d11_value,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Εργαζόμενοι ΕΚΟ (% επί του Συνόλου Εργαζομένων ΚοιΣΠΕ)"},
                number={'suffix': '%'},
                
            ))
            

            # Customize the appearance of the gauge chart
            fig.update_traces(
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "red",'thickness': 0.7},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 100], 'color': 'whitesmoke'},
                        ]
                    },  # Set the range for the gauge axis
                title_font={'size': 10,'color': 'gray'},  # Set the title font size
                number_font={'size': 40},  # Set the number font size
            )
            fig.update_layout(
                height=300,  # Adjust the height of the chart
                width=400,   # Adjust the width of the chart
                paper_bgcolor="white",
                # margin=dict(l=0, r=0, t=30, b=0, autoexpand=True),  # Set the margin to auto

                font={'color': "gray", 'family': "Arial"}
            )
            # fig.update_layout(paper_bgcolor = "white", font = {'color': "gray", 'family': "Arial"})
            st.plotly_chart(fig)

        with st.container():
            col1, col2,col3 = st.columns(3)
            with col1:
                pass
            with col2:
                # Select the relevant columns
                columns = ['D9', 'D10', 'D11']
                kpdf_selected = kpdf[columns]
                # Create the stacked bar plot using Plotly
                fig = go.Figure()
                for col in columns:
                    fig.add_trace(go.Bar(
                        name=col,
                        x=kpdf['year'].apply(str),
                        y=kpdf_selected[col],
                        text=kpdf[col],
                        textposition='inside'
                    ))
                # Update the layout
                fig.update_layout(barmode='stack', xaxis_title='Year',yaxis_title='Percentage')
                fig.update_layout(title={
                    'text': '100% Stacked Bar Plot',
                    'y': 0.95,
                    'x': 0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                })
                # Show the plot
                st.plotly_chart(fig)
            with col3:
                pass










    #     col1, col2,col3 = st.columns(3)
    #     with col1:
    #         st.write('D12')
    #         st.metric(label="Συνολο"+str(kpdf['D12'][kpdf['year']=='2016'][0]), value=int(kpdf['D12'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")

    #     with col2:
    #         st.write('D13')
    #         st.metric(label="Συνολο"+str(kpdf['D13'][kpdf['year']=='2016'][0]), value=int(kpdf['D13'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")

  
    #     with col3:
    #         st.write('D14')
    #         st.write(kpdf['D14'])
    #         st.metric(label="Συνολο"+str(kpdf['D14'][kpdf['year']=='2016'][0]), value=int(kpdf['D14'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")
    # with st.container():
    #     col1, col2,col3 = st.columns(3)

    #     with col1:
    #         st.write('D15')
    #         st.write(kpdf['D15'])
    #         st.metric(label="Συνολο"+str(kpdf['D15'][kpdf['year']=='2016'][0]), value=int(kpdf['D15'][kpdf['year']=='2016'][0]), delta=-0.5,delta_color="inverse")
    #     with col2:
    #         st.write('D16')
    #         st.write(kpdf['D16'])
    #     with col3:
    #         st.write('D17')
    #         st.write(kpdf['D17'])

def ad_button3(id,kpdf,js_code):
    st.subheader("Ωρες απασχόλησης εργαζομένων")
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
   
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #st.write('Δ14-Ωρες απασχολησης εργαζομένων ΛΥΨΥ(Μεσος Όρος)')
            text=kpdf['D14'][kpdf['year']==str(year_filter)].iloc[0]
            text=str(text.round())
            #st.write(kpdf['D14'][kpdf['year']==str(year_filter)])
            # st.write('Δ14-'+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Ωρες απασχολησης εργαζομένων ΛΥΨΥ(Μεσος Όρος)</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
            # st.metric(label="Συνολο Μελών "+str(kpdf['D1'][kpdf['year']==str(year_filter)][0]), value=int(kpdf['D1'][kpdf['year']==str(year_filter)][0]), delta=-0.5,delta_color="inverse")

        with col2:
            #st.write('Δ15-Ωρες απασχολησης εργαζομένων ΕΚΟ(Μεσος Όρος)')
            #st.write(kpdf['D15'][kpdf['year']==str(year_filter)])
            text=kpdf['D15'][kpdf['year']==str(year_filter)].iloc[0]
            text=str(text.round())
            # st.write('Δ15-Ωρες απασχολησης εργαζομένων ΕΚΟ(Μεσος Όρος): '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Ωρες απασχολησης εργαζομένων ΕΚΟ(Μεσος Όρος)</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
        
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #st.write('Δ12-Ωρες απασχολησης εργαζομένων ΛΥΨΥ')
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D12'].tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                title='Μεταβολή ωρών απασχόλησης ΛΥΨΥ',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig)


        with col2:
            #st.write('Δ13-Ωρες απασχολησης εργαζομένων ΕΚΟ')
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D13'].tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                title='Μεταβολή ωρών απασχόλησης ΕΚΟ',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig)
        
          

   

# def ad_button3(id,kpdf):
#     st.subheader("button3 Submenu")
#     st.write("Content of button3")
#     with st.container():
#         col1, col2,col3 = st.columns(3)
#         with col1:
#             st.write('D18')
#             st.write(kpdf['D18'])

#         with col2:
#             st.write('D19')
#             st.write(kpdf['D19'])
#         with col3:
#             st.write('D20')
#             st.write(kpdf['D20'])

#     with st.container():
#         col1, col2,col3 = st.columns(3)
#         with col1:
#             st.write('D21')
#             st.write(kpdf['D21'])

#         with col2:
#             st.write('D22')
#             st.write(kpdf['D22'])

#         with col3:
#             st.write('D23')
#             st.write(kpdf['D23'])


          






def ad_button4(id,kpdf,js_code):
    st.subheader("Ετήσιες Μονάδες Εργασίας")
    
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            #st.write('D18')
            #st.write(kpdf['D18'][kpdf['year']==str(year_filter)])
            text=str(kpdf['D18'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write('D18 Ετησιες μοναδες εργασιας: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Ετησιες μοναδες εργασιας</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )
        with col2:
            #st.write('D19')
            #st.write(kpdf['D19'][kpdf['year']==str(year_filter)])
            text=str(kpdf['D19'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write('D19 Ετησιες μοναδες εργασιας: '+text)
            st.markdown("<h3 style='text-align: center; color: grey;'>Ετησιες μοναδες εργασιας(Μέσος Όρος)</h3>", unsafe_allow_html=True)

            html(
                f"""<body style="display: flex;flex-wrap: nowrap;align-content: center;justify-content: center;">
                <div id="counter" style="text-align: center; font-weight: bold; font-size: 60px; background-color: #f1f1f1; width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;"></div>
                <script type="text/javascript">
                {js_code}
                animateCounter2("counter", 0, """+str(text)+""", 1000);  // Increase from 0 to 100 in 1 second
                </script></body>
                """
            )

    with st.container():
        col1, col2 =st.columns(2)
        
        #     # val=50

        with col1:
             # Create the layout with two y-axes

            val=float(kpdf['D22'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write(val)
            # st.write(val2)
            layout = go.Layout(
                title='ΛΥΨΥ',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400,  # Set the width of the chart
                margin=dict(l=0, r=0, t=30, b=0, autoexpand=True)  # Set the margin to auto

            )
            fig = go.Figure( layout=layout)
            fig.add_trace(go.Pie(labels=['(%) ΛΥΨΥ επι του συνόλου',' '],
                                values=[val,100-val],
                                hole=0.85,
                                textinfo='none',
                                marker_colors=['rgb(135 206 235)','rgb(240,240,240)'],
                                ))
            fig.update_layout(annotations=[dict(text=str(val)+"%",  font_size=40, showarrow=False)])
            st.plotly_chart(fig)
        with col2:
        
            val2=float(kpdf['D23'][kpdf['year']==str(year_filter)].iloc[0])
            # st.write(val)
            # st.write(val2)
            layout = go.Layout(
                title='EKO',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )
            fig = go.Figure( layout=layout)
            fig.add_trace(go.Pie(labels=['(%) ΕΚΟ επι του συνόλου',' '],
                                values=[val2,100-val2],
                                hole=0.85,
                                textinfo='none',
                                marker_colors=['rgb(113,209,145)','rgb(240,240,240)'],
                                ))
            fig.update_layout(annotations=[dict(text=str(val2)+"%",  font_size=40, showarrow=False)])
            st.plotly_chart(fig)

    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.write('D18')
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D18_lipsi'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                title='% Ετήσια Μεταβολή Μονάδων Εργασίας ΛΥΨΥ',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig)


        with col2:
            st.write('D19')
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D18_eko'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                title='% Ετήσια Μεταβολή Μονάδων Εργασίας ΕΚΟ',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig)


    with st.container():
         col1, col2 = st.columns(2)
         with col1:
            # Select the relevant columns
            columns = ['D22', 'D23', 'D22_23_g']
            kpdf_selected = kpdf[columns]
            # Create the stacked bar plot using Plotly
            fig = go.Figure()
            for col in columns:
                fig.add_trace(go.Bar(
                    name=col,
                    x=kpdf['year'].apply(str),
                    y=kpdf_selected[col],
                    text=kpdf[col],
                    textposition='inside'
                ))
            # Update the layout
            fig.update_layout(barmode='stack', title='100% Stacked Bar Plot', xaxis_title='Year',yaxis_title='Percentage')
            # Show the plot
            st.plotly_chart(fig)

             



        




def e_button5(id,kpdf):
    st.subheader("button5 Submenu")
    st.write("Content of button5")
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    val2=float(kpdf['D24'][kpdf['year']==str(year_filter)].iloc[0])
    text="**Κυκλοι** **Εργασιών:** **"+str(val2)+"** **&#8364;** "
        #st.write(first_alias_value)
        #st.markdown(text)
    st.title(text)
   
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            val26=float(kpdf['D26'][kpdf['year']==str(year_filter)].iloc[0])
            text26="**🏠** **"+str(val26)+"** &#8364; "
            st.title(text26)
        with col2:
            val27=float(kpdf['D27'][kpdf['year']==str(year_filter)].iloc[0])
            text27="**🍴** **"+str(val27)+"** &#8364; "
            st.title(text27)
        with col3:
            val28=float(kpdf['D28'][kpdf['year']==str(year_filter)].iloc[0])
            text28="**🎏** **"+str(val28)+"** &#8364; "
            st.title(text28)
    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            labels = ['Δ26','Δ27','Δ28']

            fig = go.Figure(data=[go.Pie(labels=labels, values=[val26,val27,val28])])
            st.plotly_chart(fig)

    with st.container():
        col1,col2 = st.columns(2)
        with col1:
             # Select the relevant columns
            columns = ['D26', 'D27', 'D28']
            kpdf_selected = kpdf[columns]
            # Create the stacked bar plot using Plotly
            fig = go.Figure()
            for col in columns:
                fig.add_trace(go.Bar(
                    name=col,
                    x=kpdf['year'].apply(str),
                    y=kpdf_selected[col],
                    text=kpdf[col],
                    textposition='inside'
                ))
            # Update the layout
            fig.update_layout(barmode='stack', title='100% Stacked Bar Plot', xaxis_title='Year',yaxis_title='Percentage')
            # Show the plot
            st.plotly_chart(fig)
   




def e_button6(id,kpdf):
    st.subheader("button6 Submenu")
    st.write("Content of button6")
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    val1=float(kpdf['D24'][kpdf['year']==str(year_filter)].iloc[0])
    val2=float(kpdf['D29'][kpdf['year']==str(year_filter)].iloc[0])
    val3=float(kpdf['D26'][kpdf['year']==str(year_filter)].iloc[0])
    val4=float(kpdf['D30'][kpdf['year']==str(year_filter)].iloc[0])
    val5=float(kpdf['D27'][kpdf['year']==str(year_filter)].iloc[0])
    val6=float(kpdf['D31'][kpdf['year']==str(year_filter)].iloc[0])
    val7=float(kpdf['D28'][kpdf['year']==str(year_filter)].iloc[0])
    val8=float(kpdf['D32'][kpdf['year']==str(year_filter)].iloc[0])
    with st.container():
        col1, col2,col3,col4 = st.columns(4)
        with col1:
            st.metric(label="% Μεταβολή Κύκλου Εργασιών", value=val1, delta=f'{val2}%')
        with col2:
            st.metric(label="% Μεταβολή Κύκλου Εργασιών-Κτήρια/Εξωτερικοί Χώροι ", value=val3, delta=f'{val4}%')
        with col3:
            st.metric(label="% Μεταβολή Κύκλου Εργασιών-Υπηρεσίες Εστίασης", value=val5, delta=f'{val6}%')
        with col4:
            st.metric(label="% Μεταβολή Κύκλου Εργασιών-Λοιπές εργασίες", value=val7, delta=f'{val8}%')

    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D24'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                title='% Ετήσια Μεταβολή Κύκλου Εργασιών',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig)

        with col2:
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D26'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                title='% Ετήσια Μεταβολή Κύκλου Εργασιών-Κτήρια/Εξωτερικοί Χώροι',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig)

           
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D27'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                title='% Ετήσια Μεταβολή Κύκλου Εργασιών-Υπηρεσίες Εστίασης',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig)
        with col2:
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D28'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                title='% Ετήσια Μεταβολή Κύκλου Εργασιών-Λοιπές Δραστηριότητες',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig)




def e_button7(id,kpdf):
    st.subheader("button7 Submenu")
    st.write("Content of button7")
    year_filter = st.selectbox("Έτος", kpdf['year'].tolist())
    val1=float(kpdf['D36_overal'][kpdf['year']==str(year_filter)].iloc[0])
    val2=float(kpdf['D36'][kpdf['year']==str(year_filter)].iloc[0])
    val3=float(kpdf['D38'][kpdf['year']==str(year_filter)].iloc[0])
    val4=float(kpdf['D40'][kpdf['year']==str(year_filter)].iloc[0])
    val5=float(kpdf['D40_metaboli'][kpdf['year']==str(year_filter)].iloc[0])

    with st.container():
        col1, col2,col3 = st.columns(3)
        with col1:
            st.metric(label="% Ετήσια Μεταβολή Καθαρών αποτελεσμάτων", value=val1, delta=f'{val2}%')
        with col2:
            st.metric(label="Αριθμοδείκτη καθαρών αποτελεσμάτων", value=val3)
        with col3:
            st.metric(label="Έσοδα ανά εργαζόμενο / % Ετήσια Μεταβολή", value=val4, delta=f'{val5}%')

    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            categories=kpdf['year'].tolist()
            # Sample data
            # categories = ['Category A', 'Category B', 'Category C', 'Category D']
            values =kpdf['D36_overal'].astype(int).tolist()

            # Calculate percentage change
            percentage_change = [(values[i] - values[i-1]) / values[i-1] * 100 for i in range(1, len(values))]

            # Create the bar trace
            bar_trace = go.Bar(x=categories, y=values, name='Values')

            # Create the line trace
            line_trace = go.Scatter(x=categories[1:], y=percentage_change, name='Percentage Change', mode='lines+markers', yaxis='y2')

            # Create the layout with two y-axes
            layout = go.Layout(
                title='% Ετήσια Μεταβολή Καθαρών Αποτελεσμάτων',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )

            # Create the figure
            fig = go.Figure(data=[bar_trace, line_trace], layout=layout)

            # Add labels to the bars
            for i in range(len(categories)):
                fig.add_annotation(
                    x=categories[i], y=values[i],
                    text=str(values[i]),
                    showarrow=False,
                    font=dict(color='black', size=12),
                    xanchor='center', yanchor='bottom'
                )

            # Add labels to the percentage change
            for i in range(len(percentage_change)):
                fig.add_annotation(
                    x=categories[i+1], y=percentage_change[i],
                    text=f"{percentage_change[i]:.2f}%",
                    showarrow=False,
                    font=dict(color='red', size=12),
                    xanchor='center', yanchor='bottom'
                )
            st.plotly_chart(fig)
        with col2:
             
            val39=float(kpdf['D39'][kpdf['year']==str(year_filter)].iloc[0])
            
            # st.write(val2)
            layout = go.Layout(
                title='Συμμετοχή (%) Επιδοτήσεων στα έσοδα / Ετος',
                yaxis=dict(title='Values', rangemode='nonnegative'),
                yaxis2=dict(title='Ποσοστιαία μεταβολή', overlaying='y', side='right', showgrid=False),
                height=600,  # Set the height of the chart
                width=400  # Set the width of the chart
            )
            fig = go.Figure( layout=layout)
            fig.add_trace(go.Pie(labels=['% Συμμετοχή Επιδοτήσεων',' '],
                                values=[val39,100-val39],
                                hole=0.85,
                                textinfo='none',
                                marker_colors=['rgb(135 206 235)','rgb(240,240,240)'],
                                ))
            fig.update_layout(annotations=[dict(text=str(val39)+"%",  font_size=40, showarrow=False)])
            st.plotly_chart(fig)
            # fig = px.area(kpdf, title="Αριθμοδείκτης Καθαρών Αποτελεσμάτων / Έτος",x='year', y='D38', markers=True)
            # st.plotly_chart(fig)
    with st.container():
        col1,col2 = st.columns(2)  
        with col1:
            st.write("smt"); 
            fig = px.area(kpdf, title="Αριθμοδείκτης Καθαρών Αποτελεσμάτων / Έτος",x='year', y='D38', markers=True)
            st.plotly_chart(fig)        
        with col2:
            st.write("smt"); 
            # fig = px.area(kpdf, title="Αριθμοδείκτης Καθαρών Αποτελεσμάτων / Έτος",x='year', y='D38', markers=True)
            # st.plotly_chart(fig)   
            # fig = px.area(kpdf, title="Αριθμοδείκτης Καθαρών Αποτελεσμάτων / Έτος",x='year', y='D38', markers=True)
            # st.plotly_chart(fig)



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
    
