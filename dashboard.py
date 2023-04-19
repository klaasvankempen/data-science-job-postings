import pandas as pd
import plotly.express as px
import folium
from geopy.geocoders import Nominatim
from folium.plugins import HeatMap
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from custom_theme import my_theme
from streamlit_folium import st_folium
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt




# Import Data
df = pd.read_csv("./cleaned.csv")
df = df.drop("Unnamed: 0", axis=1)

######################################## Plot 1 ########################################
# Compute top 5 job titles
top_job_titles = df["clean_job_title"].value_counts().nlargest(5).index.tolist()

# Filter data to include only top 5 job titles
df_top_jobs = df[df["clean_job_title"].isin(top_job_titles)]

# Define custom color palette
colors = ["#FFA07A", "#FFC0CB", "#BA55D3", "#00BFFF", "#3CB371", "#FFD700"]

# Create bar graph
fig1 = px.histogram(
    df_top_jobs,
    x="clean_job_title",
    color="clean_job_title",
    color_discrete_sequence=colors,
    labels={"count": "Number of Job Postings"},
    hover_data={"clean_job_title": False},
    template="plotly_white",
)
fig1.update_traces(hovertemplate="<b>Number of Job Postings:</b> %{y}")

# Update layout
fig1.update_layout(
    title="Top 5 Job Titles by Number of Postings",
    xaxis_title="Job Title",
    yaxis_title="Number of Job Postings",
    xaxis={"categoryorder": "total descending", "tickmode": "array", "ticklen": 10},
    showlegend=False,
    height=600,
    hoverlabel=dict(font=dict(size=30)),
)
fig1.update_layout(my_theme["layout"])

######################################## Plot 2 ########################################

# Compute top 5 job titles
df_reduce = df[df["location"] != "United States"]
top_locations = df_reduce["location"].value_counts().nlargest(10).index.tolist()

# Filter data to include only top 5 job titles
df_top_locations = df[df["location"].isin(top_locations)]

# Define custom color palette
colors = [
    "#FFA07A",
    "#FFC0CB",
    "#BA55D3",
    "#00BFFF",
    "#3CB371",
    "#FFD700",
    "#FF1493",
    "#9370DB",
    "#20B2AA",
    "#F08080",
]

# Create bar graph
fig2 = px.histogram(
    df_top_locations,
    x="location",
    color="location",
    color_discrete_sequence=colors,
    labels={"count": "Number of Job Postings"},
    hover_data={"location": False},
    template="plotly_white",
)
fig2.update_traces(hovertemplate="<b>Number of Job Postings:</b> %{y}")

# Update layout
fig2.update_layout(
    title="Top 10 Locations by Number of Jobs",
    xaxis_title="Job Title",
    yaxis_title="Number of Job Postings",
    xaxis={"categoryorder": "total descending", "tickmode": "array", "ticklen": 10},
    showlegend=False,
    height=600,
    hoverlabel=dict(font=dict(size=30)),
)

fig2.update_layout(my_theme["layout"])


######################################## Plot 3 ########################################

# Compute top 5 job titles
top_job_titles = df["clean_job_title"].value_counts().nlargest(5).index.tolist()

# Filter data to include only top 5 job titles
df_top_jobs = df[df["clean_job_title"].isin(top_job_titles)]

# Compute top 5 job posting sites
top_sites = df["via"].value_counts().nlargest(5).index.tolist()


# Filter data to include only top 5 job titles
df_top_jobs = df_top_jobs[df_top_jobs["via"].isin(top_sites)]

# Compute percentages of work from home for each job title
job_title_percents = (
    df_top_jobs.groupby(["clean_job_title", "via"])["via"]
    .count()
    .groupby(level=0)
    .apply(lambda x: 100 * x / x.sum())
    .unstack()
)
colors = ["#FFA07A", "#FFC0CB", "#BA55D3", "#00BFFF", "#3CB371", "#FFD700"]

