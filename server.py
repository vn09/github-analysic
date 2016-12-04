from flask import Flask
from flask_restful import Resource, Api, reqparse
from github import Github
import json
import requests
from bs4 import BeautifulSoup
import urllib2

app = Flask(__name__)
api = Api(app)

GROUP1_ENDPOINT = "http://localhost:8181/api/v1/test/preprocessing"
GROUP2_ENDPOINT = "http://localhost:8181/api/v1/test/post-commit"

GIT_URL = "https://github.com/{}/{}"

# Parse request data
parser = reqparse.RequestParser()
parser.add_argument("repos",
                    required=True,
                    action='append',
                    help="Get all repos info from group 3")

# Token used for authentication
# Due to rate limit in Github requests
TOKEN = "9a548d84262e88bddfd5a26ca8ffa6022b9fa5bb"
g = Github(TOKEN)


class HelloWorld(Resource):
  def get(self):
    return {'hello': 'world'}


class RepoInfo(Resource):
  def post(self):
    try:
      success = True
      msg = None

      args = parser.parse_args()
      repos = args["repos"]
      for repo in repos:
        # Convert single quote string to dictionary type
        # and then json loads
        a_dict = eval(repo)
        repo = json.loads(json.dumps(a_dict))

        owner, repo_name, token = repo["owner"], repo["repo_name"], repo[
          "token"]

        languages, total_commit, last_commit = None, None, None
        # Public repo
        if len(token) == 0:
          repo = g.get_user(owner).get_repo(repo_name)
          languages = self.get_language(repo)
          total_commit = self.count_number_commit(owner, repo_name)
          last_commit = self.get_last_commit(repo)

        else:  # Private repo
          # TODO here
          pass

        # Send back data to group 1, group 2
        # Group 1
        requests.post(GROUP1_ENDPOINT,
                      data={
                        'git_url': GIT_URL.format(owner, repo_name) + ".git",
                        'languages': languages})
        # Group 2
        requests.post(GROUP2_ENDPOINT,
                      data={'repo_url': GIT_URL.format(owner, repo_name),
                            'commit_total': total_commit,
                            'last_commit': last_commit})
    except Exception as e:
      msg = e
      success = False
    finally:
      if success:
        return {
          "success": success
        }
      else:
        return {
          "success": success,
          "msg": msg
        }

  def get_language(self, repo):
    """
    Get languages of specific repo
    :param repo: repo object of
    :return:
    """
    languages = repo.get_languages()
    return languages.keys()

  def count_number_commit(self, owner, repo_name):
    """
    Get total commit by parsing html page of repo
    :param owner: owner of repository
    :param repo_name: repo name
    :return:
    """
    html = urllib2.urlopen(GIT_URL.format(owner, repo_name))
    bs = BeautifulSoup(html, "html.parser")

    commit = bs.find_all("li", class_="commits")
    if len(commit) > 0:
      commit = commit[0]
    return commit.a.span.get_text().strip()

  def get_last_commit(self, repo):
    """
    Get lastest commit of master branch
    :param repo: repo object
    :return: lastest commit of repo
    """
    branches = repo.get_protected_branch("master")
    return branches.commit.sha

# Mapping requests here
api.add_resource(HelloWorld, '/')
api.add_resource(RepoInfo, '/api/v1/repo-info')

if __name__ == '__main__':
  app.run(debug=True, host="localhost", port=8080)
