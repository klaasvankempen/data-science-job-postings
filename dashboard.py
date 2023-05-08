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
from PIL import Image

# Import Data
df = pd.read_csv("./cleaned.csv")
df = df.drop("Unnamed: 0", axis=1)

######################################## Plot 1 ########################################
# find top 5 job titles
top_job_titles = df["clean_job_title"].value_counts().nlargest(5).index.tolist()

# filter data to include only top 5 job titles
df_top_jobs = df[df["clean_job_title"].isin(top_job_titles)]

# custom color palette
colors = ["#FFA07A", "#FFC0CB", "#BA55D3", "#00BFFF", "#3CB371", "#FFD700"]

# define bar graph
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

fig1.update_layout(
    title="Top 5 Job Titles by Number of Postings",
    xaxis_title="Job Title",
    yaxis_title="Number of Job Postings",
    xaxis={"categoryorder": "total descending", "tickmode": "array", "ticklen": 10},
    showlegend=False,
    height=400,
    hoverlabel=dict(font=dict(size=15)),
)
fig1.update_layout(my_theme["layout"])

######################################## Plot 2 ########################################

# find top 10 locations
df_reduce = df[df["location"] != "United States"]
top_locations = df_reduce["location"].value_counts().nlargest(10).index.tolist()

# filter data to include only top 10 locations
df_top_locations = df[df["location"].isin(top_locations)]

# custom color palette
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

# define bar graph
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

fig2.update_layout(
    title="Top 10 Locations by Number of Jobs",
    xaxis_title="Location",
    yaxis_title="Number of Job Postings",
    xaxis={"categoryorder": "total descending", "tickmode": "array", "ticklen": 10},
    showlegend=False,
    height=400,
    hoverlabel=dict(font=dict(size=15)),
)

fig2.update_layout(my_theme["layout"])


######################################## Plot 3 ########################################

# find top 5 job titles
top_job_titles = df["clean_job_title"].value_counts().nlargest(5).index.tolist()

# filter data to include only top 5 job titles
df_top_jobs = df[df["clean_job_title"].isin(top_job_titles)]

# find top 5 job posting sites
top_sites = df["via"].value_counts().nlargest(5).index.tolist()


# filter data to include only top 5 job posting sites
df_top_jobs = df_top_jobs[df_top_jobs["via"].isin(top_sites)]

# find percentages of work from home for each job title
job_title_percents = (
    df_top_jobs.groupby(["clean_job_title", "via"])["via"]
    .count()
    .groupby(level=0)
    .apply(lambda x: 100 * x / x.sum())
    .unstack()
)
colors = ["#FFA07A", "#FFC0CB", "#BA55D3", "#00BFFF", "#3CB371", "#FFD700"]

job_title_percents.fillna(0)
# define stacked bar chart, 1 trace for each job site
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

fig3.update_layout(
    title="Job Postings by Site",
    xaxis_title="Job Title",
    yaxis_title="Percent of Job Postings",
    barmode="stack",
    xaxis={"categoryorder": "max descending", "tickmode": "array", "ticklen": 10},
    template="plotly_white",
    height=500,
    hoverlabel=dict(font=dict(size=15)),
)
fig3.update_layout(
    legend={"title": {"text": "Job Site", "font": {"size": 15}}, "font": {"size": 10}}
)
fig3.update_layout(my_theme["layout"], title_x=0.29)

fig3.update_xaxes(tickangle=30)

######################################## Plot 4 ########################################

df_group = df.groupby("location").count()
df_cities = pd.DataFrame()
df_group.reset_index(inplace=True)
df_cities["city"] = df_group["location"]
df_cities["num_jobs"] = df_group["job_title"]
i = 0
df_cities["top_company"] = ""
df_cities["top_job_title"] = ""
for city in df_cities["city"]:
    df_cities["top_company"].iloc[i] = df[df["location"]==city]["company_name"].value_counts().reset_index()["index"].iloc[0]
    df_cities["top_job_title"].iloc[i] = df[df["location"]==city]["clean_job_title"].value_counts().reset_index()["index"].iloc[0]
    i += 1
