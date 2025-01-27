# import pandas as pd

# # 文件路径
# file_path = "GYM-USA2.xlsx"

# # 读取 Excel 文件
# data = pd.read_excel(file_path)

# # 定义奖牌的权重
# medal_weights = {
#     "Gold": 1,
#     "Silver": 0.5,
#     "Bronze": 0.2
# }

# # 获取所有的年份并排序
# years = sorted(data["Year"].unique())

# # 按国家分组计算
# countries = data["NOC"].unique()
# results = []

# for country in countries:
#     country_data = data[data["NOC"] == country]
#     country_result = []
    
#     for year in years:
#         # 当前年、前一年、下一年的数据
#         current_year_data = country_data[country_data["Year"] == year]
#         prev_year_data = country_data[country_data["Year"] == year - 4]  # 假设间隔为4年
#         next_year_data = country_data[country_data["Year"] == year + 4]
        
#         # 计算奖牌数量
#         def calculate_medal_score(year_data):
#             score = 0
#             for medal, weight in medal_weights.items():
#                 score += len(year_data[year_data["Medal"] == medal]) * weight
#             return score

#         # 当前年的奖牌数量
#         current_score = calculate_medal_score(current_year_data)
#         # 前一年和下一年的奖牌数量
#         prev_score = calculate_medal_score(prev_year_data)
#         next_score = calculate_medal_score(next_year_data)
        
#         # 计算该年的总奖牌数
#         total_score = current_score + prev_score + next_score
        
#         # 添加到结果
#         country_result.append({"NOC": country, "Year": year, "Medal Score": total_score})
    
#     results.extend(country_result)

# # 转换结果为 DataFrame
# results_df = pd.DataFrame(results)

# # 保存结果到 Excel
# results_df.to_excel("1.xlsx", index=False)

# print("奖牌趋势计算完成，结果已保存到 1.xlsx")





# import pandas as pd
# import ruptures as rpt

# # 读取数据
# file_path = "1.xlsx"
# data = pd.read_excel(file_path)

# # 获取国家列表
# countries = data["NOC"].unique()

# # 保存结果
# change_points_result = []

# for country in countries:
#     # 获取该国家的时间序列数据
#     country_data = data[data["NOC"] == country]
#     scores = country_data["Medal Score"].values
#     years = country_data["Year"].values

#     # 使用 PELT 算法检测变化点
#     algo = rpt.Pelt(model="rbf").fit(scores)
#     change_points = algo.predict(pen=0.01)  # `pen` 参数可以调整模型灵敏度

#     # 将变化点转换为年份
#     change_years = [years[cp - 1] for cp in change_points[:-1]]  # 忽略最后一个点（数据结束）
#     change_points_result.append({"NOC": country, "Change Years": change_years})

# # 输出结果到控制台
# for result in change_points_result:
#     print(f"国家: {result['NOC']}, 变化年份: {result['Change Years']}")




# import numpy as np
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
# from scipy.interpolate import make_interp_spline

# # 数据输入
# data = {
#     "NOC": ["CHN", "CHN", "CHN", "CHN", "CHN", "CHN", "CHN", "CHN", "CHN", "CHN",
#             "USA", "USA", "USA", "USA", "USA", "USA", "USA", "USA", "USA", "USA"],
#     "Year": [1984, 1988, 1992, 1996, 2004, 2008, 2012, 2016, 2020, 2024,
#              1984, 1988, 1992, 1996, 2004, 2008, 2012, 2016, 2020, 2024],
#     "Medal Score": [1.2, 1.2, 0.7, 0.5, 1.2, 1.2, 1.2, 1.0, 1.0, 0.0,
#                     0.5, 0.7, 0.2, 0.2, 0.5, 1.0, 1.2, 1.7, 1.7, 1.5]
# }

# df = pd.DataFrame(data)

# # 设置主题

# sns.set_theme(style="darkgrid")




# # 数据准备
# chn_data = df[df["NOC"] == "CHN"]
# usa_data = df[df["NOC"] == "USA"]

# # 创建插值平滑曲线
# def smooth_curve(x, y, num_points=300):
#     x_smooth = np.linspace(x.min(), x.max(), num_points)
#     y_smooth = make_interp_spline(x, y)(x_smooth)
#     return x_smooth, y_smooth

# chn_x_smooth, chn_y_smooth = smooth_curve(chn_data["Year"], chn_data["Medal Score"])
# usa_x_smooth, usa_y_smooth = smooth_curve(usa_data["Year"], usa_data["Medal Score"])

# # 绘图
# plt.figure(figsize=(10, 6))

# # CHN: 红色点划线
# plt.plot(chn_x_smooth, chn_y_smooth, color="red", linestyle="--", label="CHN", linewidth=2.5)

# # USA: 蓝色实线
# plt.plot(usa_x_smooth, usa_y_smooth, color="blue", linestyle="-", label="USA", linewidth=2.5)

# # 在USA的2008年点添加标注
# usa_2008_score = usa_data[usa_data["Year"] == 2008]["Medal Score"].values[0]
# plt.annotate(
#     "Turning Point",
#     xy=(2008, usa_2008_score),  # 转折点坐标
#     xytext=(2009, usa_2008_score - 0.3),  # 箭头起始坐标
#     arrowprops=dict(
#         facecolor='black',  # 箭头填充色
#         edgecolor='black',  # 箭头边框颜色
#         linewidth=1.5,  # 边框线宽
#         arrowstyle="->"
#     ),
#     fontsize=10,
#     color="black"
# )


