import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# 1. 读取数据
athletes_file = "summerOly_athletes.csv"
medals_file = "summerOly_medal_counts.csv"

athletes_df = pd.read_csv(athletes_file)
medals_df = pd.read_csv(medals_file)

# 2. 筛选2024年数据
year = 2024
medals_2024 = medals_df[medals_df["Year"] == year]

# 3. 统计每个国家的运动员总数
athletes_2024 = athletes_df[athletes_df["Year"] == year]
athlete_counts = athletes_2024.groupby("Team").size().reset_index(name="Athlete_Count")

# 4. 合并奖牌和运动员数据
merged_data = medals_2024.merge(athlete_counts, left_on="Country", right_on="Team", how="left")

# 确保无缺失值，将缺失值填充为0
merged_data.fillna({"Athlete_Count": 0, "Gold": 0, "Silver": 0, "Bronze": 0, "Total": 0}, inplace=True)

# 5. 准备聚类特征：运动员总数, 奖牌总数, 金牌总数
features = merged_data[["Athlete_Count", "Total", "Gold"]]

# 6. 使用K-means聚类
kmeans = KMeans(n_clusters=4, random_state=42)
merged_data["Cluster"] = kmeans.fit_predict(features)

# 7. 计算每个类的总奖牌数，按总奖牌数排序
cluster_medal_sums = merged_data.groupby("Cluster")["Total"].sum().sort_values(ascending=False)
color_palette = sns.color_palette("husl", n_colors=4)  # 使用 Seaborn 的调色板
cluster_colors = {cluster: color_palette[idx % len(color_palette)] for idx, cluster in enumerate(cluster_medal_sums.index)}

# 设置 Seaborn 样式
sns.set_style("whitegrid")  # 设置背景样式
plt.rcParams['grid.color'] = "gray"  # 网格颜色
plt.rcParams['grid.linestyle'] = "--"  # 网格线样式
plt.rcParams['grid.alpha'] = 0.7  # 网格线透明度
plt.rcParams['font.size'] = 10  # 设置字体大小

# 8. 三维可视化：聚类结果 + 特殊标注
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d', facecolor="whitesmoke")  # 设置背景颜色

# 定义每个类的名称
# 定义每个类的英文名称
legend_names = {
    1: "Olympic power",
    2: "Medium Olympic power",
    3: "Weak Olympic power",
    0: "Countries that have never won a medal"
}

# 绘制每个聚类的点，并使用指定的图例名称
for cluster, color in cluster_colors.items():
    cluster_data = merged_data[merged_data["Cluster"] == cluster]
    ax.scatter(
        cluster_data["Athlete_Count"],
        cluster_data["Total"],
        cluster_data["Gold"],
        label=f"{legend_names.get(cluster, f'Cluster {cluster}')} ",
        color=color,
        s=80  # 点的大小
    )


# 9. 标注特殊数据：奖牌数为0且运动员数<50
special_data = merged_data[(merged_data["Total"] == 0) & (merged_data["Athlete_Count"] < 50)].head(10)

# 标注特殊数据点
for _, row in special_data.iterrows():
    ax.scatter(
        row["Athlete_Count"], row["Total"], row["Gold"],
        color="blue", marker="x", s=120, 
        label="Special case" if "Special case" not in ax.get_legend_handles_labels()[1] else ""  # 确保只添加一次图例
    )
    ax.text(
        row["Athlete_Count"], row["Total"], row["Gold"],
        row["Country"],
        fontsize=10, color="darkblue"
    )

# 设置三维图的轴标签
ax.set_xlabel("Athlete Count", fontsize=12)
ax.set_ylabel("Total Medals", fontsize=12)
ax.set_zlabel("Gold Medals", fontsize=12)
ax.set_title(" Clustering of Olympic Countries (2024)", fontsize=16, color="darkslategray")

# 设置网格线
ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.7)

# 设置图例
ax.legend(fontsize=12, loc='upper left', title="Country Categories", title_fontsize=12)

# 显示图表
plt.show()
