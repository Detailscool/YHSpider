#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import sys
from selenium import webdriver
import time

reload(sys)
sys.setdefaultencoding('utf-8')

iOS_crewTeam = {'李远晖': 132, '李康德': 90, '廖成龙': 89, '陈波文': 92, '袁健强': 102}

android_crewTeam = {'张雄斌': 86, '毛金星': 73, '黄伟金': 141, '邹志刚': 84}

def get_text_from_tag(outer_list, name='a'):
    list = []
    for a_tag in outer_list:
        a = a_tag.find_all(name=name)
        text = a_tag.get_text()
        if a:
            print '2:', a[0].get_text()
            list.append(a[0].get_text().encode('utf-8'))
            print '-------'
        elif text:
            print '1:', text
            list.append(text.encode('utf-8'))
            print '-------'
    return list

def get_bugfix_content(id):
    driver.get('http://192.168.20.252/redmine/users/%d' % id)
    soup = BeautifulSoup(driver.page_source, 'lxml')

    bugfixs = []

    activities = soup.select('h4')
    # print 'soup :', soup.prettify()
    # print 'activities: ', activities
    # if activities and activities[0].get_text() == '今天':
    #     today_activity = activities[0].nextSibling.nextSibling
        # print type(today_activity)
        # print today_activity

    for index, activity in enumerate(activities):
        # print index, ':', 'activity:\n', activity, '\n'
        # if compare_time():
        #     today_activity.ge

        today_activity = activity.nextSibling.nextSibling
        print 'today_activity:\n', today_activity, '\n'

        bug_closed = today_activity.find_all(class_='issue-closed')
        bug_edit = today_activity.find_all(class_='issue-edit')
        bug_notes = today_activity.find_all(class_='issue-note')
        bug_note_des = today_activity.find_all(class_='description')

        bug_closed = get_text_from_tag(bug_closed)
        bug_edit = get_text_from_tag(bug_edit)
        bug_notes = get_text_from_tag(bug_notes)
        bug_note_des = get_text_from_tag(bug_note_des, name='span')

        if bug_closed or bug_edit or bug_notes or bug_note_des:
            bugfixs.append('\t<' + activity.get_text().encode('utf-8') + '>\n')

        if bug_closed:
            bugfixs.append('\t新增已修复内容：\n')
            [bugfixs.append('\t' + name + '\n') for name in bug_closed]

        if bug_edit:
            bugfixs.append('\t新增编辑内容：\n')
            [bugfixs.append('\t' + name + '\n') for name in bug_edit]

        notes = zip(bug_notes, bug_note_des)
        if notes:
            bugfixs.append('\t新增描述内容：\n')
            for note, des in zip(bug_notes, bug_note_des):
                bugfixs.append('\t' + note + ' --->>> ' + des + '\n')

        if bug_closed or bug_edit or bug_notes or bug_note_des:
            bugfixs.append('\n')

    return bugfixs

def txt_result_make(dict):
    if dict:
        bug_fix_contents = []
        for name, id in dict.items():
            print name, '-', id
            bug_fix_content = get_bugfix_content(id)
            if bug_fix_content:
                bug_fix_contents.append('%s ：\n' % name)
                bug_fix_contents += bug_fix_content

        f = open('a.txt', 'wb')
        f.writelines(bug_fix_contents)
        f.close()

        print '耗时 ： ', time.time() - start


if __name__ == '__main__':

    driver = webdriver.PhantomJS()

    url = 'http://192.168.20.252/redmine/login'

    driver.get(url)

    username_text = driver.find_element_by_name('username')
    password_text = driver.find_element_by_name('password')
    sure_button = driver.find_element_by_name('login')

    if username_text and password_text and sure_button:
        username_text.send_keys('liyuanhui')
        password_text.send_keys('liyuanhui')
        sure_button.click()
        time.sleep(0.5)

        print 'Logined……'

        if len(sys.argv[1:]) > 1:
            print '参数过多'
        else:
            work_name = sys.argv[1:][0] if len(sys.argv[1:]) == 1 else None
            if not work_name:
                while 1:
                    work_name = raw_input('你要搞边个RM:' + '\n1.iOS组' + '\n2.安卓组' + '\n3.某条油' + '\n').strip()

                    start = time.time()

                    if int(work_name) == 1:
                        txt_result_make(iOS_crewTeam)
                        pass
                    elif int(work_name) == 2:
                        txt_result_make(android_crewTeam)
                        pass
                    elif int(work_name) == 3:
                        name = raw_input("条油个名：\n").strip()
                        id = raw_input("条油噶id：\n").strip()
                        if name and id.isdigit():
                            args = {name: int(id)}
                            txt_result_make(args)
                            pass
                    else:
                        pass