df_cities = df_cities.merge(df[["location_coord", "location"]], left_on = "city", right_on = "location")
# filter data to remove USA as location
df_cities = df_cities[df["location"] != "United States"]
df_cities = df_cities.dropna(subset=["location_coord"])

# change coordinates from string to floats
df_cities["location_coord"] = [eval(x) for x in df_cities["location_coord"]]

def popup_table(i):
    # Define variables needed
    location = df_cities["city"].iloc[i]
    number_of_jobs = df_cities["num_jobs"].iloc[i]
    company = df_cities["top_company"].iloc[i]
    job_title = df_cities["top_job_title"].iloc[i]
    # Define html that combines a table to information next to the bar chart for each county
    html =""" <!DOCTYPE html>
<html>
<head>
<h4>{}</h4>""".format(location) + """
</head>
<body>
<table>
<tr>
<td>
<table style="width: 250px;color: black;">
<tbody>
<tr>
<th style="background-color: #CCCCCC" ;"><span style="color: black;">Number of Job Postings</span>
</td>
<td style="width: 75px;text-align: center;background-color: #CCCCCC" ;">{}</td>""".format(number_of_jobs) + """
</tr>
<tr>
<th style="background-color: #e3e3e3" ;"><span style="color: black;">Top Company</span></td>
<td style="width: 75px;text-align: center;background-color: #e3e3e3" ;">{}</td>""".format(company) + """
</tr>
<tr>
<th style="background-color: #CCCCCC" ;"><span style="color: black">Top Job Title</span></td>
<td style="width: 75px;text-align: center;background-color: #CCCCCC" ;">{}</td>""".format(job_title) + """
</tr>
</tbody>
</table>
</td>
</tr>
</table>
</body>
</html>
"""
    return html

loc_dict = {}
loc_dict["Washington, DC"] = [39,-76]
loc_dict["USA"] = [40,-70]
loc_dict["New York, NY"] = [40.75,-73]
loc_dict["Boston, MA"] = [42.5,-70]
loc_dict["San Francisco, CA"] = [37.75,-121]



######################################## Plot 5 ########################################

# find top 5 job titles
top_job_titles = df["clean_job_title"].value_counts().nlargest(5).index.tolist()

# filter data to include only top 5 job titles
df_top_jobs = df[df["clean_job_title"].isin(top_job_titles)]

# define a new column to represent work from home as a factor
df_top_jobs["wfh"] = np.where(df_top_jobs["work_from_home"] == 1, "Yes", "No")

# find percentage of work from home jobs for each job title
job_title_percents = (
    df_top_jobs.groupby(["clean_job_title", "wfh"])["work_from_home"]
    .count()
    .groupby(level=0)
    .apply(lambda x: 100 * x / x.sum())
    .unstack()
)
colors = ["#BA55D3", "#00BFFF"] # custom colors

# define stacked bar chart, trace for wfh and no wfh
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

fig5.update_layout(
    title="Percentage of Work from Home Job Postings",
    title_x=0.5,
    xaxis_title="Job Title",
    yaxis_title="Percent of Job Postings",
    barmode="stack",
    xaxis={"categoryorder": "min ascending", "tickmode": "array", "ticklen": 10},
    legend=dict(title="Work From Home"),
    height=500,
    hoverlabel=dict(font=dict(size=15)),
)
fig5.update_xaxes(tickangle=0)
fig5.update_layout(my_theme["layout"], title_x=0.20)
fig5.update_layout(
    legend={
        "title": {"text": "Work From<br>Home Job", "font": {"size": 10}},
        "font": {"size": 10},
    }
)
fig5.update_xaxes(tickangle=30)

######################################## Plot 6 ########################################

# change the minimum_education column categorical data
df["minimum_education"] = df["minimum_education"].astype("category")

