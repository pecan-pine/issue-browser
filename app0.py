from flask import Flask, request, Response, redirect, render_template
import os
import requests
from flask_paginate import Pagination, get_page_parameter, get_page_args

app = Flask(__name__)

# auto-reload templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

r = requests.get("https://api.github.com/repos/walmartlabs/thorax/issues")
issues = r.json()
def get_issues(offset=0, per_page=10):
    return issues[offset: offset + per_page]

@app.route('/', methods=['POST', 'GET'])
def main_page():
    r = requests.get("https://api.github.com/repos/walmartlabs/thorax/issues")
    issues = r.json()
    titles = [issue["title"] for issue in issues]
    page = request.args.get(get_page_parameter(), type=int, default=1)
    pagination = Pagination(page=page, per_page=10, total=len(issues), record_name="issues", css_framework="bootstrap4")

    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(issues)

    pagination_issues = get_issues(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework="bootstrap4")

    return render_template("issue_browser.html", issues=pagination_issues, pagination=pagination)

def update_website(commit_message):
    resume_dir = '../resume'
    input_dir = resume_dir + '/generated_resumes/website'
    website_dir = '../pecan-pine.github.io'
    output_dir = website_dir + '/shared'
    pdf_file = resume_dir + '/generated_resumes/programming/resume.pdf'    

    print(os.system(f'cd { resume_dir }; git pull;'))
    print(os.system(f'cd { website_dir }; git pull;'))

    input_files = os.listdir(input_dir)
    print(input_files)
    print(os.listdir(output_dir))


    for f in input_files:
        print(f'Copying file {f}...')
        os.system(f'cp { input_dir }/{f} {output_dir}/{f}')

    print(f'Copying resume pdf to main site')
    os.system(f'cp { pdf_file } { website_dir }/static/resume.pdf')

    print(f'Copying resume pdf to commandLine site')
    os.system(f'cp { pdf_file } { website_dir }/commandLineSite/static/resume.pdf')

    print(os.system(f'cd { website_dir }; git add .; git commit -m "{ commit_message }"; git push;'))
    print("Website git repository updated")
       
    
def write_commit_message(request):
    message = request.json
    ref = message["ref"]
    branch = ref.split("/")[-1]
    name = message["repository"]["name"]
    prev_commit = message["before"]
    current_commit = message["after"]
    compare_url = message["compare"]
    prev_commit_message = message["head_commit"]["message"]
    
    # expand_json(message) 
    commit_message_output = f"Updated resume-related files in website in \
response to commit # { current_commit } in \
pecan-pine/resume repository. The message for this commit \
was: '{ prev_commit_message }'. The previous commit was \
# { prev_commit }. Compare the changes here: { compare_url }."

    return commit_message_output


# expand a json message to better read what is included
def expand_json(message):
    for key in message:
        if type(message[key]) == type({}):
            for k in message[key]:
                print("values of", key, "key:", k, ":", message[key][k])
        else:
            print("value of", key, ":", message[key])
