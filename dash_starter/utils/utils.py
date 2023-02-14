from ast import List
import pandas as pd
import numpy as np


def generate_random_pagenames(n: int = 10) -> list:
    """Generate a set of unique random page names

    a page name has the following format:
    main>[credit, account, rewards, payments, disputes, it]> [subpage[int 1to10]] > [subsubpage_[a to z]]]

    """
    main_pages = ['credit', 'account', 'rewards', 'payments', 'disputes', 'it']
    sub_pages = [f'subpage{str(i)}' for i in range(1, 11)]
    subsub_pages = [f'subsubpage_{chr(i)}' for i in range(97, 123)]
    page_names = []
    for _ in range(n):
        page_name = 'main>'
        page_name += main_pages[np.random.randint(0, len(main_pages))] + '>'
        page_name += sub_pages[np.random.randint(0, len(sub_pages))] + '>'
        page_name += subsub_pages[np.random.randint(0, len(subsub_pages))]
        page_names.append(page_name)
    return page_names


def simulate_traffic(n: int = 1000, random_pagenames: List = None, seed:int = 42) -> pd.DataFrame:
    """This functions creates a dataframe with the following columns:
    index PAGE_NAME that is a list of n pages generated using generate_random_pagenames
    IS_MOBILE that is either [MOB, OLB], each page has a MOB and OLB version
    RAW_TRAFFIC that is a list of random integers between 0 and 100000000
    RAW_TRAFFIC_WITH_CALL that is a list of random integers between 0 and 30% of RAW_TRAFFIC
    CALL_TO_TRAFFIC_RATIO that is RAW_TRAFFIC_WITH_CALL / RAW_TRAFFIC


    """
    np.random.seed(seed)
    if random_pagenames is None:
        random_pagenames = []
    df = pd.DataFrame()
    
    if random_pagenames is None:
        df['PAGE_NAME'] = generate_random_pagenames(n) * 2
    else:
        df['PAGE_NAME'] = random_pagenames * 2
        n = len(random_pagenames)
    df['IS_MOBILE'] = ['MOB'] * n + ['OLB'] * n
    df['RAW_TRAFFIC'] = np.random.default_rng().wald(
        1000, 50, n * 2)
    df['RAW_TRAFFIC_WITH_CALL'] = np.random.normal(
        0.15*df['RAW_TRAFFIC'], 0.15*df['RAW_TRAFFIC'], n * 2)
    # convert all values to int
    df['RAW_TRAFFIC'] = df['RAW_TRAFFIC'].astype(int)
    df['RAW_TRAFFIC_WITH_CALL'] = df['RAW_TRAFFIC_WITH_CALL'].astype(int)
    df['CALL_TO_TRAFFIC_RATIO'] = df['RAW_TRAFFIC_WITH_CALL']/df['RAW_TRAFFIC']
    return df
