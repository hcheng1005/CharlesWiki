## Key Words
- greedy match
- GIOU
- NMS
- KF
---


### **MOT-Model**
```yml
running:
  covariance: default
  score_threshold: 0.7
  max_age_since_update: 2
  min_hits_to_birth: 3
  match_type: greedy  # 贪心匹配算法 也可以是bipartite（匈牙利orKM分配）
  asso: giou          # 关联分计算算法GIOU
  has_velo: false
  motion_model: kf
  asso_thres:
    iou: 0.9
    giou: 1.5

redundancy:
  mode: mm
  det_score_threshold: 
    iou: 0.1
    giou: 0.1
  det_dist_threshold: 
    iou: 0.1
    giou: -0.5

data_loader:
  pc: true
  nms: true
  nms_thres: 0.25   # NMS阈值
```


---
### **跟踪入口**
```python
# real mot happens here
ids, bboxes, states, types = sequence_mot(configs, data_loader, file_index, gt_bboxes, gt_ids, args.visualize)
```
>其中：f**ile_index是文件个数，也就是frame帧数**，由数据集大小决定。
---


### **跟踪算法主体**
```python
def sequence_mot(configs, data_loader: WaymoLoader, sequence_id, gt_bboxes=None, gt_ids=None, visualize=False):
    tracker = MOTModel(configs) #定义跟踪模型、滤波器以及参数定义和初始化
    frame_num = len(data_loader)
    IDs, bboxes, states, types = list(), list(), list(), list()
    for frame_index in range(data_loader.cur_frame, frame_num):
        ···
        ···
        # mot
        results = tracker.frame_mot(frame_data)
        ···
        ···
    return IDs, bboxes, states, types
```
---


### **单帧MOT主体 frame_mot**
```python
def frame_mot(self, input_data: FrameData):
    """ For each frame input, generate the latest mot results
    Args:
        input_data (FrameData): input data, 
        including detection bboxes and ego information
    Returns:
        tracks on this frame: [(bbox0, id0), (bbox1, id1), ...]
    """
```