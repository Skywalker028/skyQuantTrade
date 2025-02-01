import logging
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database.base import get_db
from utils.originalKLine import get_original_kline
from fastapi.middleware.cors import CORSMiddleware
from service.strategies.MAStrategy import MAStrategy
import pandas as pd

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# 定义允许的源
origins = [
    "http://localhost:8080",  # 允许的源
    "http://127.0.0.1:8080",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的请求头
)

@app.get("/")
async def read_root():
   
    logger.info("Root 111111 accessed")  # 使用日志记录
    return {"message": "Welcome to FastAPI!"}

@app.get("/test-db/")
async def test_db(db: Session = Depends(get_db)):
    try:
        # 查询表名为 jiaoyi 的表
        result = db.execute(text("SELECT * FROM jiaoyi"))
        rows = result.fetchall()  # 获取所有行
        
        # 将结果转换为字典列表
        return {"message": [dict(zip(result.keys(), row)) for row in rows]}  
    except Exception as e:
        logger.error(f"Error: {str(e)}")  # 使用日志记录错误信息
        return {"error": str(e)}


#通过股票类别  股票代码  k线精度 和起始时间和结束时间获取股票K线
@app.get("/get-stock-kline/")
async def get_stock_kline(stock_type: str, stock_code: str, kline_precision: str, start_time: str, end_time: str):
    # 这里可以添加获取K线的逻辑
    # 调用utils/originalKLine.py中的get_original_kline函数 获取股票K线
    df = get_original_kline(stock_type, stock_code, kline_precision, start_time, end_time)    
    # 返回值显示成一个多维数组
    result =[]
    for index, row in df.iterrows():
           result.append([
                 
                  # 股票代码
                row['trade_date'].strftime('%Y%m%d'),   # 交易日期
                row['open'],         # 开盘价
                row['close'],        # 收盘价
                row['high'],         # 最高价
                
                row['low'],          # 最低价
                row['vol'],          # 成交量
                row['ts_code'],  
        ])
    return result


#股票代码为002269 股票类别为深证  k线精度为daily 起始时间为2024-01-01的url是什么










    

@app.get("/test-strategy/")
async def test_strategy(stock_code: str, start_time: str, end_time: str):
    try:
        # 获取股票数据
        df = get_original_kline("上证", stock_code, "daily", start_time, end_time)
        
        # 创建并初始化策略
        strategy = MAStrategy(df)
        strategy.initialize()
        
        # 确保 df 和 signals 的长度一致
        # df = strategy.data  # 使用策略处理后的数据
        # signals = df['signal'].values  # 使用 values 替代 tolist()
        
        # # 构建返回结果
        # result = []
        # for i in range(len(df)):
        #     result.append([
        #         df['trade_date'].iloc[i].strftime('%Y%m%d'),   # 交易日期
        #         df['open'].iloc[i],         # 开盘价
        #         df['close'].iloc[i],        # 收盘价
        #         df['low'].iloc[i],          # 最低价
        #         df['high'].iloc[i],         # 最高价
        #         df['vol'].iloc[i],          # 成交量
        #         int(signals[i])             # 交易信号: 1(买入)/-1(卖出)/0(持有)
        #     ])
        # return result
        for i in range(len(df)):
            strategy.handle_data(i)  # 传入当前索引
        results = strategy.evaluate()
        print(f"总收益率: {results['total_returns']}%")
        print(f"最终资金: {results['final_cash']}")
        print(f"交易次数: {results['number_of_trades']}")
        return results
        
                 
        
        
    except Exception as e:
        print(f"Error: {str(e)}")  # 添加错误日志
        return {"error": str(e)}










    
