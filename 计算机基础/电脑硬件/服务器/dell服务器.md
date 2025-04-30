* ACHI MODE：识别为单块硬盘
* RAID MODE：使用raid模式


BIOS里设置 SATA为 RAID MODE

某些阵列卡里自带的模式，可以不需要BIOS里设置



## raid问题

硬盘显示 foreign (外来)

1. 重启
2. ctrl + R 进入阵列卡界面
3. ctrl + n 到 **foreign view** 页面
4. 光标位于第一行，阵列卡那行，然后按 F2 弹出选项，这里有2个选项，clear和import
   1. clear：清楚外部配置，会清空数据
   2. import：导入外部配置，如果原有raid正常，则导入后正常