job_title_percents.fillna(0)
# Create stacked bar chart
fig3 = go.Figure(
    data=[
        go.Bar(
            name="Angel List",
            x=top_job_titles,
            y=job_title_percents["via AngelList"],
            marker_color=colors[0],
            hovertemplate="Percentage: %{y:.1f}%",
        ),
        go.Bar(
            name="Level",
            x=top_job_titles,
            y=job_title_percents["via Lever"],
            marker_color=colors[1],
            hovertemplate="<b>Percentage:</b> %{y:.1f}%",
        ),
        go.Bar(
            name="LinkedIn",
            x=top_job_titles,
            y=job_title_percents["via LinkedIn"],
            marker_color=colors[2],
            hovertemplate="<b>Percentage:</b> %{y:.1f}%",
        ),
        go.Bar(
            name="Upwork",
            x=top_job_titles,
            y=job_title_percents["via Upwork"],
            marker_color=colors[3],
            hovertemplate="<b>Percentage:</b> %{y:.1f}%",
        ),
        go.Bar(
            name="ZipRecruiter",
            x=top_job_titles,
            y=job_title_percents["via ZipRecruiter"],
            marker_color=colors[4],
            hovertemplate="<b>Percentage:</b> %{y:.1f}%",
        ),
    ]
)

# Update layout
fig3.update_layout(
    title="Job Postings by Site",
    xaxis_title="Job Title",
    yaxis_title="Percent of Job Postings",
    barmode="stack",
    xaxis={"categoryorder": "max descending", "tickmode": "array", "ticklen": 10},
    template="plotly_white",
    height=600,
    hoverlabel=dict(font=dict(size=30)),
)
fig3.update_layout(
    legend={"title": {"text": "Job Site", "font": {"size": 15}}, "font": {"size": 12}}
)
fig3.update_layout(my_theme["layout"], title_x=0.37)

fig3.update_xaxes(tickangle=0)

######################################## Plot 4 ########################################

df_reduce = df[df["location"] != "United States"]
df_reduce = df_reduce.dropna(subset=["location_coord"])

# Convert string coordinates to floats
heat_data = [eval(coord) for coord in df_reduce["location_coord"]]

# Create a Folium map centered on the US
m = folium.Map(location=[40, -95], zoom_start=4)

# Add heatmap layer
HeatMap(heat_data, radius=15).add_to(m)

######################################## Plot 5 ########################################

# Compute top 5 job titles
top_job_titles = df["clean_job_title"].value_counts().nlargest(5).index.tolist()

# Filter data to include only top 5 job titles
df_top_jobs = df[df["clean_job_title"].isin(top_job_titles)]

# Create a new column to represent work from home as a string for plotting
df_top_jobs["wfh_str"] = np.where(df_top_jobs["work_from_home"] == 1, "Yes", "No")

# Compute percentages of work from home for each job title
job_title_percents = (
    df_top_jobs.groupby(["clean_job_title", "wfh_str"])["work_from_home"]
    .count()
    .groupby(level=0)
    .apply(lambda x: 100 * x / x.sum())
    .unstack()
)
colors = ["#BA55D3", "#00BFFF"]

# Create stacked bar chart
fig5 = go.Figure(
    data=[
        go.Bar(
            name="No",
            x=top_job_titles,
            y=job_title_percents["No"],
            marker_color=colors[0],
            hovertemplate="Percentage: %{y:.1f}%",
        ),
        go.Bar(
            name="Yes",
            x=top_job_titles,
            y=job_title_percents["Yes"],
            marker_color=colors[1],
            hovertemplate="<b>Percentage:</b> %{y:.1f}%",
        ),
    ]
)

# Update layout
fig5.update_layout(
    title="Percentage of Work from Home Job Postings",
    title_x=0.5,
    xaxis_title="Job Title",
    yaxis_title="Percent of Job Postings",
    barmode="stack",
    xaxis={"categoryorder": "min ascending", "tickmode": "array", "ticklen": 10},
    legend=dict(title="Work From Home"),
    height=600,
    hoverlabel=dict(font=dict(size=30)),
)
fig5.update_xaxes(tickangle=0)
fig5.update_layout(my_theme["layout"], title_x=0.29)
fig5.update_layout(
    legend={
        "title": {"text": "Work From<br>Home Job", "font": {"size": 15}},
        "font": {"size": 12},
    }
)
######################################## Plot 6 ########################################

