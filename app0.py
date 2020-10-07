from flask import Flask, request, Response, redirect, render_template
import os
import requests
from flask_paginate import Pagination, get_page_parameter, get_page_args
import issues

app = Flask(__name__)

# auto-reload templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

# get issue data and format as json / dict
# issues_data = requests.get("https://api.github.com/repos/walmartlabs/thorax/issues")
# issues = issues_data.json()
issues = issues.issues

def get_issues(offset=0, per_page=10):
    return issues[offset: offset + per_page]

@app.route('/', methods=['POST', 'GET'])
def main_page():
    # r = requests.get("https://api.github.com/repos/walmartlabs/thorax/issues")
    # issues = r.json()
    print(issues)
    # titles = [issue["title"] for issue in issues]
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page=10, total=len(issues), record_name="issues", css_framework="bootstrap4")

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(issues)

    pagination_issues = get_issues(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework="bootstrap4")

    return render_template("issue_browser.html", issues=pagination_issues, pagination=pagination)

@app.route('/issue_detail')
def issue_detail():
    issue_id = request.args.get("id", None)
    print(issue_id)
    print([int(issue_id) == int(issue["id"]) for issue in issues])
    issue = [issue for issue in issues if int(issue["id"]) == int(issue_id)][0]
    return render_template("issue_detail.html", issue=issue)
