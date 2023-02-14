import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

app = dash.Dash()

df = pd.DataFrame({
    'medal': ['Gold', 'Silver', 'Bronze', 'Gold', 'Silver', 'Bronze'],
    'count': [32, 28, 24, 20, 16, 12],
    'nation': ['USA', 'USA', 'USA', 'China', 'China', 'China']
})

app.layout = html.Div([
    dcc.Graph(
        id='medal-graph',
        figure={
            'data': [
                {'x': df['medal'], 'y': df['count'], 'type': 'bar',
                    'name': nation, 'text': df['count'], 'textposition':'auto'}
                for nation in df['nation'].unique()
            ],
            'layout': {
                'title': 'Medal Counts by Nation'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
