from collections import OrderedDict
from lxml import etree
from lxml import html
import io
import sys
import glob
import json
import os

def getCourses(input_files):
    for input_file in glob.glob(input_files):
        html_f = io.open(input_file)
        htree = html.parse(html_f)
        subject = htree.xpath('''//div[@class = 'page-header']/h1/span/text()''')[0].strip().replace('/', '_')
        courses_info = []
        for element in htree.xpath('''//div[@class = 'tab-content']/div'''):
            courses = element.xpath('ul/li')
            for course in courses:
                course_info = OrderedDict()
                title = course.xpath('div/h3/text()')
                units = course.xpath('div/p[1]/text()')
                desc = course.xpath('div/p[2]/text()')
                course_info['course number & title'] = title[0] if title else ""
                course_info['Number of units'] = units[0] if units else ""
                course_info['Course description'] = desc[0] if desc else ""
                courses_info.append(course_info)
        output = OrderedDict()
        output['subject'] = subject
        output['courses'] = courses_info
        pos = len(subject) - subject[::-1].find('(') - 1
        subject = subject[:pos].rstrip()
        if not os.path.exists('../results/'):
            os.makedirs('../results/')
        with io.open('../results/' + subject + '.json', 'w') as f:
            f.write(json.dumps(output, indent=3))
        f.close()
        html_f.close()

if __name__ == '__main__':
    input_files = sys.argv[1]
    if input_files[-1] == '/':
        input_files += '*html'
    else:
        input_files += '/*html'
    getCourses(input_files)