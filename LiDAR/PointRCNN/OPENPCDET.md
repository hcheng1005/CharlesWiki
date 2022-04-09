## OpenPCDET

### **相关组件**
- **CUDA**
    > wget https://developer.download.nvidia.com/compute/cuda/11.1.0/local_installers/cuda_11.1.0_455.23.05_linux.run
    sudo sh cuda_11.1.0_455.23.05_linux.run

---
- **torch**
    > 1. https://pytorch.org/get-started/previous-versions/
    > 2. 根据所需版本自行安装
---
- **torch_scatter** 
    > 1. https://data.pyg.org/whl/
    > 2. 根据当前torch版本和cuda版本下载对应的版本
---
·


### KITTI
```python
python demo.py  --cfg_file ${model_path} 
                --ckpt ${ckeckpoint_path} 
                --data_path ${data_path}
```

### nuScenes
