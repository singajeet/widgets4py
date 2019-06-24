echo "Checking for new or modified files..."
git add .
git status

read -p "Push files to remote(y/n)?:" result

if [ $result=="y" ]
then
	git commit -m "$1"
	git push origin master
	echo "Files pushed successfully!"
else
	echo "File push cancelled!"
fi

