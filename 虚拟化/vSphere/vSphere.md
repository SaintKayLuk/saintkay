## 两个核心组件

* ESXi
* vCenter Server


- 一个基础 hypervisor，即 vSphere ESXi，安装在每个物理服务器中用于托管虚拟机。
- 一个管理服务器实例，即 vCenter Server，用于集中管理多个 vSphere 主机。




## 许可证

vCenter Server 6 许可证
```
HG612-FH19H-08DL1-V19X2-1VKND
NU4JA-4V2DQ-48428-T32GK-8VRN4
0Y4H2-8P217-H8900-M8AE4-2LH44
NA658-2308J-08809-93AQ6-278J0
```


ESXI 6 许可证
```
HV4WC-01087-1ZJ48-031XP-9A843
```
---



---

VMware vCenter 7.0 Standard
```
104HH-D4343-07879-MV08K-2D2H2
410NA-DW28H-H74K1-ZK882-948L4
406DK-FWHEH-075K8-XAC06-0JH08
```
VMware vSphere ESXi 7.0 Enterprise Plus
```
JJ2WR-25L9P-H71A8-6J20P-C0K3F
HN2X0-0DH5M-M78Q1-780HH-CN214
JH09A-2YL84-M7EC8-FL0K2-3N2J2
```

---

vSphere 8 Enterprise Plus 许可证
```
4V492-44210-48830-931GK-2PRJ4
```
vCenter Server 8 Standard 许可证
```
0Z20K-07JEH-08030-908EP-1CUK4
0F41K-0MJ4H-M88U1-0C3N0-0A214
4F282-0MLD2-M8869-T89G0-CF240
```

## esxi 安装vmtoos

1. 先挂载cdrom，(页面操作)

2. 然后进入虚拟机挂载(只读模式)
```
mkdir /mnt/cdrom
mount /dev/cdrom /mnt/cdrom
```
3. 安装依赖
```
yum install -y perl gcc kernel-devel
```
4. 安装vmtools
```
cd /mnt
cp  /mnt/cdrom/VMwareTools-10.2.0-7253323.tar.gz .
tar -zxvf VMwareTools-10.2.0-7253323.tar.gz
./vmware-tools-distrib/vmware-install.pl
```
第一个yes，后面全都回车
```
open-vm-tools packages are available from the OS vendor and VMware recommends 
using open-vm-tools packages. See http://kb.vmware.com/kb/2073803 for more 
information.
Do you still want to proceed with this installation? [no] yes
```




