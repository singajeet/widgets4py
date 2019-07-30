echo "Checking for new or modified files..."
git add .
git status
git commit -m %1
git push origin master
echo "Files pushed successfully!"
