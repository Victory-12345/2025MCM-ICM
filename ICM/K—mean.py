import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# 1. 读取数据
athletes_file = "summerOly_athletes.csv"
hosts_file = "summerOly_hosts.csv"
medals_file = "summerOly_medal_counts.csv"

athletes_df = pd.read_csv(athletes_file)
hosts_df = pd.read_csv(hosts_file)
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

# 7. 可视化聚类结果
plt.figure(figsize=(10, 6))
for cluster in range(4):
    cluster_data = merged_data[merged_data["Cluster"] == cluster]
    plt.scatter(cluster_data["Athlete_Count"], cluster_data["Total"], label=f"Cluster {cluster}")

plt.xlabel("Athlete Count")
plt.ylabel("Total Medals")
plt.title("K-means Clustering of Countries (2024)")
plt.legend()
plt.grid()
plt.show()

# 8. 输出聚类结果
output_file = "clustered_countries_2024.csv"
merged_data.to_csv(output_file, index=False)
print(f"Clustering results saved to {output_file}")
