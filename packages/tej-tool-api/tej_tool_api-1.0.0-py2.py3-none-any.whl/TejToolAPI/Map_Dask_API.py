import pandas as pd
import datetime
import tejapi 
tejapi.ApiConfig.ignoretz = True
import numpy as np
import dask.dataframe as dd
import dask 
import multiprocessing
import gc

npartitions_local = multiprocessing.cpu_count()

default_start = '2013-01-01'
default_end = datetime.datetime.now().date().strftime('%Y-%m-%d')

def get_fin_data(table, tickers, columns=[], **kwargs):
    start = kwargs.get('start', default_start)
    end = kwargs.get('end', default_end)
    fin_type = kwargs.get('fin_type', ['A', 'Q', 'TTM'])
    transfer_to_chinese = False
    npartitions = kwargs.get('npartitions', npartitions_local)

    # transfer fin_ann_date to daily basis
    # days = generate_multicalendars(tickers, start = start, end = end)
    
    # 將需要的 column 選出
    columns += ['coid', 'mdate', 'annd', 'no', 'key3']
    columns = list(set(columns))

    # get all data
    data_sets = tejapi.get(table,
                    coid=tickers,
                    paginate=True,
                    chinese_column_name=False,
                    mdate={'gte': start, 'lte': end},
                    opts={'columns': columns, 'sort':{'coid.desc', 'mdate.asc', 'annd.asc', 'no.asc'}})
            
    # select certain fin_type
    data_sets = get_certain_fin_type(data_sets, fin_type)

    # parallel fin_type to columns 
    data_sets = fin_pivot(data_sets, remain_keys=['coid', 'mdate', 'no', 'annd'])

    return data_sets

def get_most_recent_date(data, sort_keys, subset, keep_mothod):
    # sort data order by mdate(accural date) and annd_s(announce date)
    data = data.sort_values(sort_keys)
    # when multiple rows have the same annd_s(announce date), keep the last row, which has the greatest mdate.
    data = data.drop_duplicates(subset = subset, keep = keep_mothod)

    return data


def get_trading_data(table, tickers, columns = [], **kwargs):
    start = kwargs.get('start', default_start)
    end = kwargs.get('end', default_end)
    npartitions = kwargs.get('npartitions', npartitions_local)
    # 自動補上 coid, mdate
    columns += ['coid', 'mdate']
    columns = list(set(columns))
    data_sets = tejapi.get(table,
                    coid = tickers,
                    paginate = True,
                    chinese_column_name=False,
                    mdate = {'gte':start,'lte':end},
                    opts = {'columns':columns, 'sort':{'coid.desc', 'mdate.desc'}})
    data_sets = dd.from_pandas(data_sets, npartitions=npartitions)

    return data_sets

def get_alternative_data(table, tickers=[], columns = [], **kwargs):
    start = kwargs.get('start', default_start)
    end = kwargs.get('end', default_end)
    transfer_to_chinese = False
    npartitions = kwargs.get('npartitions', npartitions_local)
    # 自動補上 coid, mdate, 發布日
    if table == 'TWN/APISALE':
        # 月營收
        columns += ['coid', 'mdate','annd_s']
        columns = list(set(columns))
    else:
        # 集保資料 
        columns += ['coid','mdate','edate1']
        columns = list(set(columns))
    # 營業日
    days = generate_multicalendars(tickers, start = start, end = end)
    # alternative data
    data_sets = tejapi.get(table,
                    coid = tickers,
                    paginate = True,
                    chinese_column_name=False,
                    mdate = {'gte':start,'lte':end},
                    opts = {'columns':columns, 'sort':{'coid.desc', 'mdate.desc'}})
    data_sets = data_sets.drop(columns=['mdate'])
    if table == 'TWN/APISALE':
        data_sets = dd.merge(days, data_sets, how='left', left_on = ['all_dates', 'coid'], right_on=['annd_s', 'coid'])
    else:
        data_sets = dd.merge(days, data_sets, how='left', left_on = ['all_dates', 'coid'], right_on=['edate1', 'coid'])
    del days
    gc.collect()
    data_sets = data_sets.groupby('coid', group_keys = False).apply(fillna_multicolumns, meta = data_sets)

    return data_sets