# # 图标题和标签
# plt.title("Volleyball Medal for CHN and USA", fontsize=16)
# plt.xlabel("Year", fontsize=12)
# plt.ylabel("Medal Score", fontsize=12)
# plt.legend(title="NOC", loc="upper left")

# # 显示图
# plt.show()





import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set Seaborn theme
sns.set_theme(style="darkgrid")

# Create data dictionary
data_dict = {
    "NOC": [
        "USA volleyball", "USA volleyball", "USA volleyball", "USA volleyball", "USA volleyball",
        "USA volleyball", "USA volleyball", "USA volleyball", "USA volleyball", "USA volleyball",
        "USA volleyball", "USA gymnastics", "USA gymnastics", "USA gymnastics", "USA gymnastics",
        "USA gymnastics", "USA gymnastics", "USA gymnastics", "USA gymnastics", "USA gymnastics",
        "USA gymnastics", "USA gymnastics", "CHN", "CHN", "FRA", "FRA", "FRA", "FRA", "FRA", "FRA",
        "FRA", "FRA", "FRA", "FRA", "FRA"
    ],
    "Year": [
        1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024,
        1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024,
        2020, 2024, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024
    ],
    "Medal Score": [
        0.5, 0.7, 0.2, 0.2, 0, 0.5, 1, 1.2, 1.7, 1.7, 1.5,
        4.3, 5.9, 4.5, 4.5, 6.1, 7.9, 11.4, 14.4, 13.3, 13.7, 7.5,
        0, 1, 0, 0, 1, 0, 0, 0, 0.2, 0, 0.1, 0, 0.5
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data_dict)

# Filter data
gymnastics_data = df[df["NOC"] == "USA gymnastics"]
volleyball_and_others_data = df[df["NOC"] != "USA gymnastics"]

# Create a color palette for different line styles and colors
palette = {
    "USA gymnastics": "blue",
    "USA volleyball": "green",
    "CHN": "red",
    "FRA": "blue"
}

# Create line styles for each NOC
line_styles = {
    "USA gymnastics": "-",
    "USA volleyball": "--",
    "CHN": "-.",
    "FRA": ":"
}

# Plot gymnastics data
plt.figure(figsize=(10, 5))
for noc in gymnastics_data["NOC"].unique():
    data_noc = gymnastics_data[gymnastics_data["NOC"] == noc]
    sns.lineplot(data=data_noc, x="Year", y="Medal Score", label=noc, color=palette[noc], linestyle=line_styles[noc], linewidth=2.5)

# Annotate USA gymnastics 2000
gymnastics_2000_score = gymnastics_data[gymnastics_data["Year"] == 2000]["Medal Score"].values[0]
plt.annotate(
    "Turning Point",
    xy=(2000, gymnastics_2000_score),
    xytext=(2002, gymnastics_2000_score + 0.5),
    arrowprops=dict(facecolor='black', edgecolor='black', linewidth=1.5, arrowstyle="->"),
    fontsize=10, color="black"
)
plt.title("USA Gymnastics Medal Score Trend", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Medal Score", fontsize=12)
plt.legend(title="NOC", loc="upper left")
plt.tight_layout()
plt.show()

# Plot volleyball and other countries data
plt.figure(figsize=(12, 6))
for noc in volleyball_and_others_data["NOC"].unique():
    data_noc = volleyball_and_others_data[volleyball_and_others_data["NOC"] == noc]
    sns.lineplot(data=data_noc, x="Year", y="Medal Score", label=noc, color=palette.get(noc, "black"), linestyle=line_styles.get(noc, "-"), linewidth=2.5)

# Annotate USA volleyball 2008
volleyball_2008_score = volleyball_and_others_data[
    (volleyball_and_others_data["NOC"] == "USA volleyball") & (volleyball_and_others_data["Year"] == 2008)
]["Medal Score"].values[0]
plt.annotate(
    "Turning Point",
    xy=(2008, volleyball_2008_score),
    xytext=(2009, volleyball_2008_score - 0.2),
    arrowprops=dict(facecolor='black', edgecolor='black', linewidth=1.5, arrowstyle="->"),
    fontsize=10, color="black"
)

# Annotate CHN 2024
chn_2024_score = volleyball_and_others_data[
    (volleyball_and_others_data["NOC"] == "CHN") & (volleyball_and_others_data["Year"] == 2024)
]["Medal Score"].values[0]
plt.annotate(
    "Turning Point",
    xy=(2024, chn_2024_score),
    xytext=(2023, chn_2024_score + 0.3),
    arrowprops=dict(facecolor='black', edgecolor='black', linewidth=1.5, arrowstyle="->"),
    fontsize=10, color="black"
)

# Annotate FRA 2024
fra_2024_score = volleyball_and_others_data[
    (volleyball_and_others_data["NOC"] == "FRA") & (volleyball_and_others_data["Year"] == 2024)
]["Medal Score"].values[0]
plt.annotate(
    "Turning Point",
    xy=(2024, fra_2024_score),
    xytext=(2023, fra_2024_score + 0.2),
    arrowprops=dict(facecolor='black', edgecolor='black', linewidth=1.5, arrowstyle="->"),
    fontsize=10, color="black"
)

plt.title("Medal Score Trend for USA Volleyball, CHN, and FRA", fontsize=16)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Medal Score", fontsize=12)
plt.legend(title="NOC", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.show()
