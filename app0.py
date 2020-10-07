from flask import Flask, request, Response, redirect, render_template
from flask_paginate import Pagination, get_page_args
import requests
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

    # get the current page number, issues per page, and current offset
    # pylint: disable=unbalanced-tuple-unpacking
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', offset="offset")
    print(page, " ", per_page, " ", offset)

    # get a the current page's list of issues
    pagination_issues = get_issues(offset=offset, per_page=per_page)
    # pylint: disable=unbalanced-tuple-unpacking
    pagination = Pagination(page=page, per_page=per_page, total=len(issues), css_framework="bootstrap4")

    return render_template("issue_browser.html", issues=pagination_issues, pagination=pagination)

@app.route('/issue_detail')
def issue_detail():
    # get issue id passed to page by the issue detail link
    issue_id = request.args.get("id", None)

    # isolate the issue by looking it up by id in the list
    issue = [issue for issue in issues if int(issue["id"]) == int(issue_id)][0]

    return render_template("issue_detail.html", issue=issue)
