import numpy as np
import pandas as pd
from scipy.stats import norm

# 文件路径
athletes_file = 'summerOly_athletes.csv'

# 加载数据
athletes_df = pd.read_csv(athletes_file)

# 1. 选取一个感兴趣的列（示例：运动员总数 per Team）
# 统计2024年每个国家的运动员总数
athletes_2024 = athletes_df[athletes_df['Year'] == 2024]
athletes_count = athletes_2024.groupby('Team').size().reset_index(name='Athletes')

# 提取样本数据 (运动员总数)
sample_data = athletes_count['Athletes'].values

# 2. 定义 Bootstrap 函数
def bootstrap(data, num_iterations=1000, confidence_level=0.95):
    
    # Bootstrap 方法计算样本均值的置信区间。

    # 参数：
    # - data: 输入样本数据 (numpy array)
    # - num_iterations: Bootstrap 迭代次数
    # - confidence_level: 所需的置信水平 (默认 95%)

    # 返回：
    # - 样本均值
    # - 置信区间 (low, high)
    
    # 存储每次 bootstrap 的均值
    bootstrap_means = []

    for _ in range(num_iterations):
        # 随机有放回采样
        bootstrap_sample = np.random.choice(data, size=len(data), replace=True)
        # 计算均值
        bootstrap_means.append(np.mean(bootstrap_sample))

    # 计算均值分布的上下限
    lower_percentile = (1 - confidence_level) / 2
    upper_percentile = 1 - lower_percentile

    ci_low = np.percentile(bootstrap_means, 100 * lower_percentile)
    ci_high = np.percentile(bootstrap_means, 100 * upper_percentile)

    return np.mean(data), (ci_low, ci_high)

# 3. 应用 Bootstrap
mean, confidence_interval = bootstrap(sample_data, num_iterations=5000, confidence_level=0.95)

# 4. 输出结果
print("Bootstrap Results:")
print(f"Sample Mean: {mean:.2f}")
print(f"95% Confidence Interval: {confidence_interval}")

# 5. 可视化 Bootstrap 分布
import matplotlib.pyplot as plt
import seaborn as sns

# 绘制 Bootstrap 均值分布
sns.set(style='whitegrid')
plt.figure(figsize=(10, 6))
sns.histplot(
    data=sample_data,
    kde=True,
    bins=20,
    color='blue',
    label='Bootstrap Mean Distribution'
)
plt.axvline(confidence_interval[0], color='red', linestyle='--', label='95% CI Lower')
plt.axvline(confidence_interval[1], color='green', linestyle='--', label='95% CI Upper')
plt.axvline(mean, color='black', linestyle='-', label='Sample Mean')
plt.title('Bootstrap Distribution of Athlete Counts')
plt.xlabel('Athletes per Team')
plt.ylabel('Frequency')
plt.legend()
plt.show()
