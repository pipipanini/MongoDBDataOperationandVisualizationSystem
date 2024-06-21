# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 18:54:27 2024

@author: 86159
"""

import pymongo
import pandas as pd
import tkinter as tk
from tkinter import messagebox, simpledialog

# 连接到 MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["doubanmovies"]  
collection = db["douban250movies"] 

file_path = "C:/Users/86159/Desktop/mogodb大作业/douban.xlsx"
df = pd.read_excel(file_path)
data = pd.read_excel(file_path)

# 将数据插入到 MongoDB
collection.insert_many(data.to_dict('records'))


# 创建主窗口
app = tk.Tk()
app.title("MongoDB数据操作与可视化")

# 创建标签和输入框
query_label = tk.Label(app, text="查询条件:")
query_label.pack(pady=5)
query_entry = tk.Entry(app, width=50)
query_entry.pack(pady=5)


# 创建查询按钮
def execute_query():
    query_str = query_entry.get()
    try:
        query_dict = eval(query_str)
        results = collection.find(query_dict)
        display_results(results)
    except Exception as e:
        messagebox.showerror("错误", f"查询失败: {e}")

query_button = tk.Button(app, text="执行查询", command=execute_query)
query_button.pack(pady=10)

# 创建结果显示区域
results_text = tk.Text(app, width=80, height=20)
results_text.pack(pady=10)

def display_results(results):
    results_text.delete(1.0, tk.END)
    for result in results:
        results_text.insert(tk.END, str(result) + "\n")




# 增加数据
def add_data():
    new_data_str = simpledialog.askstring("增加数据", "请输入新的数据（JSON格式）:")
    try:
        new_data_dict = eval(new_data_str)
        collection.insert_one(new_data_dict)
        messagebox.showinfo("成功", "数据增加成功!")
    except Exception as e:
        messagebox.showerror("错误", f"数据增加失败: {e}")

add_button = tk.Button(app, text="增加数据", command=add_data)
add_button.pack(pady=5)

# 删除数据
def delete_data():
    delete_query_str = simpledialog.askstring("删除数据", "请输入删除条件（JSON格式）:")
    try:
        delete_query_dict = eval(delete_query_str)
        result = collection.delete_many(delete_query_dict)
        messagebox.showinfo("成功", f"数据删除成功! 删除了 {result.deleted_count} 条记录。")
    except Exception as e:
        messagebox.showerror("错误", f"数据删除失败: {e}")

delete_button = tk.Button(app, text="删除数据", command=delete_data)
delete_button.pack(pady=5)

# 修改数据
def update_data():
    update_query_str = simpledialog.askstring("修改数据", "请输入修改条件（JSON格式）:")
    update_data_str = simpledialog.askstring("修改数据", "请输入新的数据（JSON格式）:")
    try:
        update_query_dict = eval(update_query_str)
        update_data_dict = eval(update_data_str)
        result = collection.update_many(update_query_dict, {'$set': update_data_dict})
        messagebox.showinfo("成功", f"数据修改成功! 修改了 {result.modified_count} 条记录。")
    except Exception as e:
        messagebox.showerror("错误", f"数据修改失败: {e}")

update_button = tk.Button(app, text="修改数据", command=update_data)
update_button.pack(pady=5)

# 启动主事件循环
app.mainloop()


