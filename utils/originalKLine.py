import pandas as pd

# 获取原始K线数据
def get_original_kline(stock_type: str, stock_code: str, kline_precision: str, start_time: str, end_time: str):
    # 获取原始K线数据从csv中 返回一个df 包括股票代码 日期 开盘价 收盘价 最高价 最低价 成交量 
   # 获取csv文件  csvdatas文件夹和utils文件夹平级 当前py在utils文件夹中
    #如果stock_type包含 深证  kline_precision为daily 则获取csvdatas/ShenZhen/stock_type_daily.csv
    # 获取csv文件 
    print("在执行get_original_kline函数")
    if stock_type == "深证":
        csv_file_pathpre = f"csvdatas/ShenZhen/"
        if kline_precision == "daily":
            csv_file_path = f"{csv_file_pathpre}{stock_code}_daily.csv"
        elif kline_precision == "weekly":
            csv_file_path = f"{csv_file_pathpre}{stock_type}_weekly.csv"
    elif stock_type == "上证":
        csv_file_pathpre = f"csvdatas/ShangHai/"
        if kline_precision == "daily":
            csv_file_path = f"{csv_file_pathpre}{stock_code}_daily.csv"
        elif kline_precision == "weekly":
            csv_file_path = f"{csv_file_pathpre}{stock_type}_weekly.csv"
    # 获取csv文件 
    df = pd.read_csv(csv_file_path)
    # 只获取前7列
    df = df.iloc[:, :7] 
    # 过滤日期在start_time和end_time之间的行 csv中的日期格式为YYYYMMDD但是start_time和end_time的格式为YYYY-MM-DD
    # 将start_time和end_time的格式转换为YYYYMMDD
    start_time = start_time.replace('-', '')
    end_time = end_time.replace('-', '')
    print(start_time, end_time)
     # 确保日期列是 date类型 不要显示时分秒
    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
    # 过滤日期在start_time和end_time之间的行
    df = df[(df['trade_date'] >= start_time) & (df['trade_date'] <= end_time)]
    # 按照时间早的在前面晚的在后面排序
    df = df.sort_values(by='trade_date', ascending=True)
    # 返回df
    return df

    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')

    df = df[(df['trade_date'] >= start_time) & (df['trade_date'] <= end_time)]
    # 按照时间早的在前面晚的在后面排序
    df = df.sort_values(by='trade_date', ascending=True)
    # 返回df
    return df


