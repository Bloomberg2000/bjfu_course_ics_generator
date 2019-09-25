# bjfu_course_ics_generator(爬虫版)

## 项目简介

* 获取北京林业大学[教务系统](http://newjwxt.bjfu.edu.cn/)课程表，并导出iCalander（.ics）文件

## 重要提示⚠️
* [已解决✅]~~若您运行程序过程中出现如下错误，表示您的课表中可能包含，缺少老师/周次/教室的课程，这种情况爬虫版并未支持。您可以联系作者，获取API版源代码~~
* **该版本为爬虫版本（相较API版查询速度较慢），API版由于明显的隐私问题已停止开源，若您需要API版本请联系作者本人**
* 😊

## 注意事项

* 本程序需要计算机可以正常访问北京林业大学[教务系统](http://newjwxt.bjfu.edu.cn/)
* 当教务系统由于某些原因无法访问时，请尝试如下操作
  * 使用校园内部网络如`bjfu_wifi`、或直连网线
  * 无法使用校园内部网络时，使用[北京林业大学](http://vpn.bjfu.edu.cn/)VPN客户端执行导入操作
    * Pulse Secure（VPN客户端）下载
      * [Windows 32位](http://trial.pulsesecure.net/clients/ps-pulse-win-9.0r4.0-b1731-32bitinstaller.msi)
      * [Windows 64位](http://trial.pulsesecure.net/clients/ps-pulse-win-9.0r4.0-b1731-64bitinstaller.msi)
      * [macOS](http://trial.pulsesecure.net/clients/ps-pulse-mac-9.0r4.0-b1731-installer.dmg)
      * [Ubuntu/Debian 64 Bit](http://trial.pulsesecure.net/clients/ps-pulse-linux-9.0r4.0-b943-ubuntu-debian-64-bit-installer.deb)
      * [CentOS/RHEL 64 Bit](http://trial.pulsesecure.net/clients/ps-pulse-linux-9.0r4.0-b943-centos-rhel-64-bit-installer.rpm) 
      * [iOS](https://itunes.apple.com/app/pulse-secure/id945832041)
      * [Android(需要科学上网)](https://play.google.com/store/apps/details?id=net.pulsesecure.pulsesecure&hl=en)


## 如何使用

```bash
pip3 install requests
pip3 install bs4
pip3 install lxml
cd /path/to/bjfu_course_ics_generator
python3 main.py
```

## 运行过程

```bash
/path/to/bjfu_course_ics_generator  master ✗                                                                                      
▶ python3 main.py 
欢迎使用课程表生成工具。
请输入北京林业大学学号(如：171001101): 171101215
请输入教务系统密码: 
请设置第一周的星期一日期(如：20190902): 20190902
正在配置提醒功能
【0】不提醒
【1】上课前 10 分钟提醒
【2】上课前 30 分钟提醒
【3】上课前 1 小时提醒
【4】上课前 2 小时提醒
【5】上课前 1 天提醒
请输入数字选择提醒时间: 3
```

## 其他学校适配

* 仅需修改`bjfu_util.py`中

  ```python
  def get_course_list(stu_code):
    # TODO
    return format_course_data(json.loads(data))
    
  def format_course_data(class_json):
    # TODO
    return json
  ```

  使之返回如下格式的`json`数据，即可

  ```json
  {
      "className": "课程名",
      "weekday": 1, // 星期（1-7）
      "classroom": "教室名",
      "teacherName":  "教师名",
      "startTime": "0800", // 上课时间 08:00
      "endTime": "0845", // 下课时间 08:45
      "week": {
          "startWeek": 1, // 起始周
          "endWeek": 8 // 结束周
      }
  }
  ```

## 导入课程表

> 强烈建议您使用云账户导入，便于多设备/多平台同步信息

> 代码运行结束后会在bjfu_course_ics_generator根目录下生成`学号.ics`

### 导入iOS & watchOS

- 由于系统设置的原因，iOS系统无法直接导入`ics`文件

- 如果你是macOS用户，请参见`导入macOS`，在`iCloud`账户中创建日历

- 如果你是Windows用户

  - 使用[iCloud桌面程序](https://support.apple.com/zh-cn/HT204283)然后导入日历

    ![Windows ç iCloud](https://tva1.sinaimg.cn/large/006y8mN6ly1g79uq4wkfmj30rs0ik78y.jpg)

  - 或参见`导入日历管理工具（Outlook，Google）`，在iOS设备中登录账户

    1. 打开设置

       ![IMG_8751](https://tva1.sinaimg.cn/large/006y8mN6ly1g79ukj8c89j30u01szdrm.jpg)

    2. 点击密码与账户
  
       ![IMG_8752](https://tva1.sinaimg.cn/large/006y8mN6ly1g79ukwcdzjj30u01szalk.jpg)
  
    3. 选择对应的账户并登录![IMG_8753](https://tva1.sinaimg.cn/large/006y8mN6ly1g79uld55hzj30u01sz7hg.jpg)

### 导入Android

1. 使用微信或其他文件管理工具将`ics`文件拷贝到手机中
2. 在文件管理器中点击`ics`文件![SmartSelect_20190923-214306_My Files](https://tva1.sinaimg.cn/large/006y8mN6ly1g79scicujsj313x0c2myb.jpg)

3. 在弹出窗口中选择`日历`（或其他日历软件）

   ![SmartSelect_20190923-214325_Android System](https://tva1.sinaimg.cn/large/006y8mN6ly1g79sd2d86aj31400sy0vz.jpg)

4. 预览日历内容后点击`保存`

   ![SmartSelect_20190923-214358_Calendar](https://tva1.sinaimg.cn/large/006y8mN6ly1g79sdr9b4vj31400ri76y.jpg)

5. 课程导入完毕

   ![SmartSelect_20190923-214438_Calendar](https://tva1.sinaimg.cn/large/006y8mN6ly1g79se0ogjdj30u01fltl0.jpg)

### 导入macOS

1. 在`日历`（或其他日历软件）中点击`文件` `导入`，或直接双击`ics`文件![屏幕快照 2019-09-23 21.27.49](https://tva1.sinaimg.cn/large/006y8mN6ly1g79ruwcdgpj31eb0u0qq5.jpg)

2. 选择生成的`ics`文件

   ![屏幕快照 2019-09-23 21.28.00](https://tva1.sinaimg.cn/large/006y8mN6ly1g79rw4gk8yj31ct0u0qhj.jpg)

3. 选择目标日历![屏幕快照 2019-09-23 21.28.13](https://tva1.sinaimg.cn/large/006y8mN6ly1g79rwlpxptj30vu0fiaf4.jpg)

4. 课程导入完毕

   ![屏幕快照 2019-09-23 21.45.10](https://tva1.sinaimg.cn/large/006y8mN6ly1g79sc1jq9rj315u0u04qp.jpg)

### 导入Windows 10

1. 在文件资源管理器中找到生成的`ics`文件，双击打开

   ![屏幕快照 2019-09-23 21.49.12](https://tva1.sinaimg.cn/large/006y8mN6ly1g79shyhoqjj30om08kq3n.jpg)

2. 选择`日历`（或其他日历软件）

   ![屏幕快照 2019-09-23 21.49.20](https://tva1.sinaimg.cn/large/006y8mN6ly1g79sk4r2uvj30li0t940j.jpg)

3. 预览日历内容后点击`添加到日历`![批注 2019-09-23 214954](https://tva1.sinaimg.cn/large/006y8mN6ly1g79spw42abj312n0u04bw.jpg)

4. 课程导入完毕

   ![批注 2019-09-23 215504](https://tva1.sinaimg.cn/large/006y8mN6ly1g79sptq7bnj312n0u04bw.jpg)

### 导入日历管理工具（Outlook，Google）

* iCalendar是日历数据交换”的标准数据格式（RFC 5545），具有非常好的兼容性，兼容几乎所有的日程管理工具，您可以自行搜索`XX如何导入ics`获取相关信息

## 鸣谢

* 感谢[LiuZhongyu](https://github.com/qaqslzy)提供的爬虫技术支持
* 感谢界面友好，功能齐全的一站式北林服务小程序`北林派`的开发者提供的接口获取思路（API版本）

  >北林派可能是北京林业大学最好的信息查询平台，拥有
  >
  >* 查询课表
  >* 查询成绩
  >* 查询阳光长跑
  >* 查询校历
  >* 教学评价
  >* 信息发布墙
  >
  >等丰富的功能，推荐北京林业大学的同学们扫码体验！

  

  ![IMG_8755](https://tva1.sinaimg.cn/large/006y8mN6ly1g79ussz6ugj30u00u0adi.jpg)

