# MAStrategy.py 均线交叉策略（Moving Average Crossover Strategy）
# 该策略基于短期和长期移动平均线的交叉来产生交易信号
# 当短期均线上穿长期均线时买入（金叉），下穿时卖出（死叉）

import pandas as pd
import numpy as np
from .BaseStrategy import BaseStrategy

class MAStrategy(BaseStrategy):
    def __init__(self, data, short_window=5, long_window=10, initial_cash=100000):
        """
        初始化均线交叉策略
        Args:
            data: DataFrame, 包含 OHLCV 数据的 DataFrame
            short_window: int, 短期均线周期，默认为5日
            long_window: int, 长期均线周期，默认为20日
            initial_cash: float, 初始资金，默认为100000
        """
        super().__init__(data)
        self.short_window = short_window  # 短期均线周期，例如5日均线
        self.long_window = long_window    # 长期均线周期，例如20日均线
        self.initial_cash = initial_cash  # 保存初始资金
        self.cash = initial_cash          # 初始资金
        self.positions = []               # 持仓记录，记录每次买入的股票数量
        self.portfolio_value = initial_cash  # 组合价值，包括现金和持仓市值
    
    def initialize(self):
        """
        初始化策略参数
        1. 计算短期和长期移动平均线
        2. 生成交易信号：
           - 1: 买入信号（金叉）
           - -1: 卖出信号（死叉）
           - 0: 无信号
        """
        # 计算移动平均线
        self.data['MA_short'] = self.data['close'].rolling(window=self.short_window).mean()  # 短期均线
        self.data['MA_long'] = self.data['close'].rolling(window=self.long_window).mean()    # 长期均线
        
        # 只在交叉点产生信号
        self.data['signal'] = 0
        # 金叉：当前短期均线在长期均线上方，且前一天在下方
        self.data.loc[(self.data['MA_short'] > self.data['MA_long']) & 
                     (self.data['MA_short'].shift(1) <= self.data['MA_long'].shift(1)), 'signal'] = 1
        # 死叉：当前短期均线在长期均线下方，且前一天在上方
        self.data.loc[(self.data['MA_short'] < self.data['MA_long']) & 
                     (self.data['MA_short'].shift(1) >= self.data['MA_long'].shift(1)), 'signal'] = -1
    
    def generate_signal(self):
        """
        生成交易信号
        Returns:
            int: 1(买入) / -1(卖出) / 0(持仓不变)
        """
        # 获取最新的信号
        current_signal = self.data['signal'].iloc[-1]
        return current_signal
    
    def handle_data(self, i=None):
        """
        处理每个交易日的数据
        Args:
            i: 当前处理的数据索引
        """
        if i is None:
            i = len(self.positions)  # 如果没有提供索引，使用持仓长度作为索引
        
        if i >= len(self.data):
            return
        
        # 获取当前时间点的信号和价格
        signal = self.data['signal'].iloc[i]
        current_price = self.data['close'].iloc[i]
        
        if signal == 1 and self.cash > 0:  # 买入信号且有可用资金
            shares = self.cash // current_price  # 计算可买入的股票数量
            self.place_order(
                symbol=self.data['ts_code'].iloc[i], 
                amount=shares,
                current_index=i
            )
        elif signal == -1 and len(self.positions) > 0:  # 卖出信号且有持仓
            self.place_order(
                symbol=self.data['ts_code'].iloc[i], 
                amount=-self.positions[-1],
                current_index=i
            )
    
    def place_order(self, symbol, amount, current_index, order_type='market'):
        """执行交易订单"""
        current_price = self.data['close'].iloc[current_index]
        
        if amount > 0:  # 买入操作
            cost = amount * current_price
            if cost <= self.cash:
                self.cash -= cost
                self.positions.append(amount)
                self.log_trade({
                    'date': self.data['trade_date'].iloc[current_index],
                    'symbol': symbol,
                    'action': 'BUY',
                    'amount': amount,
                    'price': current_price
                })
        else:  # 卖出操作
            revenue = -amount * current_price
            self.cash += revenue
            self.positions = []
            self.log_trade({
                'date': self.data['trade_date'].iloc[current_index],
                'symbol': symbol,
                'action': 'SELL',
                'amount': -amount,
                'price': current_price
            })
    
    def calculate_returns(self):
        """
        计算策略收益率
        Returns:
            float: 策略总收益率（百分比）
        """
        final_value = self.cash
        if len(self.positions) > 0:
            last_price = self.data['close'].iloc[-1]
            position_value = sum(self.positions) * last_price
            final_value += position_value
        
        return (final_value - self.initial_cash) / self.initial_cash * 100
    
    def evaluate(self):
        """
        评估策略表现
        Returns:
            dict: 包含总收益率、最终资金、交易次数等指标
        """
        final_value = self.cash
        if len(self.positions) > 0:
            last_price = self.data['close'].iloc[-1]
            position_value = sum(self.positions) * last_price
            final_value += position_value
        
        return {
            'total_returns': self.calculate_returns(),  # 总收益率
            'final_cash': self.cash,                   # 现金
            'position_value': position_value if len(self.positions) > 0 else 0,  # 持仓市值
            'total_value': final_value,                # 总价值（现金+持仓）
            'number_of_trades': len(self.trades)       # 交易次数
        } 