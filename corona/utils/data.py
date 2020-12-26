import os
from pathlib import Path
import pandas as pd
pd.options.display.width = 0


def get_data() -> pd.DataFrame:
    data = Path(os.environ['DATA_DIR'])
    fn = data / Path('owid-covid-data.csv')
    df = pd.read_csv(fn)

    fn = data / Path('head_of_government.csv')
    heads = pd.read_csv(fn)

    df = df.merge(heads, on=['location'], how='left')

    return df


if __name__ == '__main__':
    df = get_data()

    print(df.head())
