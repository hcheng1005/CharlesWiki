## 安装NVIDIA驱动

### **查看系统适用的驱动版本**
```
ubuntu-drivers devices
```

### **使用ubuntu-drivers自动下载驱动**
```
sudo ubuntu-drivers autoinstall
```
或者自行选择驱动下载
```
sudo apt install nvidia-driver-455
```

### **GPU Version Pytorch**
```
pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio===0.7.2 -f https://download.pytorch.org/whl/torch_stable.html
```

### **更新nvcc路径**
```
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

### **其他**
- [Spconv](Spconv_README.md)