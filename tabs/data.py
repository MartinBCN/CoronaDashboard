from pathlib import Path
import pandas as pd
pd.options.display.width = 0


def get_data() -> pd.DataFrame:
    fn = Path('data/owid-covid-data.csv')
    # p = Path(__file__).parents[1]
    # fn = p / fn
    df = pd.read_csv(fn)

    fn = Path('data/head_of_government.csv')
    # p = Path(__file__).parents[1]
    # fn = p / fn
    heads = pd.read_csv(fn)

    df = df.merge(heads, on=['location'], how='left')
    return df


if __name__ == '__main__':
    df = get_data()

    print(df.head())
