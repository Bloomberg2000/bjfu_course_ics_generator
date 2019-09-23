# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import re


def format_course_data(infomation, course_index, week_day):
    if infomation.text == '\xa0':
        return None
    else:
        course_list = []
        index = 0
        # 每个课程长度为 8
        # 处理同一表格多课程
        while index + 8 <= len(infomation):
            course_list += create_course(infomation.contents[index: index + 8], course_index, week_day)
            # 课程分隔符长度为2 ['---------------------', <br/>]
            index += 8 + 2
        return course_list


def create_course(information, course_index, weekday):
    """[
     0 '计算机网络A(必修)',
     1 <br/>,
     2 <font title="老师">曹佳</font>,
     3 <br/>,
     4 <font title="周次(节次)">2-4,6-10(周)</font>,
     5 <br/>,
     6 <font title="教室">二教306</font>,
     7 <br/>
     ]
    """
    course_list = []
    class_weeks = information[4].text.replace('(周)', '').split(",")
    for week in class_weeks:
        startWeek = endWeek = 0
        if '-' in week:
            week = week.split('-')
            startWeek = int(week[0])
            endWeek = int(week[1])
        else:
            startWeek = endWeek = int(week)
        class_dict = {
            "className": information[0],
            "weekday": weekday,
            "classroom": information[6].text,
            "teacherName": information[2].text,
            "startTime": get_start_time(course_index),
            "endTime": get_end_time(course_index),
            "week": {
                "startWeek": startWeek,
                "endWeek": endWeek
            }
        }
        course_list.append(class_dict)
    return course_list


def get_course_list(user_id, password):
    headers = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
        'Connection': 'Keep-Alive',
    }

    login_url = 'http://newjwxt.bjfu.edu.cn/jsxsd/xk/LoginToXk'
    kb_url = 'http://newjwxt.bjfu.edu.cn/jsxsd/xskb/xskb_list.do'
    studentId = user_id
    password = password
    result = requests.post(login_url, data={"USERNAME": studentId, "PASSWORD": password}, allow_redirects=False)
    headers['Cookie'] = result.headers['Set-Cookie']

    all_class = requests.get(kb_url, headers=headers)

    soup = BeautifulSoup(all_class.text, "lxml")

    lesson = soup.find_all(id="kbtable")[0].find_all("tr")
    lesson_list = []
    for i in range(1, 8):
        p = lesson[i].find_all(class_="kbcontent")
        for day, t in enumerate(p):
            someLesson = format_course_data(t, i, day + 1)
            if someLesson is not None:
                lesson_list += someLesson

    return lesson_list


def get_start_time(index):
    # 数据格式：1[03]0405
    course_list = ['0800', '0950', '1130', '1330', '1520', '1830', '2010']
    return course_list[index - 1]


def get_end_time(index):
    # 数据格式：10304[05] 1060708[09]
    course_list = ['0935', '1125', '1215', '1505', '1655', '2005', '2055']
    return course_list[index - 1]