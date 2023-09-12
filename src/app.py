from dash import html, dcc, Dash
from flask import Flask
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import dash_daq as daq
import geopandas as gpd
from collections import OrderedDict
import pandas as pd

tags = [
    {
        'charset': 'utf-8',
    },
    {
        'name': 'viewport',
        'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
    }
]

styles = ['styles.css', dbc.themes.SUPERHERO, dbc.icons.BOOTSTRAP]
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
purchases_year = [2018, 2019, 2020, 2021, 2022, 2023, 2018, 2019, 2020, 2021, 2022, 2023]
purchases = [450000, 490000, 450000, 650000, 680000, 850000, 590000, 740000, 790000, 850000, 880000, 870000]
comments_type = ["Very Unsatisfied","Not Satisfied","Neutral","Satisfied","Very Satisfied"]
comments_values = [3500000, 4500000, 6000000, 7500000, 8000000]
comments_colors = ['#D71D09','#F39C12','#F1C40F','#2ECC71','#145A32']
purchases_type = ['Online', 'Online', 'Online', 'Online', 'Online', 'Online', 
                'In-Store', 'In-Store', 'In-Store', 'In-Store', 'In-Store', 'In-Store']
data_purchases = OrderedDict(
        [
            ('Year', purchases_year),
            ('purchases', purchases),
            ('type', purchases_type),
        ]
    )
df_purchases = pd.DataFrame(data_purchases)
labels_products = ['Product 1 (5780)','Product 2 (4500)','Product 3 (3853)','Product 4 (3460)', 'Product 5 (2789)']
data_campaign = OrderedDict(
    [
        ('Campaigns', ['Adwords', 'Emails','Banners Ads','Social Ads']),
        ('Values', [13703000, 17605000, 16000000, 12503000]),
    ]
)
df_campaigns = pd.DataFrame(data_campaign)
data_cost = OrderedDict(
    [
        ('Categories', [
            'Purchase', 'Purchase','Purchase','Purchase', 'Purchase', 'Purchase', 
            'Labour', 'Labour','Labour','Labour', 'Labour', 'Labour', 
            'Lease', 'Lease', 'Lease', 'Lease', 'Lease', 'Lease'
        ]),
        ('Month', [
            'July', 'August', 'September', 'October', 'November', 'December',
            'July', 'August', 'September', 'October', 'November', 'December',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]),
        ('Porcents', [
            25, 45, 38, 44, 20, 35,
            60, 25, 32, 16, 40, 35,
            15, 30, 30, 40, 40, 30
        ]),
    ]
)
df_cost = pd.DataFrame(data_cost)

values_products = [5780, 4500, 3853, 3460, 2789]
geo_df = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
px.set_mapbox_access_token("pk.eyJ1IjoiaGVpbmVyZW5pcyIsImEiOiJjbGFiOHB0dnYwZWEzM29vMzg1YjY5YW95In0.DDoI2wcz7Miya1mQ-x6UoQ")
df_visitors= px.data.gapminder()

scatter_visitors = px.scatter(
    df_visitors, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
    size="pop", color="continent", hover_name="country", facet_col="continent",
    log_x=True, size_max=45, range_x=[100,100000], range_y=[25,90],
    hover_data={'gdpPercap':True, 'lifeExp':True, 'year':True, 'country':True, 'continent':True, 'pop':False},
    labels={'gdpPercap':'Callers', 'lifeExp':'Comments', 'year':'Year'}, height=700
)
scatter_visitors.update_layout(
    margin={"r":0,"t":35,"l":0,"b":0},
    legend=dict(
        x=1,
        y=0.97,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    font = dict(
        size = 15
    ),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    barmode='stack',
    hovermode='x unified',
    bargap=0.15, 
    bargroupgap=0.1 
)

map_sales = px.scatter_mapbox(geo_df, lat=geo_df.geometry.y,lon=geo_df.geometry.x, hover_name="name", zoom=1)
map_sales.update_layout(
    margin ={'l':0,'t':0,'b':0,'r':0},
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)'
)

