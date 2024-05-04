# Overview

Example ETL Data pipeline to extract any CSV from the web and geo encode addreses.  


# Using this pipeline:

1) *Create a config file* - The config files are saved in the toml file format and should have the  file should contain the following fields:
   ```
    [header]
    name="WI Dairy plant license holders"
    url="https://mydatcp.wi.gov/documents/dfrs/Public_Dairy_Plant_License_Holders.csv"

    [cols]
    address="StreetAddress"
    city_col="City"
    state_col="StateZip"
    zip_col=""
    ```
    * Header - contains the pipeline name and the url of where to find the file, files will vary if file has one column for complete address then assign full address col to address col in config and leave the others blank/empty string, e.g. :
        ```
         [cols]
        address="oneAddressCol"
        city_col=""
        state_col=""
        zip_col=""
        ```
        
    * cols - Contains the columns for needed address columns, the pipeline will concatenate these together and then attempt to geocode the address using mapbox.

2) *Sign up for mapbox account* at `mapbox.com` create an API key
3) *Add API as an enviroment variable*: `export MAPBOX_API_KEY="<your API key here>"
4) *run pipeline* - run pipeline from command line as follows where ../config/wi_dairy_permit_holders.toml is the config file to run the pipeline for:
    `python main.py ../config/wi_dairy_permit_holders.toml`
