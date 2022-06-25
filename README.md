# -智能远程视频监控
**毕设项目：**

本系统以树莓派3B+为嵌入式计算平台，与CSI摄像头、二自由度旋转云台结合，主体使用Python和PHP编程，应用I2C通信与OpenCV等前沿技术，通过Frp内网穿透打通内外网数据传输，实现具有远程实时视频监控、运动检测及画面截图邮件预警、远程控制云台摄像头转动、监控画面截取及视频录制、Web端在线预览视频/图片、下载或删除文件等功能的远程流媒体传输系统。

------
**配置方法：**

主要是环境配置和内网穿透，网上查阅资料配置即可，原先的文件个人信息比较多就不展示了，这里很感谢同济子豪兄的树莓派帖子。代码详情见运动检测模式和云台监控模式两个文件夹，程序已经部署好了，注意的是两种模式均可开启摄像头，在某一种模式下开启摄像头后，要想开启另一种模式的摄像头，要先关闭之前模式的摄像头否则会冲突，页面会弹出报错信息，系统程序没有崩，用户体验不佳而已，重新刷新下页面，再开启摄像头即可，当时因为毕设时间不足和能力有限，暂时没有想到处理冲突的办法，刷新一下即可。

![image](https://user-images.githubusercontent.com/40397845/175769585-2e6643b0-f176-4eb7-aebf-24b1176063a6.png)

![image](https://user-images.githubusercontent.com/40397845/175769607-ee7b269f-66e2-4314-94b4-a1e1e9a30cf8.png)

![image](https://user-images.githubusercontent.com/40397845/175769622-66d94f55-0c1c-4180-8387-dab228b133b6.png)

![image](https://user-images.githubusercontent.com/40397845/175769670-d561bddc-0e63-4895-a171-9b4ef1c5bc81.png)


------
**成品图：**

![9A{W4(PMFCX9G~6}47V@IE5](https://user-images.githubusercontent.com/40397845/175769281-47712151-1897-4943-b4bd-3cb652678938.jpg)

**云台控制模式：**

![image](https://user-images.githubusercontent.com/40397845/175769393-79911012-1ca9-4529-b990-ded63692deb6.png)

**运动检测模式：**

![image](https://user-images.githubusercontent.com/40397845/175769427-defcd6ca-35df-49c4-84ff-8de1171434c4.png)