sales_indicator =  daq.Gauge(
    id="sales_indicator",
    color={"gradient":True,"ranges":{"green":[0,60],"yellow":[60,80],"red":[80,100]}},
    scale={'start': 0, 'interval': 5, 'labelInterval': 2},
    value=83,
    units="%",
    max=100,
    min=0,
    showCurrentValue=True,
    size=250,
    style = {'fontSize':15}
)

area_purchases = px.area(df_purchases, x="Year", y='purchases', color="type", labels={'type':' '})
area_purchases.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(
        x=0,
        y=0.97,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    font = dict(
        size = 15
    ),
    yaxis=dict(
        title='USD',
        tickfont_size=14,
    ),
    xaxis=dict(
        title='year',
        titlefont_size=16,
    ),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)'
)

pie_products = go.Figure(data=[go.Pie(labels=labels_products, values=values_products, hole=.3)])
pie_products.update_traces(textposition='inside', textinfo='percent+label')
pie_products.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(
        x=0,
        y=0.97,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    font = dict(
        size = 15
    ),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)'
)

pie_comments = go.Figure(data=[go.Pie(labels=comments_type, values=comments_values, hole=.5)])
pie_comments.update_traces(textposition='inside', textinfo='percent+label')
pie_comments.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(
        x=0,
        y=0.97,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    font = dict(
        size = 15
    ),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)'
)
pie_comments.update(layout_showlegend=False)

bar_campaigns = px.bar(df_campaigns, x='Values', y='Campaigns', color='Campaigns', orientation='h', labels={'Values':' '})
bar_campaigns.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(
        x=1,
        y=0.97,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    font = dict(
        size = 15
    ),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    barmode='stack',
    bargap=0.15, 
    bargroupgap=0.1 
)

bar_cost = px.bar(df_cost, x='Month', y='Porcents', color='Categories', labels={'Porcents':'Procent %'})
bar_cost.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    legend=dict(
        x=1,
        y=0.97,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    font = dict(
        size = 15
    ),
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    barmode='stack',
    hovermode='x unified',
    bargap=0.15, 
    bargroupgap=0.1 
)

analysis = go.Figure()
analysis.add_trace(
    go.Bar(
        x=years,
        y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263, 350, 430, 474, 526, 488, 537, 500, 439],
        name='Rest of world',
        marker_color='rgb(55, 83, 109)'
    )
)
analysis.add_trace(
    go.Bar(
        x=years,
        y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,299, 340, 403, 549, 499],
        name='China',
        marker_color='rgb(26, 118, 255)'
    )
)
analysis.update_layout(
    margin={"r":5,"t":0,"l":5,"b":0},
    xaxis_tickfont_size=14,
    yaxis=dict(
        title='USD (millions)',
        titlefont_size=16,
        tickfont_size=14,
    ),
    legend=dict(
        x=0,
        y=0.97,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1, # gap between bars of the same location coordinate.
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)'
)

