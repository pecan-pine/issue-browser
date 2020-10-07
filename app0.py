from flask import Flask, request, Response, redirect, render_template
import os
import requests

app = Flask(__name__)

# auto-reload templates
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/', methods=['POST', 'GET'])
def main_page():
    r = requests.get("https://api.github.com/repos/walmartlabs/thorax/issues")
    l = r.json()
    print(type(r.json()))
    print(r.json())
    for text in r.json():
        print(text)

    if request.method == 'POST':
        print("Post!")
        user_agent = request.headers["User-Agent"]
        if "GitHub-Hookshot" in user_agent.split("/"):
            commit_message = write_commit_message(request)
            print(commit_message)
            update_website(commit_message)
        return Response(status=200)
    return render_template("issue_browser.html", issues=r.json())

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