df_reduce = df[
    (df["clean_job_title"] == "Machine Learning Engineer")
    | (df["clean_job_title"] == "Data Scientist")
    | (df["clean_job_title"] == "Data Analyst")
    | (df["clean_job_title"] == "Deep Learning Engineer")
    | (df["clean_job_title"] == "Blockchain Engineer")
]

# group data by job title and minimum education level
grouped = (
    df_reduce.groupby(["clean_job_title", "minimum_education"])
    .size() # find size of each group
    .reset_index(name="counts")
)

# custom color scale
colors = ["#FFA07A", "#FFC0CB", "#BA55D3", "#00BFFF", "#3CB371", "#FFD700"]

# define the sunburst plot with job title as center and minimum education as second step in path
fig6 = px.sunburst(
    grouped,
    path=["clean_job_title", "minimum_education"],
    values="counts",
    color="clean_job_title",
    color_discrete_sequence=colors,
)

# change the hovertemplate
fig6.update_traces(hovertemplate="<b>%{id} </b>" + "<br>Total Job Postings: %{value}")

fig6.update_layout(
    title="Minimum Education Required by Job Title",
    xaxis=dict(title="Job Title"),
    yaxis=dict(title="Minimum Education"),
    height=600,
    width=600,
    hoverlabel=dict(font=dict(size=15)),
)
fig6.update_layout(my_theme["layout"], title_x=0.22)

######################################## Plot 7 ########################################
# Define list of locations that we want in the data
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
# keep only desired locations
df_reduce = df_reduce[df_reduce["location"].isin(location_list)]
# group the data by city and job title
grouped = (
    df_reduce.groupby(["location", "clean_job_title"])
    .size() # find the size of each group
    .reset_index(name="# of Job Postings")
)
# custom colors
colors = ["#FFA07A", "#FFC0CB", "#BA55D3", "#00BFFF", "#3CB371", "lightblue"]

# define treemap 
fig7 = px.treemap(
    grouped,
    path=[px.Constant("USA"), "location", "clean_job_title"],
    values="# of Job Postings",
    color="clean_job_title",
    color_discrete_sequence=colors,
)

# update the hovertemplate
fig7.update_traces(
    hovertemplate="<b>%{label} </b>" + "<br>Total Job Postings: %{value}"
)
fig7.update_layout(
    title="Most Common Job Titles by City",
    hoverlabel=dict(font=dict(size=15)),
    height=600,
)
fig7.update_layout(my_theme["layout"], title_x=0.30)
fig7.update_layout(uniformtext=dict(minsize=8, mode="hide"))

######################################## Plot 8 ########################################
# keep only top 5 job titles in data
grouped = df[
    (df["clean_job_title"] == "Machine Learning Engineer")
    | (df["clean_job_title"] == "Data Scientist")
    | (df["clean_job_title"] == "Data Analyst")
    | (df["clean_job_title"] == "Deep Learning Engineer")
    | (df["clean_job_title"] == "Blockchain Engineer")
]
# drop work from home variable
grouped = grouped.drop("work_from_home", axis=1)
# group by job title and find mean of every other category
# each variable is a boolean so we can take the mean and muliptly times 100 to get percentage of jobs requiring each skill
grouped = grouped.groupby("clean_job_title").mean() * 100

# define heatmap 
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

# adjust the tooltip
fig8.update_traces(
    hovertemplate="<b>Job Title:</b> %{y}<br>"
    + "<b>Skill:</b> %{x}"
    + "<br><b>Percentage of Jobs:</b>  %{z:.2f}%<br>"
)
fig8.update_layout(hoverlabel=dict(font=dict(size=15)), height=400)
fig8.update_layout(my_theme["layout"], title_x=0.30)
fig8.layout.coloraxis.colorbar.title = {
    "text": "Percentage of Jobs <br> Requiring Skill",
    "font": {"size": 12},
}
fig8.update_layout(yaxis=dict(tickfont=dict(size=10)))
fig8.layout.coloraxis.colorbar.tickfont = {"size": 12}

