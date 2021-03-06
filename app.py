import requests
import os
import math
import json
import pandas as pd

from flask import Flask, render_template

from bokeh.models import ColumnDataSource, Range1d
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.plotting import figure, column, row
from bokeh.palettes import Viridis10, Category20c
from bokeh.models import CustomJS, Select, Button, Paragraph
from bokeh.transform import jitter, cumsum

app = Flask(__name__)

# Repositories
repos = {
    "vuejs": "vue",
    "facebook": "react",
    "microsoft": "vscode",
    "apache": "logging-log4j2",
    # "torvalds": "linux", -- Github API response says contributor list is too large to be obtained by API
    "golang": "go",
    "apple": "swift",
    "atom": "atom",
    "freeCodeCamp": "freeCodeCamp"
}

token = None

# Transform value t from range [a,b] to [c,d]
def transform(t: float, a: float, b: float, c: float, d: float):
    return c + ((d - c)/(b - a))*(t - a)

def get_repo(headers, owner, repo) -> json:
    repo_data = []

    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"

    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            repo_data = r.json()
    except (requests.ConnectionError, requests.Timeout):
        pass

    return repo_data

@app.route('/')
def index():

    if token is None or "":
        return "<p>Failed to load Github API token!</p>"
    
    headers = None
    try:
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    except:
        return "<p>Invalid Github API token! (Check for special characters, white space or mistakes)</p>"

    error_text = Paragraph(text="Failed to retrieve some Github API Data! (Check your API access token and git API server status)")
    error = False

    source = ColumnDataSource()

    x_data = []
    y_data = []
    color_data = []
    login_data = []
    id_data = []
    size_data = []

    # map of 'repo_name' -> (map of 'login' -> 'total_contributions')
    pie_data = {}

    largest_contribution = 0

    i = 0
    with open("data.json", "w") as file:
        for owner in repos:
            repo_data = get_repo(headers, owner, repos[owner])
            if repo_data == []:
                error = True

            json.dump(repo_data, file, indent=4)

            repo_name = str(owner + '/' + repos[owner])
            pie_data[repo_name] = {}

            for contributor in repo_data:
                login = contributor["login"]
                id = contributor["id"]
                total_contributions = contributor["contributions"]
                x_data.append(repos[owner])
                y_data.append(total_contributions)
                color_data.append(Viridis10[i % 10])
                size_data.append(float(total_contributions))
                login_data.append(login)
                id_data.append(id)

                pie_data[repo_name][login] = total_contributions

                if largest_contribution < total_contributions:
                    largest_contribution = total_contributions
            i = i + 1

    # Scale points based on total contributions
    size_data = [transform(value, 1, largest_contribution, 5, 40) for value in size_data]

    fig = figure(x_range=[repos[owner] for owner in repos], plot_height=720, plot_width=1280, toolbar_location=None, tooltips=[("User", "@login"), ("User ID", "@id"), ("Contributions", "@commit_count")], tools="pan,wheel_zoom,reset", active_drag="pan", active_scroll="wheel_zoom")
    fig.circle(x=jitter("x", width=0.8, range=fig.x_range), y="y", source=source, size="size", color="color", fill_alpha=0.6)
    fig.xaxis.axis_label = "Repositories"
    fig.yaxis.axis_label = "Total Contributions by User"
    fig.xaxis.major_label_text_font_size = '10pt'
    fig.yaxis.major_label_text_font_size = '10pt'
    fig.xaxis.axis_label_text_font_size = '15pt'
    fig.yaxis.axis_label_text_font_size = '15pt'

    source.data = dict(
        x = x_data,
        y = y_data,
        color = color_data,
        size = size_data,
        login = login_data,
        id = id_data,
        commit_count = y_data
    )

    # Pie Chart
    # ------------

    # Data
    pie_panda_data = {}
    pie_panda_data_json = {}
    for owner in repos:
        repo_name = owner + '/' + repos[owner]
        if pie_data[repo_name] == {}:
            data = { "angle": [], "color": [], "contributions": [], "index": [], "login": []}
            pie_panda_data[repo_name] = data
            pie_panda_data_json[repo_name] = json.loads(json.dumps(data))
            continue

        top = 10 # Only display the top 10 contributors
        data = pd.Series(pie_data[repo_name]).reset_index(name='contributions').rename(columns={'index':'login'}).nlargest(top, columns='contributions')
        data['color'] = Category20c[top]
        data['angle'] = (data['contributions'] / data['contributions'].sum()) * 2 * math.pi
        pie_panda_data[repo_name] = data
        pie_panda_data_json[repo_name] = json.loads(data.to_json())
    
    default = "apple/swift"
    pie_source = ColumnDataSource()
    pie_source.data = pie_panda_data[default]

    # Chart
    p = figure(plot_height = 350, plot_width = 500, title="Pie Chart (Top 10 Contributors)", toolbar_location=None,
            tools="hover", tooltips="@login: @contributions")

    p.wedge(x=0.33, y=0.5, radius=0.25, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', source=pie_source, legend_field='login')

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    p.x_range = Range1d(0, 1)
    p.y_range = Range1d(0, 1)

    json_dump = json.dumps(pie_panda_data_json)
    json_pass = Button(label=json_dump)

    select = Select(title="", value=default, options=[str(owner + '/' + repos[owner]) for owner in repos])
    select_code = ""
    with open("select.js", "r") as file:
        select_code = file.read()
    callback = CustomJS(args={"source": pie_source, "json_pass":json_pass}, code=select_code)
    select.js_on_change("value", callback)

    column_layout = column([p, select])
    layout = row([fig, column_layout])

    if error:
        error_layout = column([error_text, layout])
        script, div = components(error_layout)
    else:
        script, div = components(layout)

    return render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')

if __name__ == "__main__":
    # Setup
    with open("gittoken.txt", "r") as file:
        token = file.read()
        token = token.strip('\n')

    # Run webapp
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))