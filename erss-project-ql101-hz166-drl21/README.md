# erss-project-ql101-hz166-drl21
Running:
modify backend/connect_config.py to make sure you are connecting to the appropriate ports.
After that,
run sudo-docker compose up to initialize the database.
run startserver.sh in the webApp directory to apply the sql migrations.
compile all the .proto files in the backend directory. You can ask ql101 for advice on getting the compiler running.
then (assuming the world is working) you can run 
"python amazon-server.py haveups" to test the back end. (initially i had a typo here)
