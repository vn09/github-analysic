## Introduction
This repo serves as a simple Flask Restful API application. 
Receiving input from other group, it retrieves data about Github repository via Github API v3.
This repo use [PyGithub](https://github.com/PyGithub/PyGithub) as a Python client library.

## Requirements
```
python 2.7
```
## How to install
Run 
```
sh install.sh
```
to install necessary libraries.
 
 ## How to test
 ### Test server (Group 1, Group 2 endpoints)
 
 ```
 python server_test.py
 ```
 Run this above to start test server. This server serves as the endpoint to send data forward.
 (Group 1, Group 2)
 
 ### Main server
 ```
 python server.py
 ```
 
 ### Using curl
 The json structure to receive data for main server is 
 ```
 {  
   "repos":[  
      {  
         "repo_name":"servant-api",
         "owner":"vn09",
         "token":""
      },
      {  
         "repo_name":"awesome-courses",
         "owner":"prakhar1989",
         "token":""
      },
      {  
         "repo_name":"linux",
         "owner":"torvalds",
         "token":""
      }
   ]
}
 ```
  
 ```
curl -X POST -H "Content-Type: application/json" -H "Cache-Control: no-cache" -d '{  
   "repos":[  
      {  
         "repo_name":"servant-api",
         "owner":"vn09",
         "token":""
      },
      {  
         "repo_name":"awesome-courses",
         "owner":"prakhar1989",
         "token":""
      },
      {  
         "repo_name":"linux",
         "owner":"torvalds",
         "token":""
      }
   ]
}' "http://localhost:8080/api/v1/repo-info"
 ```

## Problems
### TOKEN timeout
 TOKEN is revoked whenever it reaches limit rate. So we need to control number of request
 to re-generate TOKEN. What happens if we run in distribution? How many TOKENs do we need?
 And how we manage TOKENs?
 
 Re-generate TOKEN [here](https://github.com/settings/tokens).
