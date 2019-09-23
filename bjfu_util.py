import http.client
import json
import urllib.parse


def get_course_list(stu_code):
    conn = http.client.HTTPConnection("newjwxt.bjfu.edu.cn")
    params = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
             "Content-Disposition: form-data; name=\"xnxq01id\"\r\n\r\n" \
             "2019-2020-1\r\n" \
             "------WebKitFormBoundary7MA4YWxkTrZu0gW--"
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'Accept': "*/*",
        'Host': "newjwxt.bjfu.edu.cn",
        'Accept-Encoding': "gzip, deflate",
    }
    conn.request("POST", "/jsxsd/appXsxk/getKb?xs0101id=" + stu_code, params, headers)
    res = conn.getresponse()
    data = res.read()
    return format_course_data(json.loads(data))


def format_course_data(class_json):
    class_list = []
    for class_data in class_json:
        class_weeks = class_data['kkzc'].split(',')
        for week in class_weeks:
            startWeek = endWeek = 0
            if '-' in week:
                week = week.split('-')
                startWeek = int(week[0])
                endWeek = int(week[1])
            else:
                startWeek = endWeek = int(week)
            class_info = {
                "className": class_data['kcmc'],
                "weekday": int(class_data['kcsj'][0]),
                "classroom": '未知' if class_data['jsmc'] is None else class_data['jsmc'],
                "teacherName": '未知' if class_data['jsxm'] is None else class_data['jsxm'],
                "startTime": get_start_time(class_data['kcsj']),
                "endTime": get_end_time(class_data['kcsj']),
                "week": {
                    "startWeek": startWeek,
                    "endWeek": endWeek
                }
            }
            class_list.append(class_info)
    return class_list


def get_start_time(course_num):
    # 数据格式：1[03]0405
    course_num = int(course_num[1] + course_num[2])
    course_list = ['0800', '0850', '0950', '1040', '1130', '1330', '1420', '1520', '1610', '1830', '1920', '2010']
    return course_list[course_num - 1]


def get_end_time(course_num):
    # 数据格式：10304[05] 1060708[09]
    course_num = int(course_num[len(course_num) - 2] + course_num[len(course_num) - 1])
    course_list = ['0845', '0935', '1035', '1125', '1215', '1415', '1505', '1605', '1655', '1915', '2005', '2055']
    return course_list[course_num - 1]
