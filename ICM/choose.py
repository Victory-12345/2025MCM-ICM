import pandas as pd

def filter_duplicates(input_file, output_file):
    # 读取CSV文件
    df = pd.read_csv(input_file)
    
    # 按Year和Event分组，并保留每组的第一个
    filtered_df = df.drop_duplicates(subset=['Year', 'Event'], keep='first')
    
    # 将结果写入新的CSV文件
    filtered_df.to_csv(output_file, index=False)

# 调用函数
input_file = 'c:/Users/LEGION/Desktop/code/py/ICM/summerOly_athletes.csv'
output_file = 'c:/Users/LEGION/Desktop/code/py/ICM/mewmedal.csv'
filter_duplicates(input_file, output_file)
import pandas as pd

def calculate_medal_ratio(sport, noc, year, medal, input_file):
    # 读取CSV文件
    df = pd.read_csv(input_file)
    
    # 筛选出指定的Sport, NOC和Year的数据
    filtered_df = df[(df['Sport'] == sport) & (df['NOC'] == noc) & (df['Year'] == year)]
    
    # 计算该大项目（Sport）下的总event数目
    total_events = filtered_df['Event'].nunique()
    
    # 计算该国家在该年该大项目中获得指定奖牌的数目
    medal_count = filtered_df[filtered_df['Medal'] == medal].shape[0]
    
    # 计算奖牌数占大项目的比例
    if total_events > 0:
        medal_ratio = medal_count / total_events
    else:
        medal_ratio = 0
    
    return medal_ratio

# 示例调用
input_file = 'c:/Users/LEGION/Desktop/code/py/ICM/mewmedal.csv'
sport = 'Swimming'
noc = 'CHN'
year = 2024
medal = 'Gold'
ratio = calculate_medal_ratio(sport, noc, year, medal, input_file)
print(f'{noc}在{year}年{sport}项目中获得{medal}奖牌的比例为: {ratio:.2%}')