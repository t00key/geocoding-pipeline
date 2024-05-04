import click
import pandas as pd
from src.config import Config
import os
import requests as req
from datetime import datetime


def get_api_key():
    # get env variable MAPBOX_API_KEY and throw error if not found
    api_key = os.getenv("MAPBOX_API_KEY")
    if not api_key:
        raise ValueError("API key not found")
    return api_key


def geocode_address(addr, limit=1):
    """geocode address using mapbox service

    Args:
        addr (_type_): address string containing street, city, state, zip that you want to geocode
        limit (int, optional): number of results wanted from mapbox, default=1.

    Returns:
        list: list of lat and long for the address
    """
    api_key = get_api_key()
    url = f"https://api.mapbox.com/search/geocode/v6/forward?q={addr}&access_token={api_key}&limit={limit}"
    response = req.get(url)
    if response.status_code == 200:
        data = response.json()
        if response.json()["features"][0]["geometry"]["coordinates"]:
            data = response.json()["features"][0]["geometry"]["coordinates"]
            return data
        else:
            print(f"No data found for {addr}")
            return [0,0]

def extract(url) -> pd.DataFrame:
    print(f"Requesting {url}")
    # request URL and save file that is returned
    try:
        return pd.read_csv(url)
    except Exception as e:
        print(f"Error requesting file, error: {e}")


def transform(df: pd.DataFrame, cfg: Config) -> pd.DataFrame:
    """transform the data by adding full address and then geocoding it to get lat long 
    using the mapbox service

    Args:
        df (pd.DataFrame): _description_
        cfg (Config): _description_

    Returns:
        pd.DataFrame: _description_
    """
    # add strip in case city/state/zip are empty leaving whitespace in col name
    addr_cols = [cfg.address.strip(), cfg.city.strip(), cfg.state.strip(), cfg.zip.strip()]
    # remove any null /empty str cols from list
    addr_cols = [x for x in addr_cols if x]
    # create new col called full_address that is a concatenation of all address cols
    df.loc[:, "full_address"] = df[addr_cols].apply(lambda x: " ".join(x), axis=1)
    # replace any /r or /n in full_address with empty string
    df.loc[:, "full_address"] = df.full_address.str.replace("\r", "").str.replace("\n", "")
    # get unique addresses
    unqiue_df = df.drop_duplicates(subset="full_address")
    results = []
    # iterate through each address and get lat long
    for addr in unqiue_df.full_address:
        lat_lon = geocode_address(addr)
        print(f"Geocoding adress: {addr}, lat/long: {lat_lon}")
        results.append(lat_lon)
    # quick fix for bug - need to fix geocode - replace None with [0,0]
    results = [x if x else [0,0] for x in results]
    # add the results to the dataframe to lat and long cols
    breakpoint() 
    unqiue_df.loc[:, "lat"] = [x[1] for x in results]
    unqiue_df.loc[:, "long"] = [x[0] for x in results]
    # merge the results back to the original dataframe
    df = df.merge(unqiue_df[["full_address", "lat", "long"]], on="full_address", how="left")
    return df


def load(df: pd.DataFrame, filename:str) -> None:
    # future save to DB, currently just save to csv
    df.to_csv(filename, index=False)


# create click command method that accepts config file as arg and then loads that config file
@click.command()
@click.argument("config_file", type=click.Path(exists=True))
def main(config_file):
    start_time = datetime.now()
    config = Config(config_file)
    print(f"running pipeline for {config.filename}...")
    df = extract(config.url)
    df = transform(df, config)
    out_file = f'{config.data_path()}/output_{config.name.lower().replace(" ", "_")}.csv'
    load(df, out_file)
    durr = datetime.now() - start_time
    print(f"Pipeline completed!, pipeline runtime: {durr}")


if __name__ == "__main__":
    main()
