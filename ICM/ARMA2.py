import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# 加载数据
medal_data = pd.read_csv('summerOly_medal_counts.csv')

# 按年份统计金、银、铜牌总数
medal_totals = medal_data.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum()

def arma_forecast_total_medals(country_name, year, data):
    # 确保年份为整数并且数据按年份排序
    year = int(year)
    data_sorted = data.sort_values('Year')

    # 过滤出指定国家的数据
    country_data = data_sorted[data_sorted['Country'] == country_name]

    # 筛选出指定年份之前的数据
    country_data_before_year = country_data[country_data['Year'] < year]

    # 如果没有足够数据，返回提示
    if country_data_before_year.empty:
        return f"没有足够的数据来进行预测: {country_name} 在 {year} 年之前没有奖牌数据。"

    # 计算总奖牌数
    country_data_before_year['Total_Medals'] = country_data_before_year[['Gold', 'Silver', 'Bronze']].sum(axis=1)

    # 提取奖牌总数序列
    total_medals = country_data_before_year.set_index('Year')['Total_Medals']

    # 创建一个新的索引，从 1 开始递增
    new_index = range(1, len(total_medals) + 1)
    total_medals.index = new_index

    # 使用线性插值填充缺失值
    total_medals_interpolated = total_medals.interpolate(method='linear')

    # 拟合 ARIMA 模型（设置 (p, d, q) 参数）
    model = ARIMA(total_medals_interpolated, order=(2, 1, 2))
    fitted_model = model.fit()

    # 预测未来 5 届奥运会的总奖牌数
    forecast = fitted_model.get_forecast(steps=5)
    forecast_totals = forecast.predicted_mean

    # 创建预测年份索引
    forecast_years = pd.date_range(start=f'{year + 4}', periods=5, freq='4Y').year
    forecast_totals.index = forecast_years

    # 转换为 DataFrame 格式
    forecast_result = pd.DataFrame({
        'Country': country_name,
        'Year': forecast_totals.index,
        'Forecasted_Total_Medals': forecast_totals.values
    })

    return forecast_result

# 要预测的国家列表
countries_to_forecast = [
    "United States", "China", "Japan", "Australia", "France", "Netherlands", "Great Britain", "South Korea", 
    "Italy", "Germany", "New Zealand", "Canada", "Uzbekistan", "Hungary", "Spain", "Sweden", "Kenya", 
    "Norway", "Ireland", "Brazil", "Iran", "Ukraine", "Romania", "Georgia", "Belgium", "Bulgaria", "Serbia", 
    "Czech Republic", "Denmark", "Azerbaijan", "Croatia", "Cuba", "Bahrain", "Slovenia", "Chinese Taipei", 
    "Austria", "Hong Kong", "Philippines", "Algeria", "Indonesia", "Israel", "Poland", "Kazakhstan", "Jamaica", 
    "South Africa", "Thailand", "Ethiopia", "Switzerland", "Ecuador", "Portugal", "Greece", "Argentina", 
    "Egypt", "Tunisia", "Botswana", "Chile", "Saint Lucia", "Uganda", "Dominican Republic", "Guatemala", 
    "Morocco", "Dominica", "Pakistan", "Turkey", "Mexico", "Armenia", "Colombia", "Kyrgyzstan", "North Korea", 
    "Lithuania", "India", "Moldova", "Kosovo", "Cyprus", "Fiji", "Jordan", "Mongolia", "Panama", "Tajikistan", 
    "Albania", "Grenada", "Malaysia", "Puerto Rico", "Cabo Verde", "Ivory Coast", "Peru", "Qatar", 
    "Refugee Olympic Team", "Singapore", "Slovakia", "Zambia"
]

# 存储所有国家的预测结果
all_forecasts = []

# 遍历每个国家并进行预测
for country in countries_to_forecast:
    try:
        result = arma_forecast_total_medals(country, 2024, medal_data)
        if not isinstance(result, str):
            all_forecasts.append(result)
    except Exception as e:
        print(f"预测 {country} 时出错: {e}")

# 合并所有预测结果
if all_forecasts:
    final_forecasts = pd.concat(all_forecasts, ignore_index=True)

    # 将预测结果保存到一个新的 Excel 文件
    final_forecasts.to_excel('forecasted_medals.xlsx', index=False)
    print("预测完成！结果已保存到 'forecasted_medals.xlsx'")
else:
    print("没有成功的预测结果。")
