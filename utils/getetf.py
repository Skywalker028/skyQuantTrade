import pandas as pd
import akshare as ak

# 设置 Pandas 显示选项
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.width', None)        # 自动调整宽度
pd.set_option('display.max_rows', None)     # 显示所有行

# 获取 ETF 历史分钟数据
fund_etf_hist_min_em_df = ak.fund_etf_hist_min_em(
    symbol="513130", 
    period="1", 
    adjust="", 
    start_date="2024-01-01 09:30:00", 
    end_date="2025-01-24 17:40:00"
)

# 打印输出完整的 DataFrame
print(fund_etf_hist_min_em_df)

# 保存到 CSV，使用 utf-8-sig 编码
fund_etf_hist_min_em_df.to_csv("513130_20250120_20250124.csv", index=False, encoding='utf-8-sig')
