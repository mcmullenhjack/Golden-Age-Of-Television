import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import numpy as np
import base64

shows = pd.read_csv('https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2019/2019-01-08/IMDb_Economist_tv_ratings.csv')

tv_shows = shows['title'].unique()

shows['year'] = shows['date'].apply(lambda x: x[0:4])
years = shows['year'].sort_values().unique()

def trend_color(df, variable_str):
    try: 
        if df[variable_str].iloc[0] > df[variable_str].iloc[-1]:
            #fill_color = '#FF0000'
            fill_color = 'rgba(255, 0, 0, 0.4)'
            line_color = 'rgb(255, 0, 0)'
        elif df[variable_str].iloc[0] < df[variable_str].iloc[-1]:
            #fill_color = '#2FFF00'
            fill_color = 'rgba(47, 255, 0, 0.3)'
            line_color = 'rgb(47, 255, 0)'
        else:
            #fill_color = '#0091FF'
            fill_color = 'rgba(0, 145, 255, 0.3)'
            line_color = 'rgb(0, 145, 255)'
        return [fill_color, line_color]
    except:
        fill_color = 'rgba(255, 255, 0, 0.3)'
        line_color = 'rgb(255, 255, 0)'
        return [fill_color, line_color]




app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

server = app.server
app.title='The Golden Age of Television'

# image_filename = '/Users/jackmcmullen/First_dashboard_stuff/assets/hackcville-logo.png'
image_filename = '/assets/hackcville-logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


# app.css.append_css({
#     "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
#       #'external_url':'https://raw.githubusercontent.com/plotly/dash-app-stylesheets/master/dash-analytics-report.css'
# })

# image_filename = '/Users/jackmcmullen/First_dashboard_stuff/assets/hackcville-logo.png'
# encoded_image = base64.b64encode(open(image_filename, 'rb').read())

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    )

app.layout = html.Div(children=[
    #dcc.Input(id='input', value='Type a TV Show', type='text'),
    #html.Div(id='output-graph'),
#     html.H1('The Golden Age of Television'),
    html.Div([
        html.Div([html.Img(
#                 src=app.get_asset_url("python-logo.png"),
                src = 'data:image/png;base64,{}'.format(encoded_image.decode()),
                id="plotly-image",
                style={
                    "height": "95px",
                    "width": "95px",
                    "margin-bottom": "0px",
                },
            )
        ],
        className="one-third column",
    ), 
        html.Div(
        [
            html.Div(
                [
                    html.H2(
                        "The Golden Age of Television",
                        style={"margin-bottom": "0px", 'textAlign':'center', 'margin-right':'100px', 'color':'white'},
                    ),
                    html.H5(
                        "An Analysis of TV Shows Since 1990", style={"margin-top": "0px", 'textAlign':'center', 'margin-right':'100px', 'color':'white'}
                    ),
                ]
            )
        ], className = 'ten columns', id='title'),
        
        html.Div(
        [
            html.A(
                    html.Button('Data Source', id='dataset-button', style=dict(backgroundColor='#1e72be', color='white')),
                                href='https://github.com/rfordatascience/tidytuesday/tree/master/data/2019/2019-01-08')
            ], className='one-third column', id='button')
      
        ], className = 'row flex-display', style={"margin-bottom": "25px"}),
    html.Div([
        html.Div([
            html.Div([ 
                html.Div(dcc.Dropdown(id='tv-show-name',
                                 options=[{'label': show, 'value': show}
                                           for show in tv_shows],
                                 placeholder = 'Type or Choose a TV Show',
                                 multi=False     
                                 ), className='dcc_control'),
                html.Div(dcc.Dropdown(id='year',
            #                      options=[{'label': year, 'value': year}
            #                                for year in years],
                                 placeholder = 'Select a Year',
                                 multi=False     
                                 ), className='dcc_control')
                ], 
                    className = 'pretty_container four columns'
            )#,
#             html.Div(
#                 html.Div((html.Div(children = html.Div(id='year-graphs', className = 'pretty_container'))), className='twelve columns')
#             )
#         ], id='left-column', className = 'four columns'),
    ]),
        html.Div([
            html.Div([
               html.Div([html.H6(id = 'tv_show_name_box', style=dict(color = 'white')), html.P('TV Show', style=dict(color = 'white'))],
                        id = 'tv-show-box',
                        className='mini_container'),
               html.Div([html.H6(id = 'best_rating', style=dict(color = 'white')), html.P('Best Season Rating', style=dict(color = 'white'))],
                       id = 'best-rating-box',
                       className = 'mini_container'),
               html.Div([html.H6(id = 'year_value', style=dict(color = 'white')), html.P('Year Selected', style=dict(color = 'white'))],
                       id = 'year-selected-box',
                       className = 'mini_container'),
               html.Div([html.H6(id = 'show_rank', style=dict(color = 'white')), html.P('Show Ranking During Year', style=dict(color = 'white'))],
                       id = 'show-rank-box',
                       className = 'mini_container')
                   ], id = 'info-container', className= 'row container-display')#,

#            html.Div(
#                  html.Div((html.Div(children = html.Div(id='graphs', className='pretty_container'))), className='twelve columns'),
                 
#                 )
            ], 
        id='right-column',
        className='seven columns')
    ]),
    
    html.Div([
            html.Div([dcc.Graph(id='year-graphs', config=dict(displayModeBar=False))],
                    className = 'pretty_container six columns'), 
        
            html.Div([dcc.Graph(id = 'graphs', config=dict(displayModeBar=False))], 
                     className='pretty_container five columns'),
        ])
], style={"display": "flex", "flex-direction": "column"})
    #     html.Div(dcc.Dropdown(id='show_after_year',