fig8.update_xaxes(tickangle=30)

######################################## Plot 9 ########################################
company_list = ["Booz Allen Hamilton",
"Apple",
"Deloitte",
"Walmart"]
top_job_titles = df["clean_job_title"].value_counts().nlargest(5).index.tolist()

df_reduce = df[df["company_name"].isin(company_list)]
df_reduce = df_reduce[df_reduce["clean_job_title"].isin(top_job_titles)]

# Group the data by job title and company
grouped = (
    df_reduce.groupby(["company_name", "clean_job_title"])
    .size()
    .reset_index(name="counts")
)

# Define a custom color scale
colors = ["#FFA07A", "#FFC0CB", "#BA55D3", "#00BFFF", "#3CB371", "#FFD700"]

# Create the sunburst plot
fig9 = px.sunburst(
    grouped,
    path=["company_name", "clean_job_title"],
    values="counts",
    color="company_name",
    color_discrete_sequence=colors,
)

# Update the hovertemplate
fig9.update_traces(hovertemplate="<b>%{id} </b>" + "<br>Total Job Postings: %{value}")

# Update the layout with a title and axis labels
fig9.update_layout(
    title="Job Postings by Company",
    height=600,
    width=600,
)
fig9.update_layout(my_theme["layout"], title_x=0.32)

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
    font-size:60px !important;
}
</style>
""",
    unsafe_allow_html=True,
)


st.markdown(
    '<center><p class="big-font">Data Science Job Postings Dashboard</p></center>',
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
kpi1, kpi2, kpi3 = st.columns(3)


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
st.markdown("**Introduction**")
st.markdown("Data science is a hot job market right now. The Bureau of Labor Statistics (BLS) estimates that the demand for data scientists will grow 36% between 2021 and 2031, making it one of the best careers to be in. With nearly 14,000 job openings per year, it can be a difficult market to navigate for data science professionals. Additionally, data science is a broad career, with many subfields. Machine learning, data analysts, and cloud engineers all share similar “data science” skills but perform different day to day duties. This analysis will give an overview of the data science job market and furthermore give insights into the qualifications and skills needed for data scientists in today's job market. ")
st.markdown("**About the Data**")
st.markdown("This project uses data science job posting data. The data was webscraped from different job listing websites. Two searches were perfomed, one for Washington, DC and another for the rest of the United States. Therefore Washington, DC and its surrounding areas are over represnted in this data.")
st.markdown("***")
st.markdown("The number one data science related job in terms of number of job postings is Machine Learning Engineer. Followed closely by Data Scientist and Data Analyst. Deep Learning Engineers and Blockchain Engineers are also common job postings, all other job postings have fewer than 14 total posts, in this dataset.")
st.plotly_chart(fig1, use_container_width=True)
st.markdown("**_Figure 1_**: An overview of the top 5 job titles for data science roles. Hovering over each category shows the exact number of job postings for that job title.")
######################## Figure 2 ########################

st.markdown("***")
st.markdown("Another important aspect of the job market is where the jobs are located.Due to the nature of the data collection, Washington DC has the greatest number of job postings, followed by New York and San Francisco. This backs up the general understanding that tech roles are located in big cities and primarily in tech hubs such as New York and San Francisco.")
st.plotly_chart(fig2, use_container_width=True)
st.markdown("**_Figure 2_**: An overview of the top 10 cities with the greatest number of job postings. Washington, DC and its surrounding areas are over represented due to the data collection")


st.markdown("***")
st.markdown("Not everyone can just move to a tech hub to land a data science job. Figure 3 provides an indepth view of where the jobs are located in the United States. By clicking on icons for certain cities you can unveil lots of information about the job market in those cities. For example in DC there are 33 open jobs, and the top job title is Data Analyst while in San Francisco the top job title in Machine Learning Engineer. This allows candidates to get a better understanding of what jobs are availible in the city they are located in.")
selection = st.selectbox(label = "Select a Location", options = ["USA", "Washington, DC", "New York, NY", "Boston, MA", "San Francisco, CA"])
zoom = 9
if selection == "USA":
    zoom = 4
# Initialize Folium Map centered on USA
fig = folium.Map(location=loc_dict[selection], tiles="OpenStreetMap", zoom_start=zoom)
# Define empty datagroup 
data_group = folium.FeatureGroup(name='Data')

# for each observation (bubble on plot)
for i in range(0, len(df_cities)):
    html = popup_table(i) # run html function defined above to get html output for that county
    data_group.add_child(folium.Marker( # add bubble plot
        location=df_cities["location_coord"].iloc[i], # set bubble at longitude and latitude
        popup= folium.Popup(folium.Html(html, script = True)), # add html output to folium popup
        fill=True,
        weight=3,
        opacity=1,
        fillopacity=0.9,
        ))
fig.add_child(data_group) # add datagroup to figure
st_folium(fig, width=1400, height=400)
st.markdown("**_Figure 3_**: Icons indicate all 157 cities which have data science job postings. Selecting a city from the dropdown will zoom into that city. Aditionally, clicking on each icon will show the number of job postings, the top job title, and the top company in that city.")

######################## Figure 7 ########################

st.markdown("***")
st.markdown("Expanding on Figure 3, this tree map gives an indepth look at the types of jobs availbile in the top 10 cities. Machine Learning Engineers are needed more in New York and San Francisco while Data Scientists and Data Analysts are more desired in DC and Chicago. Typically SF and NY have been seen as tech hubs more than DC and Chicago, therefore it makes sense that they desire the higher technical positions such as machine learning, blockchain, and deep learning engineers.")
st.plotly_chart(fig7, use_container_width=True)
st.markdown("**_Figure 4_**: The total number of job postings for each job title in the top 10 cities. Size of each block represents the relative number of job postings for that job title/city combination. Hovering over each block will show the number of job postings.")

######################## Figure 9 ########################

st.markdown("***")
st.markdown("Top companies also differ in the types of jobs that they offer. Apple, Booz Allen Hamilton, and Deloitte all desire Machine Learning Engineers while Walmart needs more Data Analysts. Apple also needs deep learning engineers, but no data scientists while Booz Allen Hamilton and Deloitte need Data Scientists and Analysts but no Deep Learning Engineers. This backs up the finding from figure 4 that tech based companies (Apple) desire more tech based roles such as Machine Learning/Deep Learning engineers while non-tech companies like Walmart need more data scientists and data analysts.")
st.plotly_chart(fig9, use_container_width=True)
st.markdown("**_Figure 5_**: This figure shows the 4 companies with the most job postings and type of job titles they offer. Clicking on a company will filter the plot to only show that company.")

######################## Figure 3 ########################

st.markdown("***")
st.markdown("In the previous figures we have examined the locations and job titles of the data science market to give job searchers an oveview of the job market. It is also useful for candiates to know how to best search for jobs which is shown in Figure 6. Machine Learning Engineer jobs are only posted on Zip Recuiter and Angel List. Data Scientists and Data Aanalyst positions are posted mostly on LinkedIn, ZipRecruiter, and Level.")
st.plotly_chart(fig3, use_container_width=True)
st.markdown("**_Figure 6_**: The top 5 job titles and the recruiting sites the jobs were posted on. The bars represent the percentage of the job postings for each job title that were found on the corresponding job site")
######################## Figure 5 ########################

st.markdown("***")
st.markdown("Since the pandemic many jobs have become work from home or hybrid. Many candidates may value this as an important aspect of their job. Candidates who want to work from home are more likely to find that in Machine Learning and Blockchain Engineering jobs than the other job positions. However, even with the post pandemic shift in working style, the vast majority of jobs are still in-person. This may be a reflection of the recent push by CEO's to get employees back to the office, and therefore most new hires are in person roles.")
st.plotly_chart(fig5, use_container_width=True)
st.markdown("**_Figure 7_**: This figure shows the percentage of jobs that are work from home for each of the top 5 job titles.")
######################## Figure 6 ########################

st.markdown("***")
st.markdown("Candidates wanting to break into the data science career should also be aware of the education requirements. Most if not all jobs require at least a bachelors degree, however many roles require advanced degrees to even apply. Those with only a Bachelors degree can find jobs in all of the top fields, however they will find the most success in finding data analyst and blockchain engineer positions. Those with advanced degrees will be strong candidates for any role, however they will be specifically desired as Deep Learning and Machine Learning Engineers. These roles are typically require a higher level of mathematics and statistics which is why they often require advanced degrees.")
st.plotly_chart(fig6, use_container_width=True)
st.markdown("**_Figure 8_**: This figure shows the breakdown of the minimum education required for each of the top 5 job titles. Clicking on a job title will filter the plot to only show job postings of that job title.")

######################## Figure 9 ########################
img = Image.open("word_cloud.png")
st.markdown("***")
st.markdown("Data Science roles typically require a lot of skills to succeed, both techinical and soft skills. The required qualifications of job roles are good indicators of what companies believe is necessary to be successful in the data science industry. Figure 9 shows that the most important qualifications are 'Machine Learning', 'Python', 'Computer Science', 'Experience', and 'Communication Skills'. Candidates who hope not only find a job but succeed as data scientists should focus on developing these skills. Interestingly, the required qualifications are mostly hard skills, not soft skills. Indicating that just to land a job you may be better off focusing on your hard skills.")
st.markdown(
    """
