import statistics
import numpy as np
import matplotlib.pyplot as plt

# 生成一个长度为 540*119 的一维列表作为示例数据
data = np.random.rand(540*119)
64800
# 将一维列表转换为二维列表，每 540 个元素为一组
grouped_data = np.array(data).reshape(-1, 540)

# 计算每组数据的平均值和标准差
means = np.mean(grouped_data, axis=1)
stds = np.std(grouped_data, axis=1)
len(stds)
# 生成 x 轴的数值
x = np.arange(1, 120)

# 在 Matplotlib 中绘制 error bar
fig, ax = plt.subplots()
ax.errorbar(x, means, yerr=stds, fmt='-o', capsize=3)
ax.set_xlabel('Index')
ax.set_ylabel('Value')
ax.set_title('Error Bar Plot')
plt.show()
