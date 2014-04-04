from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

import json


@csrf_exempt
def hookPush(request):
	# check headers to see if it's got the github stuffs

	rtn_dict = {"status": False, "msg": "init"}

	''' example body text

	{
	  "ref": "refs/heads/master",
	  "after": "60280827f40cdf60fed12e082437c61ed0a96964",
	  "before": "dc080577436ff9c4b6d5013fc489f5ab4918a265",
	  "created": false,
	  "deleted": false,
	  "forced": false,
	  "compare": "https://github.com/tekton/DocuCanvas/compare/dc080577436f...60280827f40c",
	  "commits": [
	    {
	      "id": "60280827f40cdf60fed12e082437c61ed0a96964",
	      "distinct": true,
	      "message": "restarting git integration",
	      "timestamp": "2014-03-20T11:46:38-07:00",
	      "url": "https://github.com/tekton/DocuCanvas/commit/60280827f40cdf60fed12e082437c61ed0a96964",
	      "author": {
	        "name": "Tyler Agee",
	        "email": "tyler@pyroturtle.com",
	        "username": "tekton"
	      },
	      "committer": {
	        "name": "Tyler Agee",
	        "email": "tyler@pyroturtle.com",
	        "username": "tekton"
	      },
	      "added": [
	        "gitHooks/__init__.py",
	        "gitHooks/admin.py",
	        "gitHooks/models.py",
	        "gitHooks/tests.py",
	        "gitHooks/urls.py",
	        "gitHooks/views.py"
	      ],
	      "removed": [
	        "git_hooks/__init__.py",
	        "git_hooks/models.py",
	        "git_hooks/tests.py",
	        "git_hooks/views.py"
	      ],
	      "modified": [

	      ]
	    }
	  ],
	  "head_commit": {
	    "id": "60280827f40cdf60fed12e082437c61ed0a96964",
	    "distinct": true,
	    "message": "restarting git integration",
	    "timestamp": "2014-03-20T11:46:38-07:00",
	    "url": "https://github.com/tekton/DocuCanvas/commit/60280827f40cdf60fed12e082437c61ed0a96964",
	    "author": {
	      "name": "Tyler Agee",
	      "email": "tyler@pyroturtle.com",
	      "username": "tekton"
	    },
	    "committer": {
	      "name": "Tyler Agee",
	      "email": "tyler@pyroturtle.com",
	      "username": "tekton"
	    },
	    "added": [
	      "gitHooks/__init__.py",
	      "gitHooks/admin.py",
	      "gitHooks/models.py",
	      "gitHooks/tests.py",
	      "gitHooks/urls.py",
	      "gitHooks/views.py"
	    ],
	    "removed": [
	      "git_hooks/__init__.py",
	      "git_hooks/models.py",
	      "git_hooks/tests.py",
	      "git_hooks/views.py"
	    ],
	    "modified": [

	    ]
	  },
	  "repository": {
	    "id": 8282652,
	    "name": "DocuCanvas",
	    "url": "https://github.com/tekton/DocuCanvas",
	    "description": "",
	    "watchers": 1,
	    "stargazers": 1,
	    "forks": 0,
	    "fork": false,
	    "size": 14962,
	    "owner": {
	      "name": "tekton",
	      "email": "pyroturtle@gmail.com"
	    },
	    "private": false,
	    "open_issues": 0,
	    "has_issues": true,
	    "has_downloads": true,
	    "has_wiki": true,
	    "language": "Python",
	    "created_at": 1361245029,
	    "pushed_at": 1395341206,
	    "master_branch": "master"
	  },
	  "pusher": {
	    "name": "tekton",
	    "email": "pyroturtle@gmail.com"
	  }
	}
	'''


	event_type = request.META['X-GitHub-Event']
	delivery_type = request.META["X-GitHub-Delivery"]

	info = json.loads(request.body)

	### check to see which project is linked to this repository, if any
	rep = info["repository"]  # ie DocuCanvas is 8282652

	for commit in info["commits"]:
		# check this commit for a fixed in the message
		# no fixed? see if there's an issue id at all... :: \#(\d+?)\s 
		pass
