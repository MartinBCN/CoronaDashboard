import os
from pathlib import Path
import pandas as pd
import io
import requests
import logging
logger = logging.getLogger('corona.utils.data')
pd.options.display.width = 0


def get_data() -> pd.DataFrame:
    """
    Curl the data from the website https://covid.ourworldindata.org/data/owid-covid-data.csv
    If for whatever reason this does not succeed we log an error and load a static file
    Returns
    -------

    """

    data = Path(os.environ['DATA_DIR'])

    try:
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        s = requests.get(url).content
        df = pd.read_csv(io.StringIO(s.decode('utf-8')))
    except Exception as e:
        logger.error('Could not load latest data')
        logger.error(f'Exception: {e}')

        fn = data / Path('owid-covid-data.csv')
        df = pd.read_csv(fn)

    fn = data / Path('head_of_government.csv')
    heads = pd.read_csv(fn)

    df = df.merge(heads, on=['location'], how='left')

    return df


if __name__ == '__main__':
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    os.environ['DATA_DIR'] = f"{Path(__file__).parents[2] / 'data'}"

    ddf = get_data()

    print(ddf.head())
