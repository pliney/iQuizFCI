from pprint import pprint as pp
import numpy as np


class semester_data:
    _students = []
    _answer_map = {}


    def __init__(self, semester_name, num_questions):
        self._name = semester_name
        self._num_questions = num_questions

    def add_student(self, student_key):
        if student_key not in self._students:
            self._students.append(student_key)
            self._answer_map[student_key] = [[","]*self._num_questions, [""]*self._num_questions]

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

        for student_key in self._answer_map:
            """add to start of list"""
            csv_list.append([student_key]+['']*5+self._answer_map[student_key][0]+['']+self._answer_map[student_key][1])
        np.savetxt(filename, csv_list, fmt='%s', delimiter=', ',header=header)


    def generate_csv_header(self):
        q_headers = ''
        for i in range(1,(self._num_questions+1)):
            q_headers += "Q" + str(i)+','
        return "Student info,,,,,,Pre-Test Responses,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,POST-Test Responses,,,,," \
               ",,,,,,,,,,,,,,,,,,,,,,,,\nName,ID#,Major,Gender,University (M or U),," +q_headers + "," + q_headers
               # "Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9," \
               # "Q10,Q11,Q12,Q13,Q14,Q15,Q16,Q17,Q18,Q19,Q20,Q21,Q22,Q23,Q24,Q25,Q26,Q27,Q28,Q29,Q30,,Q1,Q2,Q3,Q4,Q5," \
               # "Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13,Q14,Q15,Q16,Q17,Q18,Q19,Q20,Q21,Q22,Q23,Q24,Q25,Q26,Q27,Q28,Q29,Q30"


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

        for i in range(0, num_questions):
            next_line = f.readline().split()
            qac.append(next_line[1])

    return qkc, qac


"""Need to figure out way to go through all the relevant files in a directory"""
def run_through_directory():
    pass


def add_student_answers(student_quiz_filename, student_key, sem_data, quiz_map, num_questions, pre_or_post):
    qkc, qac = parse_student_file(student_quiz_filename, num_questions)
    correlated_answers = correlate_answers(qac, quiz_map)
    if pre_or_post == "pre":
        sem_data.add_pre_answers(correlated_answers, student_key)
    else:
        sem_data.add_post_answers(correlated_answers, student_key)


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


def main():
    quizmap = parse_quiz_map('quiz_key.txt')
    n_questions = len(quizmap)
    s_data = semester_data('spring', n_questions)
    # add_student_answers('MICHAELIM6185', 'MICHAELIM6185', s_data, quizmap, n_questions, 'pre')
    # add_student_answers('MICHAELIM6185', 'MICHAELIM6185', s_data, quizmap, n_questions, 'post')
    # add_student_answers('BROWNK9241', 'BROWNK9241', s_data, quizmap, n_questions, 'pre')
    # add_student_answers('BROWNK9241', 'BROWNK9241', s_data, quizmap, n_questions, 'post')
    """Add try/catch for add_student_anwsers call"""
    add_student_answers('YIH7383', 'YIH7383', s_data, quizmap, n_questions, 'pre')
    add_student_answers('YIH7383', 'YIH7383', s_data, quizmap, n_questions, 'post')
    # add_student_answers('ZILLMANNR3944', 'ZILLMANNR3944', s_data, quizmap, n_questions, 'pre')
    # add_student_answers('ZILLMANNR3944', 'ZILLMANNR3944', s_data, quizmap, n_questions, 'post')
    s_data.write_csv_file('testfile.csv')



if __name__ == "__main__":
    main()