# Convert the minimum_education column to a categorical data type
df["minimum_education"] = df["minimum_education"].astype("category")

df_reduce = df[
    (df["clean_job_title"] == "Machine Learning Engineer")
    | (df["clean_job_title"] == "Data Scientist")
    | (df["clean_job_title"] == "Data Analyst")
    | (df["clean_job_title"] == "Deep Learning Engineer")
    | (df["clean_job_title"] == "Blockchain Engineer")
]

# Group the data by job title and minimum education
grouped = (
    df_reduce.groupby(["clean_job_title", "minimum_education"])
    .size()
    .reset_index(name="counts")
)

# Define a custom color scale
colors = ["#FFA07A", "#FFC0CB", "#BA55D3", "#00BFFF", "#3CB371", "#FFD700"]

# Create the sunburst plot
fig6 = px.sunburst(
    grouped,
    path=["clean_job_title", "minimum_education"],
    values="counts",
    color="clean_job_title",
    color_discrete_sequence=colors,
)

# Update the hovertemplate
fig6.update_traces(hovertemplate="<b>%{id} </b>" + "<br>Total Job Postings: %{value}")

# Update the layout with a title and axis labels
fig6.update_layout(
    title="Minimum Education Required by Job Title",
    xaxis=dict(title="Job Title"),
    yaxis=dict(title="Minimum Education"),
    uniformtext=dict(minsize=10, mode="hide"),
    height=600,
    width=600,
    hoverlabel=dict(font=dict(size=30)),
)
fig6.update_layout(uniformtext=dict(minsize=18, mode="hide"))
fig6.update_layout(my_theme["layout"], title_x=0.32)

######################################## Plot 7 ########################################

location_list = [
    "Washington, DC",
    "New York, NY",
    "San Francisco, CA",
    "Arlington, VA",
    "Chicago, IL",
    "Annapolis Junction, MD",
    "Herndon, VA",
    "Seattle, WA",
    "McLean, VA",
    "Paolo Alto, CA",
]
df_reduce = df_reduce[df_reduce["location"].isin(location_list)]
# Group the data by city and job title, count the number of occurrences
grouped = (
    df_reduce.groupby(["location", "clean_job_title"])
    .size()
    .reset_index(name="# of Job Postings")
)

colors = ["#FFA07A", "#FFC0CB", "#BA55D3", "#00BFFF", "#3CB371", "lightblue"]

# Create a treemap using plotly.express
fig7 = px.treemap(
    grouped,
    path=[px.Constant("USA"), "location", "clean_job_title"],
    values="# of Job Postings",
    color="clean_job_title",
    color_discrete_sequence=colors,
)

# Update the hovertemplate
fig7.update_traces(
    hovertemplate="<b>%{label} </b>" + "<br>Total Job Postings: %{value}"
)
# Update the layout with a title
fig7.update_layout(
    title="Most Common Job Titles by City",
    hoverlabel=dict(font=dict(size=30)),
    height=600,
)
fig7.update_layout(my_theme["layout"], title_x=0.32)
fig7.update_layout(uniformtext=dict(minsize=15, mode="hide"))

######################################## Plot 8 ########################################

grouped = df[
    (df["clean_job_title"] == "Machine Learning Engineer")
    | (df["clean_job_title"] == "Data Scientist")
    | (df["clean_job_title"] == "Data Analyst")
    | (df["clean_job_title"] == "Deep Learning Engineer")
    | (df["clean_job_title"] == "Blockchain Engineer")
]
grouped = grouped.drop("work_from_home", axis=1)
grouped = grouped.groupby("clean_job_title").mean() * 100

