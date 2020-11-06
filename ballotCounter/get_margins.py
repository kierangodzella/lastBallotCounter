"""
Run directly from command line: $ python get_margins.py [options]
Options are optional!
Currently only supporting "-V" which will print out df heads for illustration.
TODO: add argument handling for multiple runs and average
"""

import pandas as pd
import numpy as np


def parse_pct(x: str):
    add = (">" in x)
    p = float(x.strip("%>")) / 100
    if add:
        p += np.random.rand() / 100
    return p


def calc_margin(dataframe, state: str):
    df = dataframe.drop(['Est. votes reported.1', 'Absentee', '2016 margin'], axis=1)
    df.dropna(inplace=True)
    df = df[df['Margin'].str.contains('\+')]
    df_out = pd.DataFrame(df['County'])
    df_out['Margin'] = df['Margin'].map(
        lambda x: float(x.split("+")[1]) if x.startswith('B') else -1 * float(x.split("+")[1])
        )
    df_out['Multiplier'] = df_out['Margin'].map(lambda x: (1/100) * (50 + x/2))

    df_out['Est. reported'] = df['Est. votes reported'].map(
        lambda x: parse_pct(x)
        )
    df_out['Total votes'] = df['Total votes']
    df_out['Remaining votes'] = df_out.apply(
        lambda row: float(row['Total votes']) / row['Est. reported'] - float(row['Total votes']), axis=1
    )
    df_out['Remaining D'] = df_out.apply(
        lambda row: row['Multiplier'] * row['Remaining votes'], axis=1
    )
    df_out['Remaining R'] = df_out.apply(
        lambda row: (1 - row['Multiplier']) * row['Remaining votes'], axis=1
    )
    df_out['D margin'] = df_out.apply(
        lambda row: row['Remaining D'] - row['Remaining R'], axis=1
    )
    d_margin_sum = np.floor(df_out['D margin'].sum())
    print(f"\nestimated final Joe lead in {state}: ", d_margin_sum)
    return d_margin_sum


if __name__ == '__main__':
    table_GA = pd.read_html(
        'https://www.nytimes.com/interactive/2020/11/03/us/elections/results-georgia-president.html')
    table_PA = pd.read_html(
        'https://www.nytimes.com/interactive/2020/11/03/us/elections/results-pennsylvania-president.html')
    table_NV = pd.read_html(
        'https://www.nytimes.com/interactive/2020/11/03/us/elections/results-nevada-president.html'
    )
    GA_margin = calc_margin(table_GA[2], "Georgia")
    PA_margin = calc_margin(table_PA[2], "Pennsylvania")
    NV_margin = calc_margin(table_PA[2], "Nevada")

