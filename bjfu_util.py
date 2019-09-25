# encoding: utf-8
import requests
from bs4 import BeautifulSoup
import re


def format_course_data(infomation, course_index, week_day):
    if infomation.text == '\xa0':
        return None
    else:
        course_list = re.sub('-{2,}', " ", infomation.text).split()
        course_info_list = []
        for single_course_info in course_list:
            course_info_list += create_course(single_course_info, course_index, week_day)
        return course_info_list


def create_course(information, course_index, weekday):
    """
    软件工程A(必修)赵方6-9,12-13,15,17-18(周)二教307
    """
    className = re.search('.{0,}\([\u4e00-\u9fa5]{2,}\)', information).group()
    information = information.replace(className, "")
    # 什么人教
    teacherName = re.search("^[\u4e00-\u9fa5]{0,}", information).group()
    information = information.lstrip(teacherName)
    # 何时上课
    courseTimeText = re.search(".{0,}\(周\)", information).group()
    # 在哪上课
    classRoom = information.lstrip(courseTimeText)
    # 具体何时
    class_weeks = courseTimeText.strip('(周)').split(',')
    course_list = []

    for week in class_weeks:
        startWeek = endWeek = 0
        if '-' in week:
            week = week.split('-')
            startWeek = int(week[0])
            endWeek = int(week[1])
        else:
            startWeek = endWeek = int(week)
        class_dict = {
            "className": className,
            "weekday": weekday,
            "classroom": classRoom,
            "teacherName": teacherName,
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
