from flask import Flask
from flask_restful import Resource, Api, reqparse
import json

app = Flask(__name__)
api = Api(app)

GROUP1_ENDPOINT = "/api/v1/test/preprocessing"
GROUP2_ENDPOINT = "/api/v1/test/post-commit"

# Parse request data
preProcessingParser = reqparse.RequestParser()
preProcessingParser.add_argument("git_url", required=True)
preProcessingParser.add_argument("languages", required=True, action='append')

dataCommitParser = reqparse.RequestParser()
dataCommitParser.add_argument("repo_url", required=True)
dataCommitParser.add_argument("commit_total", required=True)
dataCommitParser.add_argument("last_commit", required=True)


class HelloWorld(Resource):
  def get(self):
    return {'hello': 'hello world'}


class PreProcessing(Resource):
  def post(self):
    args = preProcessingParser.parse_args()
    git_url = args["git_url"]
    languages = args["languages"]
    print "GIT url: ", git_url
    print "Language: ", languages


class DataCommit(Resource):
  def post(self):
    args = dataCommitParser.parse_args()
    print "Repo URL: ", args["repo_url"]
    print "Total commit: ", args["commit_total"]
    print "Last commit: ", args["last_commit"]


api.add_resource(HelloWorld, '/')
api.add_resource(PreProcessing, GROUP1_ENDPOINT)
api.add_resource(DataCommit, GROUP2_ENDPOINT)

if __name__ == '__main__':
  app.run(debug=True, host="localhost", port=8181)