def get_fin_auditor(table, tickers, columns=[], **kwargs):
    # Setting defualt value of the parameters
    start = kwargs.get('start', default_start)
    end = kwargs.get('end', default_end)
    fin_type = kwargs.get('fin_type', ['A', 'Q', 'TTM'])
    transfer_to_chinese = False
    npartitions = kwargs.get('npartitions', npartitions_local)

    # 自動補上 coid, mdate
    columns += ['coid', 'mdate','key3','no','annd']
    columns = list(set(columns))

    # get fin data
    data_sets = tejapi.get(table,
                        coid = tickers,
                        paginate = True,
                        chinese_column_name=transfer_to_chinese,
                        mdate = {'gte':start,'lte':end},
                        opts= {'pivot':True, 'sort':{'coid.desc', 'mdate.asc', 'key3.asc', 'no.asc'}})
    

    # modify the name of the columns from upper case to lower case.
    lower_columns = {i:i.lower() for i in data_sets.columns}
    data_sets = data_sets.rename(columns=lower_columns)

    # select certain fin_type
    data_sets = get_certain_fin_type(data_sets, fin_type)

    # get most recent announce date of the company
    fin_date = get_announce_date(tickers, start = start, end = end)
    fin_date = get_certain_fin_type(fin_date, fin_type)
    data_sets = fin_date.merge(data_sets, how = 'left', on = ['coid', 'mdate', 'key3','no'])
    del fin_date
    gc.collect()

    # select columns
    data_sets = data_sets.loc[:,columns]

    # parallel fin_type to columns 
    data_sets = fin_pivot(data_sets, remain_keys=['coid','mdate','no','annd'])
    

    # Cut off the duplicate rows
    data_sets = data_sets.sort_values(['coid','mdate', 'annd'])
    data_sets = data_sets.drop_duplicates(subset=['coid', 'annd'], keep = 'last')

    return data_sets


def get_announce_date(tickers, **kwargs):
    start = kwargs.get('start', default_start)
    end = kwargs.get('end', default_end)
    data = tejapi.get('TWN/AINVFINQA',
                    coid = tickers,
                    paginate = True,
                    chinese_column_name=False, 
                    mdate = {'gte':start, 'lte':end},
                    opts = {'sort':{'coid.desc', 'mdate.asc', 'annd.asc'}})
    return data

def get_certain_fin_type(data, fin_type):
    if type(fin_type) is str:
        # data = data.query(f'key3 == "{fin_type}"')
        data = data.loc[data['key3']==fin_type,:]
    else:
        # data = data.query(f'key3.isin({fin_type})')
        data = data.loc[data['key3'].isin(fin_type),:]
    return data

def fin_pivot(df, remain_keys):
    # for loop execute pviot function
    uni = df['key3'].dropna().unique()
    data = pivot(df, remain_keys, uni[0])
    for i in range(1, len(uni)):
        temp = pivot(df, remain_keys, uni[i])
        data = data.merge(temp, on = remain_keys)
    return data


def pivot(df, remain_keys, pattern):
    try:
        data = df.loc[df['key3']==pattern, :]
        # Create a mapping table of column names and their corresponding new names.
        new_keys = {i:i+'_'+str(pattern) for i in data.columns.difference(remain_keys)}
        # Replace old names with the new ones.
        data = data.rename(columns = new_keys)
        data = data.loc[:,~data.columns.str.contains('key3')]
    except:
        raise ValueError('請使用 get_announce_date 檢查該檔股票的財務數據發布日是否為空值。')
    return data


def generate_multicalendars(tickers, **kwargs):
    start = kwargs.get('start', default_start)
    end = kwargs.get('end', default_end)
    npartitions = kwargs.get('npartitions', npartitions_local)

    def get_daily_calendar(ticker):
        cal = pd.date_range(start=start, end=end, freq='D')
        coid = [str(ticker)]*len(cal)
        return pd.DataFrame({'coid':coid, 'all_dates': cal})
    
    meta = pd.DataFrame({'coid': pd.Series(dtype='object'), 'all_dates': pd.Series(dtype='datetime64[ns]')})
    D_cal = dd.from_delayed([dask.delayed(get_daily_calendar)(ticker) for ticker in tickers], meta = meta)
    D_cal = D_cal.repartition(npartitions=npartitions)
    
    return D_cal

def fillna_multicolumns(df):
    return df.fillna(method = 'ffill')