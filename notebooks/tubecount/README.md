# Terminal Traffic Tube Count

## Author:
Karen Ficenec - karen.ficenec@nrel.gov

## Description
This analysis repo includes analysis of data from the traffic engineering team at DFW given for March 15th 2019. Tube counts are given as well as terminal dwell times. The data is cleaned, analyzed, and visualized in the jupyter notebook file TrafficVehicleVolumeValidation.ipynb.

## Purpose
Report dwell distributions at the curb and better estimate the flow of traffic to each terminal within the airport.

## How to...

###   Run the code:
  1) Clone this repo to a folder locally.  
  2) Download anaconda here: https://www.anaconda.com/distribution/ (click the download button & follow instructions for your OS). Use the python 3.7 version.  
  3) Once you have downloaded anaconda, you can open it. Then click the "jupyter notebook" button to open a browser with your file system. Once the browser window opens, navigate to where you cloned this repo to within your filesystem and double-click the TrafficVehicleVolumeValidation.ipynb file to open it.  
  4) Setup the environment:  
      1) Either follow the instructions here: https://github.com/NREL/ATHENA-twin in the "Environment Installation" section.  
      2) OR, if you only want to run this notebook and not other repo's notebooks within the athena project:  
        1) In a terminal type "conda create --name athena python=3.7 pandas numpy matplotlib seaborn".  
        2) Then type "python -m ipykernel install --user --name athena --display-name "Python (athena)".  
        3) In the jupyter notebook click the "kernal" tab near the top, go to "change kernal" and select "Python (athena)" from the drop-down menu.  
  5) Hit shift enter on a cell in the notebook to run it and move on to the next cell. But you can't run too many cells without also accessing the data...
  
###   Get the data:
  Once Matt and Monte work out permissions issues, this will change to an AWS solution.
  For now, if you have access to the ATHENA - team google drive, navigate through these folders: Data --> Recieved Data --> Archival Copy --> DFW --> Traffic Engineering --> Central Terminal Area (March 15, 2019). Download the zip ("Traffic Data CTA.zip") and open it. The unzipped item should be a folder. Rename the folder "data" and move it to the same folder that holds the "TrafficVehicleVolumeValidation.ipynb". (This is because the code accesses the data by referencing the parent folder that is holding the notebook file.)
  
