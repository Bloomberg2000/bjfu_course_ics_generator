# coding: utf-8
import time
import datetime
from bjfu_util import get_course_list
from random import Random

ics_first_day = time.time()
ics_reminder_method = ""
ics_event_uid = ""
ics_unit_uid = ""
ics_created_time = ""
ics_alarm_uid = ""
ics_stu_code = ""

class_info_list = []


# 输入检查方法
class InputCheckMethod:
    first_day = 0
    reminder = 1


def ics_create():
    global ics_alarm_uid, ics_unit_uid
    ics_string = "BEGIN:VCALENDAR\n" \
                 "METHOD:PUBLISH\n" \
                 "VERSION:2.0\n" \
                 "X-WR-CALNAME:课程表\n" \
                 "PRODID:-//Apple Inc.//Mac OS X 10.14.6//EN\n" \
                 "X-APPLE-CALENDAR-COLOR:#FB0055\n" \
                 "X-WR-TIMEZONE:Asia/Shanghai\n" \
                 "CALSCALE:GREGORIAN\n" \
                 "BEGIN:VTIMEZONE\n" \
                 "TZID:Asia/Shanghai\n" \
                 "BEGIN:STANDARD\n" \
                 "TZOFFSETFROM:+0900\n" \
                 "RRULE:FREQ=YEARLY;UNTIL=19910914T150000Z;BYMONTH=9;BYDAY=3SU\n" \
                 "DTSTART:19890917T000000\n" \
                 "TZNAME:GMT+8\n" \
                 "TZOFFSETTO:+0800\n" \
                 "END:STANDARD\n" \
                 "BEGIN:DAYLIGHT\n" \
                 "TZOFFSETFROM:+0800\n" \
                 "DTSTART:19910414T000000\n" \
                 "TZNAME:GMT+8\n" \
                 "TZOFFSETTO:+0900\n" \
                 "RDATE:19910414T000000\n" \
                 "END:DAYLIGHT\n" \
                 "END:VTIMEZONE\n"
    event = ""
    for class_info in class_info_list:
        class_name = class_info["className"]
        class_room = class_info["classroom"]
        start_time = class_info["startTime"]
        end_time = class_info["endTime"]
        teacher_name = class_info["teacherName"]
        index = 0
        for date in class_info["date"]:
            event += "BEGIN:VEVENT\nCREATED:" + class_info["CREATED"]
            event += "\nUID:" + class_info["UID"][index]
            event += "\nDTEND;TZID=Asia/Shanghai:" + date + "T" + end_time + "00"
            event += "\nTRANSP:OPAQUE\nX-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC\nSUMMARY:" + class_name
            event += "\nDTSTART;TZID=Asia/Shanghai:" + date + "T" + start_time + "00"
            event += "\nDTSTAMP:" + ics_created_time
            event += "\nLOCATION:" + class_room
            event += "\nDESCRIPTION:" + teacher_name
            event += "\nSEQUENCE:0\nBEGIN:VALARM\nX-WR-ALARMUID:" + ics_alarm_uid
            event += "\nUID:" + ics_unit_uid
            event += "\nTRIGGER:" + ics_reminder_method
            event += "\nDESCRIPTION:Reminder\nACTION:DISPLAY\nEND:VALARM\nEND:VEVENT\n"
            index += 1
    ics_string += event + "END:VCALENDAR"
    f = open(ics_stu_code + ".ics", 'wb')
    f.write(ics_string.encode("utf-8"))
    f.close()


def handle_class():
    global class_info_list, ics_first_day, ics_created_time, ics_event_uid
    for class_info in class_info_list:
        # 计算具体日期
        start_week = class_info["week"]["startWeek"]
        end_week = class_info["week"]["endWeek"]
        week_day = int(class_info["weekday"])
        # 计算开始和结束日期
        start_date = datetime.datetime.fromtimestamp(int(time.mktime(ics_first_day))) + \
                     datetime.timedelta(days=(start_week - 1) * 7 + week_day - 1)
        end_date = datetime.datetime.fromtimestamp(int(time.mktime(ics_first_day))) + \
                   datetime.timedelta(days=(end_week - 1) * 7 + week_day - 1)
        date_string = start_date.strftime('%Y%m%d')
        date_list = [date_string]
        current_date = start_date
        # 逐周添加
        flag = True
        while flag:
            current_date = current_date + datetime.timedelta(days=7)
            if current_date > end_date:
                flag = False
            else:
                date_string = current_date.strftime('%Y%m%d')
                date_list.append(date_string)
        class_info["date"] = date_list

        # 设置 UID
        create_time()
        class_info["CREATED"] = ics_created_time
        class_info["DTSTAMP"] = ics_created_time
        UID_List = []
        for current_date in date_list:
            UID_List.append(random_str(20))
        class_info["UID"] = UID_List


