# Install Powershell
``winget install --id Microsoft.PowerShell --source winget``

<p align="center">
<img src="./assets/gpu_wsl/01_install_ubuntu.png" alt="drawing" width="800"/>
<p>

# Install WSL
https://learn.microsoft.com/en-us/windows/wsl/install

```
wsl --install
wsl -l -v       # to check what is running
```

<p align="center">
<img src="./assets/gpu_wsl/02_list_distrib.png" alt="drawing" width="800"/>
<p>

``wsl --unregister Ubuntu``

<p align="center">
<img src="./assets/gpu_wsl/03_uninstall_ubuntu.png" alt="drawing" width="800"/>
<p>

```
wsl -d Ubuntu

exit
```

<p align="center">
<img src="./assets/gpu_wsl/04_run_ubuntu.png" alt="drawing" width="800"/>
<p>





# Install CUDA


```
wsl -d Ubuntu
sudo apt update && sudo apt upgrade
sudo apt install gcc --fix-missing
sudo apt install nvidia-cuda-toolkit
```
<p align="center">
<img src="./assets/gpu_wsl/05_gcc.png" alt="drawing" width="800"/>
<p>


```
nvidia-smi
```
<p align="center">
<img src="./assets/gpu_wsl/06_nvidia_smi.png" alt="drawing" width="800"/>
<p>




```
nvcc
```
<p align="center">
<img src="./assets/gpu_wsl/07_nvcc.png" alt="drawing" width="800"/>
<p>


# Install VSCode WSL Extension

<p align="center">
<img src="./assets/gpu_wsl/08_wsl_extension.png" alt="drawing" width="800"/>
<p>

```
code --list-extensions
code --install-extension ms-vscode-remote.remote-wsl
# code --uninstall-extension ms-vscode.csharp
```

# Config NVDIA

<p align="center">
<img src="./assets/gpu_wsl/09_nvidia_dev.png" alt="drawing" width="800"/>
<p>

<p align="center">
<img src="./assets/gpu_wsl/10_nvidia_counter.png" alt="drawing" width="800"/>
<p>


# Sample code

<p align="center">
<img src="./assets/gpu_wsl/11_ubuntu_terminal.png" alt="drawing" width="800"/>
<p>

```
cd /mnt/c/Users/phili/OneDrive/Documents/Programmation/Formations_JEDHA/02_Data_Science_Fullstack_march_2024H 

code .

```


<p align="center">
<img src="./assets/gpu_wsl/12_install_python.png" alt="drawing" width="800"/>
<p>


```
print("Hello")
```

<p align="center">
<img src="./assets/gpu_wsl/13_test01.png" alt="drawing" width="800"/>
<p>



<p align="center">
<img src="./assets/gpu_wsl/14_test01_run.png" alt="drawing" width="800"/>
<p>

```
sudo apt install python3-pip
```


```
pip install torch
```

<p align="center">
<img src="./assets/gpu_wsl/15_install_torch.png" alt="drawing" width="800"/>
<p>


```python
import torch

if torch.cuda.is_available():
    device = torch.device("cuda")
else:    
    device = torch.device("cpu")

print(f"Using device : {device}")
```

<p align="center">
<img src="./assets/gpu_wsl/16_test02.png" alt="drawing" width="800"/>
<p>

```
pip install numpy==1.26.4
pip install scipy==1.14.1
pip install scikit-learn==1.3.1
```


# Run Bert
Open 03_bert_01.ipynb
Let VSCode install Jupyter extension
pip install tensorflow==2.17.0
pip install pandas, matplotlib, tensorflow, transformers, tf_keras, scikit-learn