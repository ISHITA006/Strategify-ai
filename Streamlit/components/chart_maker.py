import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
import math
import plotly.graph_objects as go
import statistics
import nltk
from nltk.corpus import wordnet
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_pie_chart(df, col_name):
    fig = px.pie(df, names=col_name)
    fig.update_layout(
    legend_borderwidth=10,
    legend_font=dict(
        size = 18,
    ),
    font=dict(
        size=17,  # Set the font size here
    ))
    fig.update_layout(legend=dict(
    yanchor="top",
    y=1,
    xanchor="left",
    x=1
    ))
    st.plotly_chart(fig, use_container_width=True)

def create_stacked_bar_chart(df, division_name, division_option):
    df['age_group'] = pd.cut(df['Age'], bins=[16, 24, 34, 44, 54, 64, 100], labels=['16-24', '25-34', '35-44', '45-54', '55-64', '65>'])
    df_grouped = df.groupby([division_name, 'Rating', 'age_group']).size().reset_index(name='counts')
    df_grouped = df_grouped[df_grouped[division_name] == division_option]
    fig = px.bar(df_grouped, x="Rating", y='counts', color="age_group", title="Ratings by Age Group")
    st.plotly_chart(fig, use_container_width=True)

def create_animated_radar_chart(data):
    age_groups = [str(x) for x in data['age_groups']]
    # make figure
    fig_dict = {
        "data": [],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["xaxis"] = {"title": "Life Expectancy"}
    fig_dict["layout"]["yaxis"] = {"title": "GDP per Capita", "type": "log"}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 1200, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 300,
                                                                        "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 2,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Year:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 300, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 2,
        "steps": []
    }


    r = []
    theta = []

    for j in data['age_groups']:
        for i in data['age_groups'][j].keys():
            theta.append(i)
            r.append(data['age_groups'][j][i])
            if len(r)==5:
                break
        theta = ['one', 'two', 'three', 'four', 'five']
        r = [(x-statistics.mean(r))/(statistics.stdev(r)) for x in r]
        new_data = pd.DataFrame({'r':r, 'theta':theta})
        new_data.sort_values(by='r', inplace=True)
        break
    data_dict = {
            "r":new_data['r'],
            "theta":new_data['theta'],
            "fill":'toself',
            "type":'scatterpolar',
            "name": age_groups[0],
            "line_color":'rgb(0,128,128)',
            "fillcolor":'rgb(0,128,128)'
        }
    fig_dict["data"].append(data_dict)

    # make frames
    cnt = -1
    for age_group in age_groups:
        frame = {"data": [], "name": str(age_group)}
        # chart_data = converters.convert_string_to_dict(data[data['year']==float(year)]['concepts'])
        # sorted_chart_data = dict(reversed(sorted(chart_data.items(), key=lambda x:x[1])))
        r = []
        theta = []
        cnt+=1
        counter = -1
        for j in data['age_groups']:
            counter+=1
            if counter == cnt:
                for i in data['age_groups'][j].keys():
                    theta.append(i)
                    r.append(data['age_groups'][j][i])
                    if len(r)==5:
                        break
                theta = ['one', 'two', 'three', 'four', 'five']
                r = [(x-statistics.mean(r))/(statistics.stdev(r)) for x in r]
                new_data = pd.DataFrame({'r':r, 'theta':theta})
                new_data.sort_values(by='r', inplace=True)
                break
        data_dict = {
                "r":new_data['r'],
                "theta":new_data['theta'],
                "fill":'toself',
                "type":'scatterpolar',
                "name": age_group,
                "line_color":'rgb(0,128,128)',
                "fillcolor":'rgb(0,128,128)'
            }
            
        frame["data"].append(data_dict)

        fig_dict["frames"].append(frame)
        slider_step = {"args": [
            [age_group],
            {"frame": {"duration": 300, "redraw": True},
            "mode": "immediate",
            "transition": {"duration": 300}}
        ],
            "label": age_group,
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)

    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)

    fig.update_layout(
        margin=go.Margin(
            l=0,
            r=0,
            b=25,
            t=0,
            pad=10
        ))

    st.plotly_chart(fig, use_container_width=True)

