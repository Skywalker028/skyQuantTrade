import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from sqlalchemy import create_engine

# PostgreSQL 数据库连接字符串
DATABASE_URL = "postgresql://postgres:123@localhost:5432/quantrade"

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

def upload_csv():
    # 打开文件对话框选择 CSV 文件
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            # 读取 CSV 文件
            df = pd.read_csv(file_path)
            # 将数据写入 PostgreSQL 数据库 表名是stock_day_a 表包括code date open high low close volume列 把csv的第八列作为code列 第一列作为date列 第二列作为open列 第三列作为high列 第四列作为low列 第五列作为close列 第六列作为volume列   
            df.columns = ['code', 'date', 'open', 'high', 'low', 'close', 'volume']
            # 将code列转换为字符串类型
            df['code'] = df['code'].astype(str)
            # 将date列转换为日期类型csv中日期为20201120格式
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
            # 将数据写入 PostgreSQL 数据库 表名是stock_day_a
            df.to_sql('stock_day_a', engine, if_exists='append', index=False)
            messagebox.showinfo("Success", "CSV file uploaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload CSV file: {str(e)}")

# 创建主窗口
root = tk.Tk()
root.title("CSV to PostgreSQL Uploader")
root.geometry("400x300")  # 设置窗口大小为 400x300 像素

# 创建上传按钮
upload_button = tk.Button(root, text="Upload CSV", command=upload_csv)
upload_button.pack(pady=20)

# 运行主循环
root.mainloop()


