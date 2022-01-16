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
3. The run the following command to build the library
   > `python3 setup.py sdist --dist-dir ../bingo-be/lib_dist/`
4. Now you can move in the 'docker-general' folder of this project and run the following command to build the whole project:
   > `docker-compose up`
   
The first run of docker-compose will show several errors of bingo-be that can't run, 
wait until the db setup properly and then you can connect to the main page using 
localhost:80/ as url in the browser 