#                           options=[{'label': show, 'value': show},
#                                       for show in tv_shows]))
#     html.Div([
#         html.Div((html.Div(children = html.Div(id='graphs', className='pretty_container'))), className='eight columns'),
#         html.Div((html.Div(children = html.Div(id='year-graphs', className = 'pretty_container'))), className='eight columns')
#     ], className='row flex-display')


# @app.callback(
#     Output(component_id='output-graph', component_property='children'),
#     [Input(component_id='input', component_property='value')])


# @app.callback(
#     Output('year', 'value'),
#     Input('year', 'options'))
# def set_year_value(available_options):
#     return available_options

@app.callback(
#     Output(component_id='graphs', component_property='children'),
    Output(component_id='graphs', component_property='figure'),
    [Input(component_id='tv-show-name', component_property='value')])

def update_graph(tv_shows):
    graphs = []
    
#     if len(tv_shows)>2:
#         class_choice = 'col s12 m6 l4'
#     elif len(tv_shows) == 2:
#         class_choice = 'col s12 m6 l6'
#     else:
#         class_choice = 'col s12' 
    try:
        #for tv_show in tv_shows:
        tv_show_data = shows.loc[shows['title'] == tv_shows]
        years_running = list(tv_show_data['year'])
        years_running_str = '(' + years_running[0] + '-' + years_running[-1] + ')'

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=tv_show_data['seasonNumber'], 
                                y = tv_show_data['av_rating'],
                                name = 'Average IMDb Rating',
                                fill = 'tozeroy',
                                fillcolor = trend_color(tv_show_data, 'av_rating')[0],
                                line = dict(color = trend_color(tv_show_data, 'av_rating')[1])))

        fig.add_trace(go.Scatter(x=tv_show_data['seasonNumber'],
                                 y = tv_show_data['share'],
                                 name = 'Share of Viewers',
                                 fill = 'tozeroy',
                                 fillcolor = trend_color(tv_show_data, 'share')[0],
                                 line = dict(color = trend_color(tv_show_data, 'share')[1], dash='dash')
                                     ))

        fig.update_layout(title = dict(text = 'Average Rating and Viewer Share Per Season for <br> {} {}'.format(tv_shows, years_running_str),
                                       xanchor='center',
                                       x = 0.5, y = .96),
                                       margin=dict(l=15, r=15, t=60, b=20),
                                      legend=dict(x=0.05, y = 1.08, bgcolor = 'rgba(0,0,0,0)'),
                                       legend_orientation = 'h',
                                      font = dict(size = 10,
                                          color = 'white',
                                          family = 'Times New Roman'),
                                      autosize=True,
                                      #xaxis_title='Season Number',
                                      xaxis = dict(title_text='Season Number',
                                                   title_font={'size': 16},
                                                   tickmode='linear',
                                                   tickfont = {'size':12}),
                                      yaxis=dict(tickfont = {'size':12},
                                                 tickmode = 'linear'),
                                      paper_bgcolor = '#192444',
                                      plot_bgcolor = '#192444')
                                      #autosize=False, width=425)
        fig.update_xaxes(title_standoff = 25)

        #graphs.append(
        return fig
#         return html.Div(dcc.Graph(
#                       id=tv_shows,
#                       figure = fig  #{
#                           'data': [graph_data_rating],
#                           'layout': {'title': 'Average Rating Per Season for {}'.format(tv_show)},}

#                  ))

#     return graphs

    except:
        pass

@app.callback(
    Output('year', 'options'),
    [Input('tv-show-name', 'value')])
def set_year_options(selected_show):
    possible_years = shows.loc[shows['title']==selected_show, 'year'].unique()
    options = {selected_show: possible_years}
    return [{'label': i, 'value': i} for i in possible_years]

@app.callback(
    Output('tv_show_name_box', 'children'),
    [Input('tv-show-name', 'value')])
