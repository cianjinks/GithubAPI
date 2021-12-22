import requests
import os
import math
from flask import Flask, render_template
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.io import curdoc
from bokeh.resources import INLINE
from bokeh.embed import components
from bokeh.plotting import figure, output_file, show

app = Flask(__name__)

# Top 10 repositories (https://gitstar-ranking.com/)
repos = {
    "freeCodeCamp": "freeCodeCamp",
    "996icu": "996.ICU",
    "EbookFoundation": "free-programming-books",
    "jwasham": "coding-interview-university",
    "vuejs": "vue",
    "facebook": "react",
    "kamranahmedse": "developer-roadmap",
    "sindresorhus": "awesome",
    "tensorflow": "tensorflow",
    "twbs": "bootstrap"
}

token = os.getenv('GITHUB_TOKEN', '...')
headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

@app.route('/')
def index():
    source = ColumnDataSource()

    for owner in repos:
        url = f"https://api.github.com/repos/{owner}/{repos[owner]}/contributors"
        r = requests.get(url, headers=headers)
        repo_data = r.json()

    fig = figure(x_range=[repos[owner] for owner in repos], plot_height=600, plot_width=720, tooltips=[("User", "@login"), ("User ID", "@id")])
    fig.vbar(x="x", top="y", source=source, width=0.9, color="color")
    fig.xaxis.axis_label = "Contributors"
    fig.xaxis.major_label_orientation = math.pi/4
    fig.yaxis.axis_label = "Top Repositories"

    source.data = dict(
        x = [repos[owner] for owner in repos],
        y = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
        color = ["#FF9900", "#FF9900", "#FF9900", "#FF9900", "#FF9900", "#FF9900", "#FF9900", "#FF9900", "#FF9900", "#FF9900"],
        login = ["test", "test", "test", "test", "test", "test", "test", "test", "test", "test"],
        id = ["test", "test", "test", "test", "test", "test", "test", "test", "test", "test"]
    )

    script, div = components(fig)
    return render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        js_resources=INLINE.render_js(),
        css_resources=INLINE.render_css(),
    ).encode(encoding='UTF-8')

if __name__ == "__main__":
    app.run(debug=True)