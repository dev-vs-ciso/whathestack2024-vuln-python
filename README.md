# overloader
Two python programs to test denial of service conditions on JWT size.

Local run:
* Create a folder for the repo, install virtualenv in it. (in the folder run `virtualenv -p python3 .`)
* Start virtualenv (in the folder where you installed virtualenv run `source bin/activate`)
* Clone repo
* Switch to branch `overloader`
* install requirements `pip install -r requirements.txt`
* edit target in the programs
* Run `python jwt_flooder` - to find the best size of jwt
* Run `request_flooder` - to find how many requests overloads the app.