# create a heatmap using plotly express
fig8 = px.imshow(
    grouped,
    title="Required Skills by Job Type",
    y=grouped.index,
    labels=dict(
        x="Skills", y="Job Title", color="Percentage of Jobs <br> Requiring Skill"
    ),
    x=[
        "Python",
        "SQL",
        "Machine Learning",
        "Communication",
        "Software Engineering",
        "Deep Learning",
        "Language Processing",
        "Pytorch",
        "Computer Vision",
        "Tableau",
        "Management",
        "Tensorflow",
    ],
    color_continuous_scale="Blues",
)

# make the tooltip pretty
fig8.update_traces(
    hovertemplate="<b>Job Title:</b> %{y}<br>"
    + "<b>Skill:</b> %{x}"
    + "<br><b>Percentage of Jobs:</b>  %{z:.2f}%<br>"
)
fig8.update_layout(hoverlabel=dict(font=dict(size=30)), height=600)
fig8.update_layout(my_theme["layout"], title_x=0.4)
fig8.layout.coloraxis.colorbar.title = {
    "text": "Percentage of Jobs <br> Requiring Skill",
    "font": {"size": 20},
}
fig8.layout.coloraxis.colorbar.tickfont = {"size": 20}


######################################## Streamlit App ########################################

st.set_page_config(
    page_title="Data Science Job Postings Dashboard",
    page_icon="✅",
    layout="centered",
)

st.markdown(
    """
<style>
.big-font {
    font-size:80px !important;
}
</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    '<p class="big-font">Data Science Job Postings Dashboard</p>',
    unsafe_allow_html=True,
    )
st.text(" ")
st.markdown(
    """
   
    
    """
)

wch_colour_box = (0, 222, 0)
wch_colour_font = (0, 0, 0)
fontsize = 30
iconname = "fas fa-certificate"
sline = "Job Postings"
lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
i = 597
j = 425
k = 160

# create three columns
space2, kpi1, kpi2, kpi3, space3 = st.columns([0.8, 1, 1, 1, 1])


# fill in those three columns with respective metrics or KPIs

with kpi1:
    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {i}
                        </style><BR><span style='font-size: 20px; 
                        margin-top: 0;'>{sline}</style></span></p>"""

    st.markdown(lnk + htmlstr, unsafe_allow_html=True)

iconname = "fas fa-certificate"
sline = "Companies"
with kpi2:
    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {j}
                        </style><BR><span style='font-size: 20px; 
                        margin-top: 0;'>{sline}</style></span></p>"""

    st.markdown(lnk + htmlstr, unsafe_allow_html=True)

iconname = "fas fa-certificate"
sline = "Cities"
with kpi3:
    htmlstr = f"""<p style='background-color: rgb({wch_colour_box[0]}, 
                                              {wch_colour_box[1]}, 
                                              {wch_colour_box[2]}, 0.75); 
                        color: rgb({wch_colour_font[0]}, 
                                   {wch_colour_font[1]}, 
                                   {wch_colour_font[2]}, 0.75); 
                        font-size: {fontsize}px; 
                        border-radius: 7px; 
                        padding-left: 12px; 
                        padding-top: 18px; 
                        padding-bottom: 18px; 
                        line-height:25px;'>
                        <i class='{iconname} fa-xs'></i> {k}
                        </style><BR><span style='font-size: 20px; 
                        margin-top: 0;'>{sline}</style></span></p>"""

    st.markdown(lnk + htmlstr, unsafe_allow_html=True)

######################## Figure 1 ########################

st.markdown("***")
st.plotly_chart(fig1, use_container_width=True)

######################## Figure 2 ########################

st.markdown("***")
st.plotly_chart(fig2, use_container_width=True)


st.markdown("***")
st_folium(m, width=1400)

######################## Figure 7 ########################

st.markdown("***")
st.plotly_chart(fig7, use_container_width=True)

######################## Figure 3 ########################

st.markdown("***")
st.plotly_chart(fig3, use_container_width=True)

######################## Figure 5 ########################

st.markdown("***")
st.plotly_chart(fig5, use_container_width=True)

######################## Figure 6 ########################

st.markdown("***")
st.plotly_chart(fig6, use_container_width=True)

######################## Figure 8 ########################

st.markdown("***")
st.plotly_chart(fig8, use_container_width=True)
