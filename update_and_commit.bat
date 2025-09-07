@echo off

echo Running compare_data.py...
python "C:\Users\Mr. Abhishek Lohiya\Desktop\Badminton Account\BaddyAutomation\badminton\compare_data.py"

echo Running update_data.py...
python "C:\Users\Mr. Abhishek Lohiya\Desktop\Badminton Account\BaddyAutomation\badminton\update_data.py"

echo Staging index.html...
git add index.html

echo Committing index.html...
set "commit_date=%date%"
git commit -m "data_updated_as_on_%commit_date%"

set /p push_confirmation="Do you want to push the changes to git? (y/n): "

if /i "%push_confirmation%"=="y" (
    echo Pushing to git...
    git push
) else (
    echo Skipping push.
)
