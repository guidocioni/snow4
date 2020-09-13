# snow4
Shows how to process data from the SNOW4 model from DWD in Python. Note that this only a collection of some scripts prepared to read the data...nothing fancy!

In `utils.py` the functions needed to read thed data are contained. `pandas` is used to read directly the file from the server without downloading them. The input files are nothing but zipped asci files, while the coordinates are binary files. 
Every file is split accordintg to the file structure declared by DWD...may need to be updated in the future. 

Both `ipynb` and `py` files show an example of how to read and plot data from snow accumulation. 
