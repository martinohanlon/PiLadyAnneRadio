cd ~/radiocontrol
sudo rm ~/radiocontrol/sourcecode/*.pyc
git add *
git commit -m "$1"
git push origin master

