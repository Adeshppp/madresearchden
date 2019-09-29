# heroku login

# Create app wiht input name
heroku apps:create $1 --region eu

# Add git remote
heroku git:remote -a $1

heroku stack:set container -a $1

# Add DB at hobby tier. 
# django_heroku will deal with the login in settings.py
heroku addons:create heroku-postgresql:hobby-dev

# Force collect of static - just being explicit. 
heroku config:set DISABLE_COLLECTSTATIC=0

# Push the master branch to heroku
# OR git push heroku testbranch:master
 git push heroku $2:master

# TODO to update the envs with heroku config:set
# TODO to update the debug setting. 
# TODO update allowed hosts.
# TODO script to back up DB.
# TODO script to restore a DB 
# Install black as a pre-commit hook.


# To destroy app
# heroku apps:destroy $1--confirm $1