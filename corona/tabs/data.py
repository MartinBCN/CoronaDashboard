from pathlib import Path
import pandas as pd
pd.options.display.width = 0


def get_data() -> pd.DataFrame:
    p = Path(__file__).parents[2]
    df = pd.read_csv(p / 'data/owid-covid-data.csv')
    return df


if __name__ == '__main__':
    df = get_data()
    print(df.head())
    df['continent'].unique()

    for continent in df['continent'].unique():
        print(f'--- {continent} ---')
        df_pop_death = df[df['continent'] == continent][['date', 'location', 'total_cases', 'population']].copy()

        idx = df.groupby(['location'])['date'].transform(max) == df['date']

        df_pop_death = df_pop_death[idx]
        print(df_pop_death)

    print(df.rolling(7))
