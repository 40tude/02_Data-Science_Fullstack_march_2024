# Configure NVDIA performance counters

<p align="center">
<img src="./assets/gpu_wsl/09_nvidia_dev.png" alt="drawing" width="800"/>
<p>

<p align="center">
<img src="./assets/gpu_wsl/10_nvidia_counter.png" alt="drawing" width="800"/>
<p>

# Install Powershell (<> Windows Powershell)

* https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.4
* Open a Windows Powershell terminal

``winget install --id Microsoft.PowerShell --source winget``

* Close the Windows Powershell terminal
* Open a Powershell terminal 


# Install WSL

 * https://learn.microsoft.com/en-us/windows/wsl/install

```
wsl --install
wsl -l -v       # to check what is running
```

<p align="center">
<img src="./assets/gpu_wsl/02_list_distrib.png" alt="drawing" width="800"/>
<p>

* You may want to uninstall Unbuntu and start a fresh installation 
    * Yes you can have multiple instances of Ubuntu but this is not the point here

``wsl --unregister Ubuntu``

<p align="center">
<img src="./assets/gpu_wsl/03_uninstall_ubuntu.png" alt="drawing" width="800"/>
<p>



# Install VSCode WSL Extension

* Open a Powershell terminal
* Launch VSCode
* Look for and install WSL Extension
* Leave VSCode

<p align="center">
<img src="./assets/gpu_wsl/08_wsl_extension.png" alt="drawing" width="800"/>
<p>

* From the command line one could use :
```
code --list-extensions
code --install-extension ms-vscode-remote.remote-wsl
# code --uninstall-extension ms-vscode.csharp
```




# Install Ubuntu

```
wsl --install -d Ubuntu
```

<p align="center">
<img src="./assets/gpu_wsl/01_install_ubuntu.png" alt="drawing" width="800"/>
<p>

* Double check the prompt ending with `$`
* Leave the session (`exit`)




## Test Ubuntu

* Restart a session and leave it


```
wsl -d Ubuntu
exit
```

<p align="center">
<img src="./assets/gpu_wsl/04_run_ubuntu.png" alt="drawing" width="800"/>
<p>





# Install CUDA under Unbuntu

* Start a session

```
wsl -d Ubuntu
sudo apt update && sudo apt upgrade
sudo apt install gcc --fix-missing
sudo apt install nvidia-cuda-toolkit
```
<p align="center">
<img src="./assets/gpu_wsl/05_gcc.png" alt="drawing" width="800"/>
<p>


## Testing

```
nvidia-smi
```
<p align="center">
<img src="./assets/gpu_wsl/06_nvidia_smi.png" alt="drawing" width="800"/>
<p>




```
nvcc -V
```
<p align="center">
<img src="./assets/gpu_wsl/07_nvcc.png" alt="drawing" width="800"/>
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