def tv_name_for_box(selected_show):
    return selected_show

@app.callback(
    Output('best_rating', 'children'),
    [Input('tv-show-name', 'value')])
def best_rating_for_show(selected_show):
    try:
        return round(list(shows.loc[shows['title']==selected_show, 'av_rating'].sort_values(ascending=False))[0], 2)
    except:
        pass

@app.callback(
    Output('year_value', 'children'),
    [Input('year', 'value')])
def year_chosen(selected_year):
    return selected_year

@app.callback(
    Output('show_rank', 'children'),
    [Input('year', 'value'),
        Input('tv-show-name', 'value')])
def rank_of_show_during_year(selected_year, selected_show):
    df = shows.loc[shows['year']==selected_year].groupby('title').mean()['av_rating'].sort_values(ascending=False).reset_index()
    df['rank'] = range(1, df.shape[0]+1)
    try:
        return list(df.loc[df['title']==selected_show, 'rank'])[0]
    except:
        pass


@app.callback(
#     Output(component_id='year-graphs', component_property='children'),
    Output(component_id='year-graphs', component_property='figure'),
    [Input(component_id='year', component_property='value'),
        Input(component_id='tv-show-name', component_property='value')]
)

def update_year_graphs(year, tv_show_name):
    year_graphs = []
    
    try:
    #         for year in years:
        #yearly_data = shows.loc[shows['year'] == year]

        test = shows.loc[shows['year']==year].groupby('title').mean()['av_rating'].sort_values(ascending=False).reset_index()
        test['rank'] = range(1, test.shape[0]+1)
        test['rank'] = test['rank'].astype(str)
        test_10 = test.iloc[:10, :]
        show_row = test.loc[test['title']==tv_show_name]
        test_10 = test_10.append(show_row, ignore_index=True)
        #test_10 = test_10.sort_values('av_rating')

        title_ranks = []
        for title, rank in zip(test_10['title'], test_10['rank']):
            title_ranks.append(rank + '. ' + title)

        test_10['rank_title'] = title_ranks

        test_10['selected_show']  = np.where(test_10['title'] == tv_show_name, 'Yes', 'No')
        
        if int(test_10.loc[test_10['title']==tv_show_name].reset_index()['rank'][0]) > 10:
            bar_colors = ['#ed6363'] + ['#278ea5']*10 

        elif int(test_10.loc[test_10['title']==tv_show_name].reset_index()['rank'][0]) <= 10:
            show_index = test_10.loc[test_10['title']==tv_show_name, 'rank'].index[0]
            bar_colors = ['#278ea5']*10 #['#69779b']*10 #['#115173']*10 #['#7045af']*10
            bar_colors[show_index] = '#ed6363'
            bar_colors = list(reversed(bar_colors))
            test_10 = test_10.iloc[:-1, :]
        
        test_10 = test_10.sort_values('av_rating', ascending=True)
            
        top_10_fig = go.Figure(data = go.Bar(x=test_10['av_rating'], y=test_10['rank_title'], 
                         orientation='h', 
                         text=round(test_10['av_rating'], 2),
                         textposition='outside',
                         textfont=dict(color = 'white'),
                         marker_color = bar_colors),
                         layout=go.Layout(autosize=True,
                                          title=dict(text='Top 10 TV Shows in {}'.format(year),
                                                     xanchor='center',
                                                     x=0.5, y=0.98),#,
                                          font = dict(size = 12,
                                                #color = '#7f7f7f',
                                                color = 'white',
                                                family = 'Open Sans'),
                                          #textfont = dict(color = 'white'),
                                          margin = dict(r = 15, b = 15, t = 30),
                                          xaxis_title = 'Average IMDb Rating',
                                          paper_bgcolor = '#192444',
                                          plot_bgcolor = '#192444'))
        
    #             test = yearly_data.groupby('title').mean()['av_rating'].sort_values().reset_index()

    #             fig_year = go.Figure(go.Bar(x=test['av_rating'][-10:], y=test['title'][-10:], orientation='h'))

#         top_10_fig.update_layout(title = dict(text = 'Top 10 TV Shows in {}'.format(year),
#                                                    xanchor='center',
#                                                    x = 0.5, y = .98),
#                                  #margin=dict(l=0, t=35, b=35, r=0),
#                                  #legend=dict(x=0.05, y = 0.1),
#                                  legend_orientation = 'h',
#                                  font = dict(size = 12,
#                                            color = '#7f7f7f',
#                                            family = 'Courier New, monospace'))

#         top_10_fig.update_xaxes(automargin=True)

#         year_graphs.append(
#         return html.Div(dcc.Graph(
#                   id=year,
#                   figure = top_10_fig))
       
        return top_10_fig
#         return year_graphs
    
    except:
        pass
    
    
if __name__ == '__main__':
    app.run_server()