<style>
.small-font {
    font-size:25px !important;
}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown(
    '<center><p class="small-font"><b>Word Cloud of Required Qualifications</b></p></center>',
    unsafe_allow_html=True,
)
st.image(img)

st.markdown('**_Figure 9_**: A wordcloud showing the most common words used in the "Qualifications" section of the job posting')
######################## Figure 8 ########################

st.markdown("***")
st.markdown("Figure 9 showed many of the most desirable skills for data science positions. However, different job titles will require different skills. In figure 10 this difference is highlighted. Python for example is required by more than 50% of Data science, deep learning, and machine learning jobs but only a quarter of data analyst and blockchain engineering jobs require it. Pytorch, a popular deep learning library, is desired only in Deep Learning and Machine Learning roles. Management is only really required for data anlysts. Clearly there are significant differences in the required skills and background of different roles and candidates should strive to gain the skills for the specific job title they want to have.")
st.plotly_chart(fig8, use_container_width=True)

st.markdown("**_Figure 10_**: This figure shows the percentage of job postings requiring each skill accross the top 5 job titles. Hovering over each block will show the exact percentage of jobs requiring that skill.")

st.markdown("***")
st.markdown("**Conclusions**")
st.markdown("An overview of the data science job market revealed the following insights")
st.markdown("**1.** Data Science Jobs are located in major cities, specifically tech hubs")
st.markdown("**2.** Tech focused cities (SF, NY) have more Machine Learning and Deep Learning Jobs, while other cities have more Data Scientist and Data Analyst jobs.")
st.markdown("**3.** Tech companies have more Machine Learning and Deep Learning Jobs compared to non-tech Fortune 500 companies.")
st.markdown("**4.** Certain Job titles are more common on different recruiting sites. ZipRecruiter has jobs from all job titles.")
st.markdown("**5.** Different Job titles have very different skill and education requirements. More technical positions like Machine Learning Engineers require more education and more technical skills. Data Analysts need more soft skills like communication and management" )

st.markdown("The data science field is very large and there are plenty of opportunities available. However, it can still be difficult to break into the field. This analysis gives a roadmap to candidates to optimize their job search given their location and experience.")