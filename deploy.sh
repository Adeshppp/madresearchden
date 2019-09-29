# heroku login

# Create app wiht input name
heroku apps:create $1 --region eu

# Add git remote
heroku git:remote -a $1

heroku stack:set container -a $1

# Push the master branch to heroku
# OR git push heroku testbranch:master
 git push heroku $2:master

# To destroy app
# heroku apps:destroy $1--confirm $1