def create_score_barchart_comparison(division_data, internal_data, division_name, division_option, compare):

    df_grouped = division_data.groupby([division_name, 'Rating']).size().reset_index(name='counts')
    df_grouped['counts'] = df_grouped['counts'] / df_grouped['counts'].sum()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_grouped['Rating'],
                y=df_grouped['counts'],
                name='Ratings for '+str(division_option),
                marker_color='rgb(256,48,48)'
    ))

    if compare == True:
        df_grouped = internal_data.groupby(['Department Name', 'Rating']).size().reset_index(name='counts')
        df_grouped_avg = df_grouped.groupby('Rating')['counts'].mean().reset_index()
        df_grouped_avg['counts'] = df_grouped_avg['counts'] / df_grouped_avg['counts'].sum()
        fig.add_trace(go.Bar(x=df_grouped_avg['Rating'],
                y=df_grouped_avg['counts'],
                name='Average Ratings',
                marker_color='rgb(220, 220, 220)'
        ))
    
        fig.update_layout(
            title='Ratings for '+str(division_option) + ' vs Average Ratings' ,
            xaxis_tickfont_size=14,
            yaxis=dict(
                title='Ratings Count',
                titlefont_size=16,
                tickfont_size=14,
            ),
            legend=dict(
                x=0,
                y=1.0,
                bgcolor='rgba(255, 255, 255, 0)',
                bordercolor='rgba(255, 255, 255, 0)'
            ),
            barmode='group',
            bargap=0.15, # gap between bars of adjacent location coordinates.
            bargroupgap=0.1 # gap between bars of the same location coordinate.
            )
    else:
        fig.update_layout(
        title='Ratings for '+str(division_option),
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Ratings Count',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15, # gap between bars of adjacent location coordinates.
        bargroupgap=0.1 # gap between bars of the same location coordinate.
        )
        
    st.plotly_chart(fig, use_container_width=True)

def create_pie_chart_from_json(data, col_name, title):
    x_col = list(data[col_name].keys())
    y_col = list(data[col_name].values())
    df = pd.DataFrame({col_name: x_col, 'count': y_col})
    df.sort_values(by=col_name, inplace=True)
    fig = go.Figure(
    data=[go.Pie(
        labels=df[col_name],
        values=df['count'],
        hole=.3,
        # Second, make sure that Plotly won't reorder your data while plotting
        sort=False)
    ])

    fig.update_traces(hoverinfo='label+percent', textinfo='none')
    
    fig.update_layout(
    title_font=dict(
        size=24,),
    legend_borderwidth=10,
    legend_font=dict(
        size = 18,
    ),
    font=dict(
        size=15,  # Set the font size here
    ),
    title={
        'text': title,
        'xanchor': 'left',
        'yanchor': 'top'})
    fig.update_layout(legend=dict(
    yanchor="top",
    y=1,
    xanchor="left",
    x=1
    ))
    st.plotly_chart(fig, use_container_width=True)

def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

def create_table(dataset):
    top_menu = st.columns(3)

    dataset = dataset[['Age', 'Rating', 'Review Text']]

    with top_menu[0]:
        sort_field = st.selectbox("Sort By", options=dataset.columns)
    with top_menu[2]:
        sort_direction = st.radio(
            "Direction", options=["⬆️", "⬇️"], horizontal=True
        )
    dataset = dataset.sort_values(
        by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
    )
    pagination = st.container()

    bottom_menu = st.columns((4, 1, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[25, 50, 100])
    with bottom_menu[1]:
        total_pages = (
            int(len(dataset) / batch_size) if int(len(dataset) / batch_size) > 0 else 1
        )
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

    pages = split_frame(dataset, batch_size)
    pagination.dataframe(data=pages[current_page - 1], use_container_width=True)



# Function to find synonyms using NLTK
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)

# Function to enrich keywords list and generate a word cloud
def generate_enriched_wordcloud(keywords, min_words=20, background_color="#0e1118", colormap="Pastel2"):
    nltk.download('wordnet')
    enriched_keywords = keywords.copy()
    if len(enriched_keywords) < min_words:
        word_frequencies = Counter(enriched_keywords)
        for word, _ in word_frequencies.most_common():
            if len(enriched_keywords) >= min_words:
                break
            synonyms = get_synonyms(word)
            enriched_keywords.extend(synonyms[:min_words - len(enriched_keywords)])
    
    wordcloud_text = ' '.join(enriched_keywords)
    wordcloud = WordCloud(
        background_color=background_color,
        colormap=colormap,
        max_words=100,
        width=800,
        height=400
    ).generate(wordcloud_text)
    
    # Create a matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    # ax.set_title("Enriched Word Cloud", fontsize=24)  # Optionally add a title
    
    return fig  # Return the figure object for further customization or saving


