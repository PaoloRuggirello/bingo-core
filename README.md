# bingo-core
Core library of Bingo project

###Powered by:
######SPC, PR



###All modules:
Bingo-core: https://github.com/PaoloRuggirello/bingo-core \
Bingo-BE: https://github.com/PaoloRuggirello/bingo-be \
Bingo-FE: https://github.com/spioc999/bingo_fe

###Building library
To build the library follow these step:
1. Create a project structure like the following: \
   | Bingo \
   | -  bingo-core \
   | -  bingo-be \
   | -  bingo-fe
2. Move inside bingo-core package, install requirements with the following command
   > `pip install -r requirements.txt`
3. The run the following command to build the library
   > `python3 setup.py sdist --dist-dir ../bingo-be/dist/`
4. Now you can move to the root folder "Bingo" and run the following command to build the whole project:
   > `docker-compose up`