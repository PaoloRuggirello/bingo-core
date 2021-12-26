# bingo-core
Core library of Bingo project

###Powered by:
######SPC, PR



###All modules:
Bingo-core: https://github.com/PaoloRuggirello/bingo-core \
Bingo-BE: https://github.com/PaoloRuggirello/bingo-be \
Bingo-FE: https://github.com/spioc999/bingo_fe

###Building library
To build the library use the command:
> `python3 setup.py sdist bdist_wheel`

This command generate a dist folder, inside that you can find the build of the library. \
Then move to the project that should import the library and install it with pip:

> pip install ${path-to-the-dist-folder}


Then you can import the library typing:
> from bingo import *