import pandas as pd

# 假设数据文件路径为 'summerOly_medal_counts.csv'
data = pd.read_csv('summerOly_medal_counts.csv')

# 参数设置
country_name = 'United States'  # 目标国家
year = 2028  # 目标年份

# 1. 计算全体国家每年的奖牌总数
medal_totals = data.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum()

# 2. 筛选目标国家的数据并排序
data_sorted = data.sort_values('Year')
country_data = data_sorted[data_sorted['Country'] == country_name]

# 3. 合并每年的奖牌总数
country_data = country_data.merge(medal_totals, on='Year', suffixes=('', '_total'))

# 4. 计算金牌得奖率
country_data['Gold_rate'] = country_data['Gold'] / country_data['Gold_total']

# 5. 只保留目标年份之前的数据
country_data_before_year = country_data[country_data['Year'] < year]

# 6. 提取得奖率序列并设置索引
gold_rate = country_data_before_year.set_index('Year')['Gold_rate']

# 7. 使用线性插值填充缺失值，得到 gold_rate_interpolated
gold_rate_interpolated = gold_rate.interpolate(method='linear')

# 输出处理后的时间序列
print("处理后的 Gold_rate 时间序列:")
print(gold_rate_interpolated)
