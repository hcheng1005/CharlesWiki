# SimpleTrack

<p align="center">
  <img src="simpletrack_gif.gif" width="100%">
</p>

### [论文]()
### [源码](https://github.com/TuSimple/SimpleTrack)
### [代码解析](simpleTrack_code.md)
---

## **论文解析**

### **1. Pre-processing of Input Detections**
<p align="center">
  <img src="p1.png" width="60%">
</p>

如果对输入的boundingBoxd一视同仁，可能会降低关联正确性。

因此作者做了一些改进，对输入的检测进行***NMS***[1](https://zhuanlan.zhihu.com/p/78504109)|[2](https://www.cnblogs.com/zf-blog/p/8532228.html)处理。

**NMS效果⬇**

<p align="center">
  <img src="p2.png" width="60%">
</p>


```
对于传统的score filter方法来说，设置删除门限0.24，可以看出，第一行的三个检测目标【0.12， 0.13 0.16】均低于0.24，因此全部被误删除；

若使用NMS方法，可以看出检测均被有效保留，且第二行的【0.24 0.10】也能被正常过滤，仅保留0.47这一个检测目标。
```
---

### **2. Motion Model**

<p align="center">
  <img src="p3.png" width="60%">
</p>       

---
### **3. Association**
<p align="center">
  <img src="p4.png" width="60%">
</p>

*这里提到：*
1. AB3DMOT用的是IoU关联以及标准卡尔曼滤波；
2. Chiu用的是Mahalanobis统计以及[GreedyMatch贪心匹配]()；
3. CenterPoint用的是L2 distance；
---
### **4. 3D GIoU(TBD)**

<p align="center">
  <img src="p5.png" width="60%">
</p>


<p align="center">
  <img src="p6.png" width="60%">
</p>

```
intersection：相交（十字路口）
union：联合
convexhull：凸包
polygon: n.多边形; 多角形
```
---
### **5. Matching Strategies**
**总体来说，两种方法：**
- 二分图-[匈牙利匹配](https://www.notion.so/charles-hao/Hungarian-f0cbbb77545d49409943d49b58794c5e)(Or [KM](https://www.notion.so/charles-hao/Kuhn-Munkres-9f33c884daea404f9dc74b755a4f7038))
- 迭代匹配最近-[贪心算法](./GreedyMatch.md)
