# whathestack2024-vuln-python
The repository for the WhatTheStack2024 Python base demos and exercises. 
The following branches are here:

* common - some common components used by the other branches
* common-templates - some common templates/html used by the other branches
*  decode-no-verify - vulnerable instance that just decodes JWTs
*  jwt_session_storage - vulnerable instance that stores JWTs in local storage
* leaking-secret - almost secure instance, but it does leak secrets
*  main - just a readme 
*  overloader - tool to test DoS on the JWTs
*  rogue_data_stealer - server and tools to show why storing data outside of secure cookies is a bad idea
*  well-protected - a well protected instance


To run the instances:
* Create a folder for the repo, install virtualenv in it. (in the folder run `virtualenv -p python3 .`)
* Start virtualenv (in the folder where you installed virtualenv run `source bin/activate`)
* Clone repo
* Switch to branch
* install requirements `pip install -r requirements.txt`
* edit target in the programs
* Run `python app.py` 
* * If you want to run multiple apps, each on different port, run `flask run -h localhost -p 3000` - where 3000 is the port for this app. Change it for various services.