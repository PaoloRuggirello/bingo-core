# bingo-core
Core library of Bingo project

###Powered by:
######SPC, PR



###All modules:
Bingo-core: https://github.com/PaoloRuggirello/bingo-core \
Bingo-BE: https://github.com/PaoloRuggirello/bingo-be \
Bingo-FE: https://github.com/spioc999/bingo_fe

###Building library And Run Project
To build the library and execute the web-app follow these step:
1. Create a project structure like the following: \
   Bingo \
   | -  bingo-core \
   | -  bingo-be \
   | -  bingo-fe
2. Move inside bingo-core package, install requirements with the following command
   > `pip install -r requirements.txt`
3. Then run the following command to build the library
   > `python3 setup.py sdist --dist-dir ../bingo-be/lib_dist/`
4. Now you can move in the 'bingo-docker' folder of this project and perform the following command to run the project:
   > `docker-compose up`
   
N.B The first time the 'docker-compose up' command will build the project. 

If you want to stop running containers you can easily type (make sure you are in bingo-docker folder):
> docker-compose stop

If you want to stop running containers and delete them or just want to delete these containers type:
> docker-compose down

   
The first run of docker-compose will show several errors of bingo-be that can't run, 
wait until the db setup properly, so you can connect to the main page using 
localhost:80/ as url in the browser 