import COVID19Py
from pandas import DataFrame, concat
from plotly.offline import plot
import plotly.graph_objects as go
import plotly.express as px
from numpy import log1p

covid19 = COVID19Py.COVID19()
locations = covid19.getLocations(timelines=True)
df = DataFrame([])
ph = []
for i, data in enumerate(locations):
    if data['country_code'] == 'PH':
        ph = data
    if df.empty:
        df = concat([DataFrame(data['latest'], index=[i]), DataFrame(data['coordinates'], index=[i])], axis=1)
        df.loc[i, 'country'] = data['country']
    else:
        sub_df = concat([DataFrame(data['latest'], index=[i]), DataFrame(data['coordinates'], index=[i])], axis=1)
        sub_df.loc[i, 'country'] = data['country']
        df = df.append(sub_df, sort=False)

for col in df.columns:
    if col != 'country':
        df[col] = df[col].astype(float)
size = log1p(df.confirmed)


def map_plot():
    """"""
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="country",
                            hover_data=['confirmed', 'deaths', 'recovered'], size=size,
                            color_discrete_sequence=['red'], zoom=2, height=800, width=1000,
                            center={'lat': 12, 'lon': 121})
    fig.update_layout(mapbox_style="carto-darkmatter")
    map_plt = plot(fig, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    return map_plt


def line():
    confirmed = ph['timelines']['confirmed']['timeline']
    deaths = ph['timelines']['deaths']['timeline']
    recovered = ph['timelines']['recovered']['timeline']

    confirmed = DataFrame(confirmed.values(), columns=['confirmed'], index=confirmed.keys())
    deaths = DataFrame(deaths.values(), columns=['deaths'], index=deaths.keys())
    recovered = DataFrame(recovered.values(), columns=['recovered'], index=recovered.keys())

    # print(confirmed)
    # Create traces
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=confirmed.index, y=confirmed.confirmed, mode='lines+markers', name='confirmed'))
    fig1.add_trace(go.Scatter(x=deaths.index, y=deaths.deaths, mode='lines+markers', name='deaths'))
    fig1.add_trace(go.Scatter(x=recovered.index, y=recovered.recovered, mode='lines+markers', name='recovered'))
    line_plt = plot(fig1, output_type='div', include_plotlyjs=False, show_link=False, link_text="")

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=confirmed.index, y=confirmed.confirmed, mode='lines+markers', name='confirmed'))
    fig2.add_trace(go.Scatter(x=deaths.index, y=deaths.deaths, mode='lines+markers', name='deaths'))
    fig2.add_trace(go.Scatter(x=recovered.index, y=recovered.recovered, mode='lines+markers', name='recovered'))
    fig2.update_layout(yaxis_type="log")
    log_plt = plot(fig2, output_type='div', include_plotlyjs=False, show_link=False, link_text="")
    return line_plt, log_plt