# 3DMOT总结

## **前言**
**检测框架：**[OPENPCDET](LiDAR/PointRCNN/OPENPCDET.md)

**数据集：** nuScenes

**检测网络：**[CenterPoint](LiDAR/CenterPoint/Center_based_3D_Object_Detection_and_Tracking.pdf)

---

## 跟踪框架介绍

### **基本参数**

- **Dets：**
    ```python
    [x, y, z, o, l, w, h, s]
    # o代表目标航向角；
    # s代表该det的score，有些检测模型可能不支持该参数
    ```

- **Trace：**
    ```python
    [x, y, z, o, l, w, h, vx, vy, vz]
    # o代表目标航向角；
    ```

- **机动模型：** CT
    ```python
    # state transition matrix
    self.kf.F = np.array([[1,0,0,0,0,0,0,time_lag,0,0],      
                            [0,1,0,0,0,0,0,0,time_lag,0],
                            [0,0,1,0,0,0,0,0,0,time_lag],
                            [0,0,0,1,0,0,0,0,0,0],  
                            [0,0,0,0,1,0,0,0,0,0],
                            [0,0,0,0,0,1,0,0,0,0],
                            [0,0,0,0,0,0,1,0,0,0],
                            [0,0,0,0,0,0,0,1,0,0],
                            [0,0,0,0,0,0,0,0,1,0],
                            [0,0,0,0,0,0,0,0,0,1]])    

    # measurement function,
    self.kf.H = np.array([[1,0,0,0,0,0,0,0,0,0],      
                            [0,1,0,0,0,0,0,0,0,0],
                            [0,0,1,0,0,0,0,0,0,0],
                            [0,0,0,1,0,0,0,0,0,0],
                            [0,0,0,0,1,0,0,0,0,0],
                            [0,0,0,0,0,1,0,0,0,0],
                            [0,0,0,0,0,0,1,0,0,0]])
    ```

### **跟踪流程**

### **1. 状态预测**
None

### **2. 航迹关联**

#### **2.1 trk-det匹配分计算**

根据不同的匹配算法决定不同的匹配分计算方式

```python
# associate the tracks with detections
if mode == 'bipartite':  #匈牙利算法 or KM分配算法
    matched_indices, dist_matrix = \
        bipartite_matcher(dets, tracks, asso, dist_threshold, trk_innovation_matrix)
elif mode == 'greedy': #贪心匹配
    matched_indices, dist_matrix = \
        greedy_matcher(dets, tracks, asso, dist_threshold, trk_innovation_matrix)
```

- **匹配分计算**
    - [欧氏距离](https://blog.csdn.net/mousever/article/details/45967643)
    - [马氏距离](https://blog.csdn.net/mousever/article/details/45967643)
    - [曼哈顿距离](https://blog.csdn.net/mousever/article/details/45967643)
    - [GIOU](common/IOU.md)
    - [IOU](common/IOU.md)


```python
    def bipartite_matcher(dets, tracks, asso, dist_threshold, trk_innovation_matrix):
    if asso == 'iou':
        dist_matrix = compute_iou_distance(dets, tracks, asso)
    elif asso == 'giou':
        dist_matrix = compute_iou_distance(dets, tracks, asso)
    elif asso == 'm_dis': # 马氏距离
        dist_matrix = compute_m_distance(dets, tracks, trk_innovation_matrix)
    elif asso == 'euler': # 欧氏距离
        dist_matrix = compute_m_distance(dets, tracks, None)
```

#### **2.2 匹配算法**

- **匈牙利匹配**
```python
    # 解线性分配
    row_ind, col_ind = linear_sum_assignment(dist_matrix)  
    matched_indices = np.stack([row_ind, col_ind], axis=1)
    return matched_indices, dist_matrix
```

- **贪心匹配** [refer](https://github.com/eddyhkchiu/mahalanobis_3d_multi_object_tracking/blob/master/main.py)
```python
    # association in the greedy manner
    # refer to 

    distance_1d = distance_matrix.reshape(-1)

    #排序：从小到大->索引号
    index_1d = np.argsort(distance_1d) 

    #巧妙的处理，能够得出dets-trace的对应关系
    index_2d = np.stack([index_1d // num_trks, index_1d % num_trks], axis=1)  
    detection_id_matches_to_tracking_id = [-1] * num_dets
    tracking_id_matches_to_detection_id = [-1] * num_trks

    for sort_i in range(index_2d.shape[0]):
        detection_id = int(index_2d[sort_i][0])
        tracking_id = int(index_2d[sort_i][1])
        if tracking_id_matches_to_detection_id[tracking_id] == -1 and detection_id_matches_to_tracking_id[detection_id] == -1:

            tracking_id_matches_to_detection_id[tracking_id] = detection_id
            detection_id_matches_to_tracking_id[detection_id] = tracking_id
            matched_indices.append([detection_id, tracking_id])

    if len(matched_indices) == 0:
        matched_indices = np.empty((0, 2))
    else:
        matched_indices = np.asarray(matched_indices)
```

### 3. 状态更新

标准的卡尔曼更新步骤。

量测状态矩阵：[x, y, z, o, l, w, h, s]

### 4. 航迹管理

None