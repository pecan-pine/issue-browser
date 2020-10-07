# GIB issue-browser
A **G**itHub **I**ssue **B**rowser app

This app uses a Flask app to make a simple GitHub issue browser. Currently it shows issues from 
https://github.com/walmartlabs/thorax/issues. The app shows a list of issues, with 10 issues per page. 
If you click on an issue name, it shows a detail page with comments about the issues. 

See the browser in action at [issue-browser](http://ec2-34-212-207-223.us-west-2.compute.amazonaws.com/).

The current running version is the branch new-rest-version, which uses the Python requests library to get issue data. That version has the feature of displaying comments. The main branch version reads data from a local file and only displays the initial issue. 
