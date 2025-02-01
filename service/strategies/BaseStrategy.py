# BaseStrategy.py 策略基类

class BaseStrategy:
    def __init__(self, data):
        self.data = data
        self.positions = []  # 持仓记录
        self.trades = []     # 交易记录
        self.cash = 0        # 当前现金
        self.portfolio_value = 0  # 组合价值
    
    # 生成交易信号
    def generate_signal(self):
        """生成交易信号"""
        raise NotImplementedError
    
    # 评估策略表现 
    def evaluate(self):
        """评估策略表现"""
        raise NotImplementedError
    
    def initialize(self):
        """初始化策略参数"""
        raise NotImplementedError
    
    def handle_data(self):
        """处理每个时间点的数据"""
        raise NotImplementedError
    
    def place_order(self, symbol, amount, order_type='market'):
        """下单函数
        Args:
            symbol: 交易标的
            amount: 交易数量，正数买入，负数卖出
            order_type: 订单类型，市价单或限价单
        """
        raise NotImplementedError
    
    def calculate_position(self):
        """计算当前持仓"""
        raise NotImplementedError
    
    def calculate_returns(self):
        """计算收益率"""
        raise NotImplementedError
    
    def risk_management(self):
        """风险管理"""
        raise NotImplementedError
    
    def update_portfolio(self):
        """更新投资组合状态"""
        raise NotImplementedError
    
    def get_historical_data(self, symbol, start_date, end_date):
        """获取历史数据"""
        raise NotImplementedError
    
    def log_trade(self, trade):
        """记录交易"""
        self.trades.append(trade)
    
    def get_performance_metrics(self):
        """获取策略表现指标"""
        raise NotImplementedError
    