buys = go.Figure()
sells = go.Figure()
buys.add_trace(
    go.Indicator(
        mode = "number+delta",
        value = 492,
        number = {"prefix": "$", "suffix": "m"},
        delta = {"reference": 512, "valueformat": ".0f", "prefix": "$", "suffix": "m"},
        title = {"text": "Buys"},
        domain = {'y': [0, 1], 'x': [0.25, 0.75]}
    )
)
sells.add_trace(
    go.Indicator(
        mode = "number+delta",
        value = 785,
        number = {"prefix": "$", "suffix": "m"},
        delta = {"reference": 512, "valueformat": ".0f", "prefix": "$", "suffix": "m"},
        title = {"text": "Sells"},
        domain = {'y': [0, 1], 'x': [0.25, 0.75]}
    )
)
sells.add_trace(
    go.Scatter(
        y = [
            325, 374, 415, 430, 445, 420, 422, 432, 419, 394, 410, 426, 428, 433, 444, 
            456, 436, 418, 429, 412, 429, 442, 464, 447, 434, 457, 474, 480, 499, 497, 
            508, 521, 557, 568, 561, 556, 559, 575, 597, 594, 518, 537, 550, 530, 642, 
            624, 643, 620, 618, 623, 623, 626, 640, 637, 636, 647, 660, 678, 672, 650, 
            680, 702, 742, 785
        ],
        line = dict(color = "#27AE60", width=7),
        name = 'Sell'
    )
)
buys.add_trace(
    go.Scatter(
        y = [
            325, 324, 405, 400, 424, 404, 417, 432, 419, 394, 410, 426, 413, 419, 404, 
            408, 401, 377, 368, 361, 356, 359, 375, 397, 394, 418, 437, 450, 430, 442, 
            424, 443, 420, 418, 423, 423, 426, 440, 437, 436, 447, 460, 478, 472, 450, 
            456, 436, 418, 429, 412, 429, 442, 464, 447, 434, 457, 474, 480, 499, 497, 
            480, 502, 512, 492
        ],
        line = dict(color = "#E74C3C", width=7),
        name = 'Buy'
    )
)
buys.update_layout(
    xaxis = {'range': [0, 62]},
    margin={"r":0,"t":0,"l":0,"b":0},
    autosize=True,
    showlegend=False,
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    font = dict(
        size = 15
    )
)
sells.update_layout(
    xaxis = {'range': [0, 62]},
    margin={"r":0,"t":0,"l":0,"b":0},
    autosize=True,
    showlegend=False,
    paper_bgcolor='rgba(0, 0, 0, 0)',
    plot_bgcolor='rgba(0, 0, 0, 0)',
    font = dict(
        size = 15
    )
)

navbar =  dbc.Nav(
    className = "navbar",
    children = [
        html.Div(
            children = [
                html.A(
                    children = [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("PowerBy Dash", className="title_brand")),
                    ],
                    className = "Brand",
                    href="https://plotly.com",
                    style={"textDecoration": "none"},
                )
            ],
            className = "brand_position"
        ),
        dbc.NavItem(dbc.NavLink("Main", active=True, href="/", className='item_activate')),
        dbc.NavItem(dbc.NavLink("About", href="#", className='item')),
        dbc.NavItem(dbc.NavLink("Contact", href="#", className='item')),
        dbc.Button(
            [
                "Notifications",
                dbc.Badge("4", color="#4C9BE8", text_color="dark", className="ms-1 notify"),
            ],
            color="secondary",
            className="notify"
        ),
        html.Div(
            className = 'search_div',
            children = [
                dbc.Input(type="search", placeholder="Search", className='search'),
                dbc.Button(
                    [html.I(className="bi bi-search icon_search"), "Search"],
                    color="secondary", className="ms-2 btn_search", n_clicks=0
                )
            ]
        )
        
    ]
)

card_content_one = [
    dbc.CardHeader([html.I(className="bi bi-patch-check icon_search"), "Success"], className = "card_title"),
    dbc.CardBody(
        [
            html.Div(
                children = [
                    html.H5("Card title", className="card-title"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa natus eveniet provident at expedita? Molestiae vero temporibus recusandae ipsam sed?",
                        className="card-text",
                    )
                ],
                className = "div_principal"
            ),
            html.Div(
                html.H5([html.I(className="bi bi-graph-up-arrow icon_search"), "75%"], className="porcent"),
                className = "div_segundario"
            )
        ],
        className = "card_body"
    ),
]

card_content_two = [
    dbc.CardHeader([html.I(className="bi bi-exclamation-diamond icon_search"), "Warning"], className = "card_title"),
    dbc.CardBody(
        [
            html.Div(
                children = [
                    html.H5("Card title", className="card-title"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa natus eveniet provident at expedita? Molestiae vero temporibus recusandae ipsam sed?",
                        className="card-text",
                    )
                ],
                className = "div_principal"
            ),
            html.Div(
                html.H5([html.I(className="bi bi-activity icon_search"), "15%"], className="porcent"),
                className = "div_segundario"
            )
        ],
        className = "card_body"
    ),
]

