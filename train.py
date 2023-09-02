from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pandas as pd

# 读取Excel文件
df = pd.read_excel("user_topic_scores_sparse.xlsx", index_col="用户ID")

# 构建Surprise的数据集
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(df.stack().reset_index(), reader)
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# 构建SVD模型
model = SVD()

# 在训练集上拟合模型
model.fit(trainset)

# 在测试集上进行预测
predictions = model.test(testset)

# 打印前几个预测结果
for prediction in predictions[:10]:
    user_id = prediction.uid
    item_id = prediction.iid
    true_rating = prediction.r_ui
    predicted_rating = prediction.est
    print(f"用户{user_id} 对主题词{item_id} 的实际评分: {true_rating}, 预测评分: {predicted_rating}")
