import pandas as pd
import numpy as np

# 读取数据
file_path = "CHN_award_rates.xlsx"
data = pd.read_excel(file_path)

# 数据预处理：填充缺失值
data.fillna(0, inplace=True)

# 第一层熵增模型计算：计算每个项目下金银铜牌得奖率的权重
def entropy_weight_method(matrix):
    """
    熵权法计算权重
    """
    # 标准化：每一列除以该列的和
    column_sums = matrix.sum(axis=0, keepdims=True)
    column_sums[column_sums == 0] = 1  # 避免除以零
    P = matrix / column_sums
    # 计算熵值
    P[P == 0] = 1e-9  # 避免log(0)
    entropy = -(P * np.log(P)).sum(axis=0) / np.log(P.shape[0])
    entropy[np.isnan(entropy)] = 0  # 处理无效值
    # 计算权重
    weights = (1 - entropy) / (1 - entropy).sum()
    weights[np.isnan(weights)] = 0  # 处理无效值
    return weights

# 按项目分组计算第一层权重：处理每个项目的金银铜牌得奖率
projects = data['Sport'].unique()
weight_matrix = pd.DataFrame(index=['Gold_Weight', 'Silver_Weight', 'Bronze_Weight'], columns=projects)

for sport in projects:
    # 提取该项目的金银铜奖得奖率（按年份为列，奖项为行）
    sport_data = data[data['Sport'] == sport][['Gold_Rate', 'Silver_Rate', 'Bronze_Rate']]
    sport_weights = entropy_weight_method(sport_data.values)  # 计算该项目的金银铜奖权重
    
    # 将结果存储在权重矩阵中
    weight_matrix[sport] = sport_weights

# 转置矩阵，使每行代表一个项目，列为金银铜牌权重
weight_matrix = weight_matrix.T
weight_matrix.reset_index(inplace=True)
weight_matrix.rename(columns={'index': 'Sport'}, inplace=True)
# 使用TOPSIS分析进行项目排序
def topsis_analysis(matrix):
    """
    TOPSIS 分析
    """
    ideal_positive = np.max(matrix, axis=0)  # 理想最优值
    ideal_negative = np.min(matrix, axis=0)  # 理想最劣值
    dist_positive = np.sqrt(((matrix - ideal_positive) ** 2).sum(axis=1))  # 与理想最优的距离
    dist_negative = np.sqrt(((matrix - ideal_negative) ** 2).sum(axis=1))  # 与理想最劣的距离
    scores = dist_negative / (dist_positive + dist_negative)  # 综合得分
    return scores

# 提取权重矩阵的值进行TOPSIS打分
topsis_scores = topsis_analysis(weight_matrix.iloc[:, 1:].values)

# 整理最终结果
final_result = pd.DataFrame({
    'Sport': weight_matrix['Sport'],
    'TOPSIS_Score': topsis_scores
}).sort_values(by='TOPSIS_Score', ascending=False)

# 输出最终结果
print("最终结果：")
print(final_result)
final_result.to_excel('CHN2.xlsx', index=False)