def create_time():
    global ics_created_time
    date = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    ics_created_time = date + "Z"


def set_first_week_date(firstWeekDate):
    global ics_first_day
    ics_first_day = time.strptime(firstWeekDate, '%Y%m%d')


def set_reminder(reminder):
    global ics_reminder_method
    reminder_list = ["-PT10M", "-PT30M", "-PT1H", "-PT2H", "-P1D"]
    if reminder == "1":
        ics_reminder_method = reminder_list[0]
    elif reminder == "2":
        ics_reminder_method = reminder_list[1]
    elif reminder == "3":
        ics_reminder_method = reminder_list[2]
    elif reminder == "4":
        ics_reminder_method = reminder_list[3]
    elif reminder == "5":
        ics_reminder_method = reminder_list[4]
    else:
        ics_reminder_method = "NULL"


def check_first_week_date(firstWeekDate):
    # 长度判断
    if len(firstWeekDate) != 8:
        return False
    year = firstWeekDate[0:4]
    month = firstWeekDate[4:6]
    date = firstWeekDate[6:8]
    dateList = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # 年份判断
    if int(year) < 1970:
        return False
    # 月份判断
    if int(month) == 0 or int(month) > 12:
        return False
    # 日期判断
    if int(date) > dateList[int(month) - 1]:
        return False
    return True


def basic_setting():
    global class_info_list, ics_stu_code, ics_alarm_uid, ics_unit_uid
    print("欢迎使用课程表生成工具。")
    # 获取学号
    stu_code = input("请输入北京林业大学学号(如：171001101): ")
    ics_stu_code = stu_code
    class_info_list = get_course_list(stu_code)

    # 获取第一周日期
    first_week_date = input("请设置第一周的星期一日期(如：20190902): ")
    check_input(InputCheckMethod.first_day, first_week_date)
    # 获取提醒设置
    reminder = input("正在配置提醒功能\n"
                     "【0】不提醒\n"
                     "【1】上课前 10 分钟提醒\n"
                     "【2】上课前 30 分钟提醒\n"
                     "【3】上课前 1 小时提醒\n"
                     "【4】上课前 2 小时提醒\n"
                     "【5】上课前 1 天提醒\n"
                     "请输入数字选择提醒时间: ")
    check_input(InputCheckMethod.reminder, reminder)
    # 生成随机id
    ics_alarm_uid = random_str(30)
    ics_unit_uid = random_str(20)


def check_input(check_method, str_input):
    if check_method == InputCheckMethod.first_day:
        if not check_first_week_date(str_input):
            first_day = input("输入有误，请重新输入第一周的星期一日期(如：20190902): ")
            check_input(InputCheckMethod.first_day, first_day)
        else:
            set_first_week_date(str_input)
    elif check_method == InputCheckMethod.reminder:
        if str_input not in ["0", "1", "2", "3", "4", "5"]:
            reminder = input("输入有误，请重新输入\n"
                             "【0】不提醒\n"
                             "【1】上课前 10 分钟提醒\n"
                             "【2】上课前 30 分钟提醒\n"
                             "【3】上课前 1 小时提醒\n"
                             "【4】上课前 2 小时提醒\n"
                             "【5】上课前 1 天提醒\n"
                             "请输入数字选择提醒时间: ")
            check_input(InputCheckMethod.reminder, reminder)
        else:
            set_reminder(str_input)


def random_str(random_length):
    return_str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        return_str += chars[random.randint(0, length)]
    return return_str


if __name__ == '__main__':
    basic_setting()
    handle_class()
    ics_create()
