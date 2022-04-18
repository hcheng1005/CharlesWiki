import matplotlib.pyplot as plt
from numpy import *
import numpy as np
import operator as op


class Ransac:
    weight = 0.
    bias = 0.

    def least_square(self, samples):
        # 最小二乘法
        x = samples[:, 0]
        y = samples[:, 1]
        x_ = 0
        y_ = 0
        x_mul_y = 0
        x_2 = 0
        n = len(x)
        for i in range(n):
            x_ = x[i] + x_
            y_ = y[i] + y_
            x_mul_y = x[i] * y[i] + x_mul_y
            x_2 = x[i] * x[i] + x_2
        x_ = x_ / n
        y_ = y_ / n
        weight = (x_mul_y - n * x_ * y_) / (x_2 - n * x_ * x_)
        bias = y_ - weight * x_
        return weight, bias

    def isRepeat(self, sour, tar):
        # 判断是否含有重复样本
        for i in range(len(sour)):
            if (op.eq(list(sour[i]), list(tar))):
                return True
        return False

    def random_samples(self, samples, points_ratio):
        # 随机采样（无重复样本）
        number = len(samples)
        inliers_num = int(number * points_ratio)
        inliers = []
        outliers = []
        cur_num = 0
        while cur_num != inliers_num:
            seed = np.random.randint(0, number)
            sap_cur = samples[seed]
            if not self.isRepeat(inliers, sap_cur):
                cur_num = cur_num + 1
                inliers.append(list(sap_cur))
        for i in range(number):
            if not self.isRepeat(inliers, samples[i]):
                outliers.append(list(samples[i]))
        return np.array(inliers), np.array(outliers)

    def fun_plot(self, sample, w, b):
        data_x = np.linspace(-50, 50, 50)
        data_y = [w * x + b for x in data_x]
        plt.ion()
        plt.plot(data_x, data_y, 'r')
        plt.plot(sample[:, 0], sample[:, 1], 'bo')
        plt.show()
        plt.pause(0.001)
        plt.clf()

    def ransac(self, samples, points_ratio=0.3, epoch=5, reject_dis=0.5, inliers_ratio=0.3):
        # samples 输入样本，形如 [[x1 ,yi],[x2, y2]]
        # point_ratio  随机选择样本点的比例
        # epoch    迭代轮数
        # reject_dis  小于此阈值将outliers加入inliers
        # inliers_ratio  有效inliers最低比例

        inliers_num_cur = 0
        for i in range(epoch):

            inliers, outliers = self.random_samples(samples, points_ratio)

            # plt.figure(1)
            # plt.ion()
            # plt.plot(inliers[:, 0], inliers[:, 1], 'bo', markersize=3)
            # plt.plot(outliers[:, 0], outliers[:, 1], 'ro', markersize=3)
            # plt.show()
            # plt.pause(0.05)
            # plt.clf()

            weight_cur, bias_cur = self.least_square(inliers)

            # self.fun_plot(samples,weight_cur,bias_cur)
            for j in range(len(outliers)):
                distance = np.abs(
                    (weight_cur * outliers[j, 0] + bias_cur) - outliers[j, 1]) / np.sqrt(np.power(weight_cur, 2)+1)
                if distance <= reject_dis:
                    inliers = np.vstack((inliers, outliers[j]))
            weight_cur, bias_cur = self.least_square(inliers)
            # self.fun_plot(samples,weight_cur,bias_cur)

            if len(inliers) >= len(samples) * inliers_ratio:
                if len(inliers) > inliers_num_cur:
                    self.weight = weight_cur
                    self.bias = bias_cur
                    inliers_num_cur = len(inliers)



def dis_vec(a,b):    # 计算两个向量的距离
 
    if len(a)!=len(b):
        return Exception
    else:
        return np.sqrt(np.sum(np.square(a-b)))
  
 
def dbscan(s, minpts):   # 密度聚类
 
    center_points = []   # 存放最终的聚类结果
    k = 0  # 检验是否进行了合并过程
 
    for i in range(n):
        if sum(dis[i] <= s) >= minpts:   # 查看距离矩阵的第i行是否满足条件
            if len(center_points) == 0:  # 如果列表长为0，则直接将生成的列表加入
                center_points.append(list(all_index[dis[i] <= s]))
            else:
                for j in range(len(center_points)):   # 查找是否有重复的元素
                    if set(all_index[dis[i] <= s]) & set(center_points[j]):
                        center_points[j].extend(list(all_index[dis[i] <= s]))
                        k=1   # 执行了合并操作
                if k==0 :
                    center_points.append(list(all_index[dis[i] <= s]))  # 没有执行合并说明这个类别单独加入
                k=0
 
    lenc =  len(center_points)
 
    # 以下这段代码是进一步查重，center_points中所有的列表并非完全独立，还有很多重复
    # 那么为何上面代码已经查重了，这里还需查重，其实可以将上面的步骤统一放到这里，但是时空复杂的太高
    # 经过第一步查重后，center_points中的元素数目大大减少，此时进行查重更快！
    k = 0
    for i in range(lenc-1):
        for j in range(i+1, lenc):
            if set(center_points[i]) & set(center_points[j]):
                center_points[j].extend(center_points[i])
                center_points[j] = list(set(center_points[j]))
                k=1
 
        if k == 1:
            center_points[i] = []   # 合并后的列表置空
        k = 0
 
    center_points = [s for s in center_points if s != []]   # 删掉空列表即为最终结果
 
    return center_points



test = Ransac()
points = np.fromfile('./testData', dtype=np.float32, count=-1).reshape([-1, 4])
sample = points[:, :2]

newPoint = []
for i in range(sample.shape[0]):
    if (abs(points[i, 0]) < 15) and (abs(points[i, 1]) < 60):
        newPoint.append(points[i, :])

data = np.array(newPoint)
data = data[:,:2]

# DBSCAN
n,m = data.shape
all_index = np.arange(n)
dis = np.zeros([n,n])

for i in range(n):   # 计算距离矩阵
    for j in range(i):
        dis[i,j] = dis_vec(data[i],data[j])
        dis[j,i] = dis[i,j]
center_points = dbscan(5,3)  # 半径和元素数目
c_n = center_points.__len__()   # 聚类完成后的类别数目
print (c_n)
ct_point = []
color = ['g','r','b','m','k']
noise_point = np.arange(n)      # 没有参与聚类的点即为噪声点    
    
for i in range(c_n):
    ct_point = list(set(center_points[i]))
    plt.scatter(data[ct_point,0], data[ct_point,1], color=color[i])       # 画出不同类别的点
    # X = np.vstack((data[ct_point,0], np.ones((len(ct_point))))).T
    # Y = data[ct_point,1].reshape(-1,1)
    # w = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(Y)
    # # print(w)
    # xin = np.linspace(-20, 20)
    # yin = w[0]*xin + w[1]
    # plt.plot(xin, yin, 'b-.')
    
    sample = data[ct_point,:]
    test.ransac(sample)
    data_x = np.linspace(-20, 20, 50)
    data_y = [test.weight * x + test.bias for x in data_x]
    plt.plot(data_x, data_y, 'b-.')
    
    #LeastSquare
    
plt.show()


# test.ransac(sample)
# print(test.weight)
# data_x = np.linspace(-20, 20, 50)
# data_y = [test.weight * x + test.bias for x in data_x]

# plt.figure(2)
# plt.plot(sample[:, 0], sample[:, 1], 'bo')
# plt.plot(data_x, data_y, 'r')
# plt.show()
# plt.pause(5)
