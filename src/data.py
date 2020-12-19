from pathlib import Path
import pandas as pd
pd.options.display.width = 0


def get_data() -> pd.DataFrame:
    p = Path(__file__).parents[1]
    df = pd.read_csv(p / 'data/owid-covid-data.csv')
    return df


if __name__ == '__main__':
    print(get_data().head())
