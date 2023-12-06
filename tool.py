import requests

def other_api(query):
    headers = {
        "authority": "api.binjie.fun",
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json",
        "origin": "https://chat18.aichatos.xyz",
        "referer": "https://chat18.aichatos.xyz/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    url = "https://api.binjie.fun/api/generateStream"
    params = {
        "refer__1360": "n4%2Bx0D9DRDc7K7KD%3DKDsF4BKqr40xr4h0qWD"
    }
    data = {
        "prompt": query,
        "userId": "#/chat/1701442165034",
        "network": "true",
        "system": "",
        "withoutContext": "false",
        "stream": "false"
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    print(response.text)
    print(response)
    return response.text

# Preset 01: 学习情况分析
def run_preset_01(query):
    query = "对后面的信息进行评价和建议：" + query
    print(f"=============run_preset_02 start =============,{query}")
    content = other_api(query)
    print(f"=============run_preset_02 end =============,{content}")
    return content


def run_preset_02(query):
    query = "对后面的语段进行品鉴并提出修改建议：" + query
    print(f"=============run_preset_01 start =============,{query}")
    content = other_api(query)
    print(f"=============run_preset_01 end =============,{content}")
    return content

from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State

# Build App
external_stylesheets = ['stylesheet.css']

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H5("轻启智言小助手"),
    dcc.Dropdown(
        id='dropdown-preset',
        options=[
            {'label': '学习情况分析', 'value': '01'},
            {'label': '作文和语段的品鉴分析', 'value': '02'},
        ],
        placeholder="点击下拉以显示具体功能"
    ),
    dcc.Textarea(
        id='textarea-query',
        value='',
        placeholder="请填写关键字搜索或者下拉菜单选项来获取想要的信息",
        style={'width': '100%', 'height': 400},
    ),
    html.Div(id='textarea-query-output', style={'whiteSpace': 'pre-line', 'padding-top': '10px'}),
    html.Button('生成结果', id='button-generate', n_clicks=0),
    html.Div(id='div-output-results', style={'padding-top': '10px'}),
    html.Pre(
        id='div-output-results2',
        style={
            'height': 200,
            'overflow': 'auto',
            'font-family': 'courier new',
            'font-weight': 'bold',
            'color': 'white',
            'background-color': 'LightSlateGrey',
            'padding': '10px',
            'font-size': '100%',
            'border': 'solid 1px #A2B1C6'
        }

    ),

], style={
    'border': 'solid 1px #A2B1C6',
    'border-radius': '5px',
    'padding': '20px',
    'margin-top': '10px'
})


##
## Called when Preset dropdown is selected
##
@app.callback(
    Output(component_id='textarea-query', component_property='value'),
    Input(component_id='dropdown-preset', component_property='value'),
)
def update_output(dropdown):
    ##return 'You have selected query "{}"'.format(get_query_from_preset(dropdown))
    return get_query_from_preset(dropdown)


def get_query_from_preset(preset):
    query = ''
    if preset == '01':
        query = '请输入以下个人信息:\n1.课程名（具体内容）\n2.作业完成情况（优良中差选择）\n3.学习进度值（百分比估计填写）\n4.平时测验的平均成绩（求出极差）\n5.自我学习状态的打分（给出1-10分）\n6.期中成绩/期末成绩（）\n 按照要求填写以上内容，小助手会给出对应的评价和建议'
    elif preset == '02':
        query = '请输入一段作文或语段：（小助手会给出对其的品鉴和修改建议）\n'
    return query


##
## Called when the Button 'Generate' is pushed
##
@app.callback(
    Output(component_id='div-output-results2', component_property='children'),
    State(component_id='textarea-query', component_property='value'),
    State(component_id='dropdown-preset', component_property='value'),
    Input('button-generate', 'n_clicks')
)
def update_output2(textarea, preset, n_clicks):
    if n_clicks is None or n_clicks == 0:
        return '(没有任何信息生成)'
    else:
        ## Execute dynamically the 'run_preset_nn' function (where 'nn' is the preset number)
        results = globals()['run_preset_%s' % preset](textarea)
        return results


# Run app and display result inline in the notebook
app.run_server(debug=False)