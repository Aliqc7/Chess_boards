# **Chess board image downloader**

Automatically saves images of all combinations of 2-D chess piece sets and board colors from [*Chess.com*](https://chess.com).


**Table of Contetnts**
- [Description](#description)
- [Getting started](#getting-started)
    - [Dependencies](#dependencies)
    - [Prerequisites](#prerequisites)
    - [Execution](#execution)

### **Description:**

This code performs webscraping using *Selenium* Python package to save images of all combinations of 2-D chess piece sets and board colors from [*Chess.com*](https://chess.com).
It automatically logs in using the user's chess.com username and password, iteratively changes the board and pieces settings to cover all desired combinations, saves the changes, captures
a screenshot containing the resulting chess boards, crops the image to include only the board, and saves the image.  
The images can be used to train a machine learning algorithm that can identify the position given the board image.  

### **Getting started**
#### ***Dependencies:***

The following packages need to be installed to run the code:

- Selenium
- Webdriver-manager

*Note:* See requirements.txt for the full list of requirements. 

#### ***Prerequisites:***

To run the code, you need to:

1- Sign up to [*Chess.com*](https://chess.com), for free, to get a username and password.

3- provide your chess.com username and password as environment variables using the following terminal commands:
```
export CHESS_USERNAME=<Your chess.com username>
export CHESS_PASSWORD=<Your chess.com password>
```

#### ***Execution:***
Upon exporting your username and password as environment variables simply execute:
```
python3 getboards.py
```
*Note 1:* A directory name "boardimages" will be created where the images will be saved

*Note 2:* A file named "last_complete_piece_set.txt" will be created to save them name of the last piece set style 
for which saving images have been completed. This is to avoid repetition in case the process is prematurely terminated for 
whatever reason (e.g., server error)

*Note 3:* If the process is terminated prematurely, simply rerun the code. 



