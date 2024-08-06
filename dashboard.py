import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from etl import load_data, load_data2, load_data3, load_data4, load_data5, load_data6
from dash.dependencies import Input, Output

# Загрузка данных
df = load_data()
df2 = load_data2()
df3 = load_data3()
df4 = load_data4()
df5 = load_data5()
df6 = load_data6()


# Определение макета дашборда

block_1=html.Div(
    children=[
        html.H1(
            f'Dashboard for sales', 
            style={'font-size':60, 'text-align':'center'}
        )
    ]
)
dd1 = dcc.Dropdown(
        id='customer-dropdown',
        options=[{'label': i, 'value': i} for i in df['customer'].unique()],
        value=df['customer'].unique()[0],
        style={'margin-top':'20px', 'width':'45%', 'display':'inline-block',}
    )
dpr1 =  dcc.DatePickerRange(
        id='date-picker-range',
        start_date=df['date'].min().date(),
        end_date=df['date'].max().date(),
        display_format='YYYY-MM-DD',
          style={'margin-top':'20px', 'width':'45%', 'display':'inline-block',}
    )

block_2=html.Div(
    children=[
        dcc.Graph(id='sales-line-chart')
    ],
    style={
        'width':'45%', 
        'display':'inline-block', 
        'padding':'10px auto',
        'margin':'5px'
    }
)
dd2 = dcc.Dropdown(
            id='year-dropdown',
            options=[{'label': i, 'value': i} for i in df2['year'].unique()],
            value=df2['year'].max(),
            style={'margin-top':'20px', 'width':'45%', 'display':'inline-block',}
)

dd3 =  dcc.Dropdown(
            id='platform-dropdown',
            options=[{'label': i, 'value': i} for i in df2['platform'].unique()],
            value=df2['platform'].unique()[0],
              style={'margin-top':'20px', 'width':'45%', 'display':'inline-block',}
        )


block_3=html.Div(
    children=[
        dcc.Graph(id='revenue-bar-chart')
    ],
    style={
        'width':'45%', 
        'display':'inline-block', 
        'padding':'10px auto',
        'margin':'5px'
    }
)


dd4 =  dcc.Dropdown(
        id='market-dropdown',
        options=[{'label': i, 'value': i} for i in df3['market'].unique()],
        value=df3['market'].unique()[0],
         style={'margin-top':'20px', 'width':'45%', 'display':'inline-block',}
    )

block_4=html.Div(
    children=[
        dcc.Graph(id='segment-pie-chart')
    ],
    style={
        'width':'45%', 
        'display':'inline-block', 
        'padding':'10px auto',
        'margin':'5px'
    }
)

dd5 = dcc.Dropdown(
        id='year-dropdown2',
        options=[{'label': str(year), 'value': year} for year in range(2017, 2024)],
        value=2017,
   style={'margin-top':'20px', 'width':'45%', 'display':'inline-block',}
    )

block_5=html.Div(
    children=[
        dcc.Graph(id='sales-count-heatmap')
    ],
    style={
        'width':'45%', 
        'display':'inline-block', 
        'padding':'10px auto',
        'margin':'5px'
    }
)
dd6 = dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': product, 'value': product} for product in df5['product'].unique()],
        value=df5['product'].unique()[0],
         style={'margin-top':'20px', 'width':'45%', 'display':'inline-block',}
    )

block_6 = html.Div(
    children=[
        dcc.Graph(id='moving-average-line-chart')
    ],
    style={
        'width':'45%', 
        'display':'inline-block', 
        'padding':'10px auto',
        'margin':'5px'
    }
)

dd7 = dcc.RadioItems(
            id='category-radio',
            options=[{'label': cat, 'value': cat} for cat in df6['product'].unique()],
            value=df6['product'].unique()[0],
             style={'margin-top':'20px', 'width':'45%', 'display':'inline-block',}
        )

block_7 = html.Div(
    children=[
        dcc.Graph(id='histogram')
    ],
    style={
        'width':'45%', 
        'display':'inline-block', 
        'padding':'10px auto',
        'margin':'5px'
    }
)

app=dash.Dash()
app.layout=html.Div(
    children=[
        block_1,
        dd1,
        dd2,
        dpr1,
        dd3,
        block_2,
        block_3,
        dd4,
        dd5,
        block_4,
        block_5,
        dd6,
        dd7,
        block_6,
        block_7
    ]
)

# Коллбэк для обновления графика
@app.callback(
    Output('sales-line-chart', 'figure'),
    [Input('customer-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_graph(selected_customer, start_date, end_date):
    # Фильтрация данных
    filtered_df = df[(df['customer'] == selected_customer) & 
                     (df['date'] >= pd.to_datetime(start_date)) & 
                     (df['date'] <= pd.to_datetime(end_date))]
    
    # Группировка данных по месяцам и вычисление суммарных продаж
    monthly_sales = filtered_df.groupby('month').agg({'total_sold_quantity': 'sum'}).reset_index()
    
    # Создание линейного графика
    line_fig = px.line(monthly_sales, x='month', y='total_sold_quantity', title='Monthly Sales Trend')
    
    return line_fig


@app.callback(
    Output('revenue-bar-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('platform-dropdown', 'value')]
)
def update_bar_chart(selected_year, selected_platform):
    filtered_df = df2[(df2['year'] == selected_year) & 
                     (df2['platform'] == selected_platform)]
    
    # Создание бар-чарта
    bar_fig = px.bar(
        filtered_df,
        x='category',
        y='total_revenue',
        title='Revenue by Product Category',
        labels={'total_revenue': 'Total Revenue', 'category': 'Product Category'}
    )
    
    return bar_fig


@app.callback(
    Output('segment-pie-chart', 'figure'),
    Input('market-dropdown', 'value')
)
def update_pie_chart(selected_market):
    filtered_df = df3[df3['market'] == selected_market]
    
    # Создание пай-чарта
    fig = px.pie(
        filtered_df,
        names='channel',
        values='revenue',
        title=f'Revenue Distribution by Segment for Market: {selected_market}'
    )
    return fig


@app.callback(
    Output('sales-count-heatmap', 'figure'),
    [Input('year-dropdown2', 'value')]
)
def update_heatmap(selected_year):
    # Создание тепловой карты
    filtered_df = df4[df4['year'] == selected_year]
    heatmap_fig = px.density_heatmap(
        filtered_df,
        x='month',
        y='region',
        z='sales_count',
        title='Sales Count Heatmap by Region and Month'
    )
    
    return heatmap_fig


@app.callback(
    Output('moving-average-line-chart', 'figure'),
    [Input('product-dropdown', 'value')]
)
def update_line_chart(selected_product):
    filtered_df = df5[df5['product'] == selected_product]
    
    line_fig = px.line(
        filtered_df, 
        x='date', 
        y='three_month_sales', 
        title=f'Three Month Sales Moving Average for {selected_product}'
    )
    
    return line_fig

@app.callback(
    Output('histogram', 'figure'),
    [Input('category-radio', 'value')]
)
def update_histogram(selected_category):
    filtered_df = df6[df6['product'] == selected_category]
    
    # Создание гистограммы
    fig = px.bar(
        filtered_df,
        x='year',
        y='total_gross_price',
        title=f'Gross Price Distribution by Year for Category {selected_category}',
        labels={'total_gross_price': 'Total Gross Price'}
    )
    fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Total Gross Price',
    bargap=0.2  
)
    return fig

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=10000, debug=True)