card_content_three = [
    dbc.CardHeader([html.I(className="bi bi-x-octagon icon_search"), "Danger"], className = "card_title"),
    dbc.CardBody(
        [
            html.Div(
                children = [
                    html.H5("Card title", className="card-title"),
                    html.P(
                        "Lorem ipsum dolor sit amet, consectetur adipisicing elit. Culpa natus eveniet provident at expedita? Molestiae vero temporibus recusandae ipsam sed?",
                        className="card-text",
                    )
                ],
                className = "div_principal"
            ),
            html.Div(
                html.H5([html.I(className="bi bi-graph-down-arrow icon_search"), "10%"], className="porcent"),
                className = "div_segundario"
            )
        ],
        className = "card_body"
    ),
]

row = [
        dbc.Card(
            children = [
                navbar
            ], 
            body=True, 
            className = "card_nav",
            color="#4C9BE8"
        ),
        dbc.Row(
            children = [
                dbc.Card(
                    dbc.CardBody(
                        children = [
                            dbc.Row(
                                children = [
                                    dbc.Col(dbc.Card(card_content_one, color="success", inverse=True, className = 'col_card')),
                                    dbc.Col(dbc.Card(card_content_two, color="warning", inverse=True, className = 'col_card')),
                                    dbc.Col(dbc.Card(card_content_three, color="danger", inverse=True, className = 'col_card')),
                                ],
                            )
                        ]
                    ),
                    className="content_row_one",
                    color="secondary"
                ),
            ],
            className = "Row_One"
        ),
        dbc.Row(
            children = [
                dbc.Card(
                    children = [
                        dbc.CardHeader(
                            html.H3(
                                children=[
                                    html.I(className="bi bi-display icon_first_title"), "Monitoring and Analytics"
                                ], 
                                className="first_title"
                            )
                        ),
                        dbc.CardBody(
                            children = [
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            width = 12,
                                            xxl = 8,
                                            children = [
                                                dbc.Card(
                                                    children = [
                                                        dbc.CardHeader(
                                                            ['Sales Analysis in International Markets'],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            dcc.Graph(
                                                                id = 'analysis',
                                                                figure=analysis,
                                                                config={
                                                                    'displayModeBar':False,
                                                                    'responsive':True,
                                                                    'queueLength':0
                                                                }
                                                            )
                                                        )
                                                    ], 
                                                    color="white", 
                                                    inverse=True, 
                                                    className = 'card_2col'
                                                )
                                            ]
                                        ),
                                        dbc.Col(
                                            width = 12,
                                            xxl = 4,
                                            children = [
                                                dbc.Row(
                                                    children = [
                                                        dbc.Col(
                                                            dbc.Card(
                                                                children = [
                                                                    dbc.CardBody(
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id = 'sells',
                                                                                figure=sells,
                                                                                config={
                                                                                    'displayModeBar':False,
                                                                                    'responsive':True,
                                                                                    'queueLength':0
                                                                                }
                                                                            )
                                                                        ]
                                                                    )
                                                                ],
                                                                color="white",
                                                                inverse=True, 
                                                                className = 'col_block'
                                                            )
                                                        ),
                                                        dbc.Col(
                                                            dbc.Card(
                                                                children = [
                                                                    dbc.CardBody(
                                                                        children=[
                                                                            dcc.Graph(
                                                                                id = 'buys',
                                                                                figure=buys,
                                                                                config={
                                                                                    'displayModeBar':False,
                                                                                    'responsive':True,
                                                                                    'queueLength':0
                                                                                }
                                                                            )
                                                                        ]
                                                                    )
                                                                ],
                                                                color="white",
                                                                inverse=True, 
                                                                className = 'col_block col_down'
                                                            )
                                                        ),
                                                    ],
                                                    className = 'row_block'
                                                )
                                            ]
                                        )
                                    ],
                                ),
                                dbc.Row(
                                    children = [
                                        dbc.Col(
                                            width=12,
                                            xxl=8,
                                            children = [
                                                dbc.Card(
                                                    children = [
                                                        dbc.CardHeader(
                                                            ['Current Global Visitors'],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children=[
                                                                dcc.Graph(
                                                                    id = 'sales_map',
                                                                    figure=map_sales,
                                                                    config={
                                                                        'displayModeBar':False,
                                                                        'responsive':True,
                                                                        'queueLength':0
                                                                    }
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    color = "white",
                                                    className="col_info"
                                                )
                                            ],
                                        ),
                                        dbc.Col(
                                            width=12,
                                            xxl=4,
                                            children = [
                                                dbc.Card(
                                                    children = [
                                                        dbc.CardHeader(
                                                            children=["Real Demand in Percentage (%)"],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children=[
                                                                sales_indicator
                                                            ],
                                                            className='sales_indicator'
                                                        )  
                                                    ],
                                                    color = "white",
                                                    className="col_info left_map"
                                                )
                                            ],
                                        )
                                    ],
                                    className="card_3col"
                                )
                            ],
                        ),
                    ],
                    color = "secondary"
                )
            ],
            className = "Row_Two"
        ),
        dbc.Row(
            children = [
                dbc.Card(
                    children=[
                        dbc.CardHeader(
                            html.H3(
                                children=[
                                    html.I(className="bi bi-clipboard-pulse icon_first_title"), "Sales Product Performance"
                                ], 
                                className="first_title"
                            )
                        ),
                        dbc.CardBody(
                            children = [
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            width=12,
                                            xxl=6,
                                            children=[
                                                dbc.Card(
                                                    children = [
                                                        dbc.CardHeader(
                                                            ['Tops Products in Revenue (K)'],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children= [
                                                                dcc.Graph(
                                                                    id = 'pie_chart',
                                                                    figure=pie_products,
                                                                    config={
                                                                        'displayModeBar':False,
                                                                        'responsive':True,
                                                                        'queueLength':0
                                                                    }
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    color = 'white',
                                                    className = "cards_x4"
                                                )
                                            ]
                                        ),
                                        dbc.Col(
                                            width=12,
                                            xxl=6,
                                            children=[
                                                dbc.Card(
                                                    children = [
                                                        dbc.CardHeader(
                                                            ['Online vs In-Store Purchases (2018-2022)'],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children= [
                                                                dcc.Graph(
                                                                    id = 'area_chart',
                                                                    figure=area_purchases,
                                                                    config={
                                                                        'displayModeBar':False,
                                                                        'responsive':True,
                                                                        'queueLength':0
                                                                    }
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    color = 'white',
                                                    className = "cards_x4"
                                                )
                                            ]
                                        )
                                    ],
                                    className = "row_x4"
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            width=12,
                                            xxl=6,
                                            children=[
                                                dbc.Card(
                                                    children = [
                                                        dbc.CardHeader(
                                                            ['Incremental Sales by Campaign'],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children= [
                                                                dcc.Graph(
                                                                    id = 'bar_chart',
                                                                    figure=bar_campaigns,
                                                                    config={
                                                                        'displayModeBar':False,
                                                                        'responsive':True,
                                                                        'queueLength':0
                                                                    }
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    color = 'white',
                                                    className = "cards_x4"
                                                )
                                            ]
                                        ),
                                        dbc.Col(
                                            width=12,
                                            xxl=6,
                                            children=[
                                                dbc.Card(
                                                    children = [
                                                        dbc.CardHeader(
                                                            ['Cost of Goods Sold'],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children= [
                                                                dcc.Graph(
                                                                    id = 'bar_vertical_chart',
                                                                    figure=bar_cost,
                                                                    config={
                                                                        'displayModeBar':False,
                                                                        'responsive':True,
                                                                        'queueLength':0
                                                                    }
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    color = 'white',
                                                    className = "cards_x4"
                                                )
                                            ]
                                        )
                                    ],
                                    className = "row_x4"
                                )
                            ]
                        )
                    ],
                    color = "secondary"
                )
            ],
            className = "Row_Three"
        ),
        dbc.Row(
            children = [
                dbc.Card(
                    children=[
                        dbc.CardHeader(
                            html.H3(
                                children=[
                                    html.I(className="bi bi-life-preserver icon_first_title"), "Call Center Globally"
                                ], 
                                className="first_title"
                            )
                        ),
                        dbc.CardBody(
                            children=[
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            width=12,
                                            xxl=3,
                                            children=[
                                                dbc.Card(
                                                    children=[
                                                        dbc.CardHeader(
                                                            children=["Speed of Answer"],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children=[
                                                                html.H3(
                                                                    children=[
                                                                        "0m:26s"
                                                                    ],
                                                                    className="principal_content_call_info"
                                                                ),
                                                                html.P(
                                                                    children=[
                                                                        html.I(className="bi bi-arrow-down"), "  0m:10s"
                                                                    ],
                                                                    className="secondary_content_call_ingo"
                                                                ),
                                                                html.Span(
                                                                    children=["vs previous 30 days"],
                                                                    className="span_content_call_info"
                                                                )
                                                            ],
                                                            className="content_call_info"
                                                        )
                                                    ],
                                                    color = 'white',
                                                    className = "cards_x4 info_call"
                                                )
                                            ]
                                        ),
                                        dbc.Col(
                                            width=12,
                                            xxl=3,
                                            children=[
                                                dbc.Card(
                                                    children=[
                                                        dbc.CardHeader(
                                                            children=["Replied to on Time"],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children=[
                                                                html.H3(
                                                                    children=[
                                                                        "98.2%"
                                                                    ],
                                                                    className="principal_content_call_info"
                                                                ),
                                                                html.P(
                                                                    children=[
                                                                        html.I(className="bi bi-arrow-up"), "  1.2%"
                                                                    ],
                                                                    className="secondary_content_call_ingo"
                                                                ),
                                                                html.Span(
                                                                    children=["vs previous 30 days"],
                                                                    className="span_content_call_info"
                                                                )
                                                            ],
                                                            className="content_call_info"
                                                        )
                                                    ],
                                                    color = 'white',
                                                    className = "cards_x4 info_call"
                                                )
                                            ]
                                        ),
                                        dbc.Col(
                                            width=12,
                                            xxl=3,
                                            children=[
                                                dbc.Card(
                                                    children=[
                                                        dbc.CardHeader(
                                                            children=["Average Call Time"],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children=[
                                                                html.H3(
                                                                    children=[
                                                                        "4m:36s"
                                                                    ],
                                                                    className="principal_content_call_info"
                                                                ),
                                                                html.P(
                                                                    children=[
                                                                        html.I(className="bi bi-arrow-down"), "  0m:14s"
                                                                    ],
                                                                    className="secondary_content_call_ingo"
                                                                ),
                                                                html.Span(
                                                                    children=["vs previous 30 days"],
                                                                    className="span_content_call_info"
                                                                )
                                                            ],
                                                            className="content_call_info"
                                                        )
                                                    ],
                                                    color = 'white',
                                                    className = "cards_x4 info_call"
                                                )
                                            ]
                                        ),
                                        dbc.Col(
                                            width=12,
                                            xxl=3,
                                            children=[
                                                dbc.Card(
                                                    children=[
                                                        dbc.CardHeader(
                                                            children=["CSR Occupancy"],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children=[
                                                                html.H3(
                                                                    children=[
                                                                        "81.6%"
                                                                    ],
                                                                    className="principal_content_call_info"
                                                                ),
                                                                html.P(
                                                                    children=[
                                                                        html.I(className="bi bi-arrow-up"), "  3.2%"
                                                                    ],
                                                                    className="secondary_content_call_ingo"
                                                                ),
                                                                html.Span(
                                                                    children=["vs previous 30 days"],
                                                                    className="span_content_call_info"
                                                                )
                                                            ],
                                                            className="content_call_info"
                                                        )
                                                    ],
                                                    color = 'white',
                                                    className = "cards_x4 info_call"
                                                )
                                            ]
                                        )
                                    ],
                                    className="row_x4"
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            width=12,
                                            xxl=3,
                                            children=[
                                                dbc.Card(
                                                    children=[
                                                        dbc.CardHeader(
                                                            children=["Customer Satisfaction"],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children=[
                                                                dcc.Graph(
                                                                    id='Pie-customer',
                                                                    figure=pie_comments,
                                                                    config={
                                                                        'displayModeBar':False,
                                                                        'responsive':True,
                                                                        'queueLength':0
                                                                    }
                                                                )
                                                            ]
                                                        )
                                                    ],
                                                    color = 'white',
                                                    className = "cards_x4"
                                                )
                                            ]
                                        ),
                                        dbc.Col(
                                            width=12,
                                            xxl=9,
                                            children=[
                                                dbc.Card(
                                                    children=[
                                                        dbc.CardHeader(
                                                            children=["Growth and Public Advice Provided Globally"],
                                                            className="title_card"
                                                        ),
                                                        dbc.CardBody(
                                                            children=[
                                                                dcc.Graph(
                                                                    id='Scatter_plot',
                                                                    figure=scatter_visitors,
                                                                    config={
                                                                        'displayModeBar':False,
                                                                        'responsive':True,
                                                                        'queueLength':0
                                                                    }
                                                                )
                                                            ],
                                                            className="scatter_plot"
                                                        )
                                                    ],
                                                    color = 'white',
                                                    className = "cards_x4"
                                                )
                                            ]
                                        )
                                    ],
                                    className="row_x4"
                                )
                            ]
                        )
                    ],
                    color="secondary"
                )
            ],
            className="Row_four"
        ),
        dbc.Row(
            children=[
                dbc.Card(
                    children=[
                        dbc.CardBody(
                            dbc.Row(
                                children=[
                                    dbc.Col(
                                        width=12,
                                        xxl=12,
                                        children=[
                                            html.H2(
                                                children=[
                                                    "Gabriel Piñero"
                                                ],
                                                className="title_footer"
                                            ),
                                            html.H4(
                                                children=[
                                                    "Python Developer"
                                                ],
                                                className="headline_footer"
                                            )
                                        ],
                                        className="footer_col_one"
                                    ),
                                    dbc.Col(
                                        width=12,
                                        xxl=12,
                                        children=[
                                            html.A(
                                                children=[
                                                    html.I(className="bi bi-github icon_website")
                                                ],
                                                href="https://github.com/GabrielPy28",
                                                draggable="https://github.com/GabrielPy28",
                                                className="footer_links"
                                            ),
                                            html.A(
                                                children=[
                                                    html.I(className="bi bi-linkedin icon_website")
                                                ],
                                                href="https://www.linkedin.com/in/gabriel-pi%C3%B1ero-a151321a9/",
                                                draggable="https://www.linkedin.com/in/gabriel-pi%C3%B1ero-a151321a9/",
                                                className="footer_links"
                                            ),
                                            html.A(
                                                children=[
                                                    html.I(className="bi bi-person-workspace icon_website")
                                                ],
                                                href="https://portfolio-web-python.netlify.app",
                                                draggable="https://portfolio-web-python.netlify.app",
                                                className="footer_links"
                                            ),
                                            html.A(
                                                children=[
                                                    html.I(className="bi bi-envelope-at-fill icon_website")
                                                ],
                                                href="mailto:gabrielparenas27@gmail.com",
                                                draggable="mailto:gabrielparenas27@gmail.com",
                                                className="footer_links"
                                            ),
                                            html.A(
                                                children=[
                                                    html.I(className="bi bi-whatsapp icon_website")
                                                ],
                                                href="https://api.whatsapp.com/send?phone=584127823455",
                                                draggable="https://api.whatsapp.com/send?phone=584127823455",
                                                className="footer_links"
                                            )
                                        ],
                                        className="footer_col_two"
                                    ),
                                    dbc.Col(
                                        width=12,
                                        xxl=12,
                                        children=[
                                            html.Span(
                                                children=[
                                                    html.I(className="bi bi-c-circle icon_compy_right"), 
                                                    "  Gabriel Piñero | All rights Reserved."
                                                ],
                                                className='copy_right'
                                            )
                                        ],
                                        className="footer_col_three"
                                    )
                                ],
                                className="footer_content"
                            )
                        )
                    ],
                    color="#4C9BE8"
                )
            ],
            className="Row_footer"
        )
    ]

app = Dash(
    __name__, title='Dashboard', server = Flask(__name__),
    update_title='Loading...', suppress_callback_exceptions=True, 
    prevent_initial_callbacks=True, external_stylesheets = styles,
    meta_tags = tags
)

server = app.server

app._favicon = "icon.ico"

app.layout = html.Div(
    row
)

if __name__ == '__main__':
    app.run(debug=False)