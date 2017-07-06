from pprint import pprint as pp
import numpy as np
import os
import sys
import re
if sys.version_info[0] >= 3:
    from tkinter.filedialog import askdirectory, askopenfilename
    from tkinter import messagebox
if sys.version_info[0] < 3:
    from tkFileDialog import askopenfilename, askdirectory
    import tkMessageBox as messagebox


class semester_data:
    def __init__(self, semester_name, num_questions):
        self._students = []
        self._answer_map = {}
        self._name = semester_name
        self._num_questions = num_questions

    def add_student(self, student_key):
        if student_key not in self._students:
            self._students.append(student_key)
            self._answer_map[student_key] = [[""]*self._num_questions, [""]*self._num_questions]

    def add_pre_answers(self, answer_list, student_key):
        if student_key not in self._students:
            self.add_student(student_key)
        """Convert answer list to string"""
        (self._answer_map[student_key])[0] = answer_list

    def add_post_answers(self, answer_list, student_key):
        if student_key not in self._students:
            self.add_student(student_key)
        """Convert answer list to string"""
        (self._answer_map[student_key])[1] = answer_list

    def write_csv_file(self, filename):
        header = self.generate_csv_header()
        csv_list = []
        keys = list(self._answer_map.keys())
        list.sort(keys)
        for student_key in keys:
            name_and_num = re.split('(\d+)',student_key)
            if len(name_and_num) > 1:
                name_and_num = [name_and_num[0] + ',' + name_and_num[1]]
            else:
                name_and_num = [name_and_num[0] + ',']
            csv_list.append(name_and_num+['']*4+self._answer_map[student_key][0]+['']+self._answer_map[student_key][1])
        np.savetxt(filename, csv_list, fmt='%s', delimiter=', ',header=header, comments='')

    def generate_csv_header(self):
        q_headers = ''
        n_questions = self._num_questions
        for i in range(1,(n_questions+1)):
            q_headers += "Q" + str(i)+','
        return "Student info,,,,,,Pre-Test Responses"+','*(n_questions+1)+"POST-Test Responses" + \
               "\nName,ID#,Major,Gender,University (M or U),," +q_headers + "," + q_headers

    def add_directory(self, dir_name, quiz_map, pre_or_post):
        for student_filename in os.listdir(dir_name):
            student_file_fullpath = os.path.join(dir_name, student_filename)
            self.add_student_answers(student_quiz_filename=student_file_fullpath, student_key=student_filename,
                                quiz_map=quiz_map, pre_or_post=pre_or_post)

    def add_student_answers(self, student_quiz_filename, student_key, quiz_map, pre_or_post):
        num_questions = len(quiz_map)
        try:
            qkc, qac = parse_student_file(student_quiz_filename, num_questions)
        except:
            print('Failed to parse student answers for file: ' + student_quiz_filename)
            return

        try:
            correlated_answers = correlate_answers(qac, quiz_map)
        except:
            print('Failed to correlate student ansers to key for file: ' + student_quiz_filename)
            return

        if pre_or_post == "pre":
            self.add_pre_answers(correlated_answers, student_key)
        else:
            self.add_post_answers(correlated_answers, student_key)


def parse_student_file(filename, num_questions):
    qkc = []
    qac = []

    with open(filename) as f:
        f.readline()
        f.readline()
        for i in range(0, num_questions):
            next_line = f.readline().split()
            del next_line[0]
            qkc.append(next_line)
        f.readline()

        i = 1
        while i <= num_questions:
            next_line = f.readline().split()
            if str(i) not in next_line[0]:
                qac.append('')
                i += 1
            qac.append(next_line[1])
            i += 1

    return qkc, qac


def correlate_answers(student_qa, quiz_map):
    mapped_anwsers = len(quiz_map)*['']
    for key in quiz_map.keys():
        mapped_anwsers[quiz_map[key]-1] = student_qa[key-1]
    return mapped_anwsers


def parse_quiz_map(filename):
    quiz_map = {}
    with open(filename) as f:
        f.readline()
        num_qs = 0
        for line in f:
            key_pair = line.strip().split(',')
            quiz_map[int(key_pair[0])] = int(key_pair[1])

    return quiz_map


def get_directory(msg):
    dir_name = askdirectory(title=msg)
    return dir_name


def get_quizmap():
    messagebox.showinfo(title="Greetings", message="Select quiz key file")
    quiz_filename = askopenfilename(title='Select quiz key file')
    return parse_quiz_map(quiz_filename)


def get_sub_dirs(dirname):
    sub_dirs = []
    for subdir, dirs, files in os.walk(dirname):
        for d in dirs:
            sub_dirs.append(d)
    return sub_dirs


def add_directories():
    messagebox.showinfo(title="Greetings", message="Select pretest directory")
    pre_dirname = get_directory("Select pretest directory")
    messagebox.showinfo(title="Greetings", message="Select post-test directory")
    post_dirname = get_directory("Select post test directory")
    pre_dirs = get_sub_dirs(pre_dirname)
    post_dirs = get_sub_dirs(post_dirname)

    quizmap = get_quizmap()
    n_questions = len(quizmap)
    for class_name in pre_dirs:
        s_data = semester_data(class_name, n_questions)

        s_data.add_directory(dir_name=os.path.join(pre_dirname,class_name),
                             quiz_map=quizmap, pre_or_post='pre')
        if class_name in post_dirs:
            s_data.add_directory(dir_name=os.path.join(post_dirname, class_name),
                                 quiz_map=quizmap, pre_or_post='post')
            post_dirs.remove(class_name)
        s_data.write_csv_file(class_name + '.csv')

    for class_name in post_dirs:
        s_data = semester_data(class_name, n_questions)
        s_data.add_directory(dir_name=os.path.join(post_dirname, class_name),
                             quiz_map=quizmap, pre_or_post='post')
        s_data.write_csv_file(class_name + '.csv')


def main():
    add_directories()

if __name__ == "__main__":
    main()
