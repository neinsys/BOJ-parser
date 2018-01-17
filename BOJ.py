import requests, json
from bs4 import BeautifulSoup
from copy import deepcopy


class Boj:
    _BOJ_URL = "https://www.acmicpc.net/"
    _SIGNIN = 'signin/'
    _SUBMIT = 'submit/'
    _LOGOUT = 'logout/'
    _STATUS = 'status/'
    _PROBLEM = 'problem/'
    _PROBLEMSET = "problemset/"
    _SUBMISSION = "source/"
    _WORKBOOK = "workbook/"
    _USER = "user/"
    _VS = "vs/"

    _LANGUAGE_MAP = {

    }

    _RESULT_MAP = {

    }

    _LOGIN_FORM = {
        "login_user_id": None,
        "login_password": None,
        "auto_login": None,
        "next": "/"
    }

    _LOGOUT_FORM = {
        "next": "/"
    }

    _SUBMIT_FORM = {
        "problem_id": None,
        "code_open": None,  # open, close, onlyaccepted
        "source": None,
        "language": None,
        "csrf_key": None
    }

    _PROBLEM_INFO = {
        'problem_id': None,
        "problem_title": None,
        'info': [],
        "time_limit": None,
        "memory_limit": None,
        "number_of_submission": None,
        "number_of_accepted_submission": None,
        "number_of_accepted_people": None,
        "accept_rate": None,
        "problem_description": None,
        "problem_input": None,
        "problem_output": None,
        "sample_input": [],
        "sample_output": [],
        "problem_hint": None,
        "source": [],
        "problem_association": [],
        "problem_tags": []
    }

    _PROBLEM_SMALL_INFO = {
        'problem_id' : None,
        'problem_title' : None,
        'info': [],
        'number_of_submission':None,
        'number_of_accepted_submission':None,
        'accept_rate':None
    }

    _SUBMISSION_INFO = {
        'source':None,
        'submission_id':None,
        'user_id':None,
        'problem_id':None,
        'problem_title':None,
        'result':None,
        'memory':None,
        'time':None,
        'language':None,
        'code_size':None,
        'submission_time':None,
        'submission_time_2':None
    }

    _WORKBOOK_INFO = {
        'title': None,
        'author': None,
        'comment': None,
        'problem': [],
        'clear_users': []
    }

    _WORKBOOK_SMALL_INFO = {
        'workbook_id': None,
        'title': None,
        'author': None,
        'number_of_clear_users': []
    }

    _USER_INFO = {
        'handle': None,
        'message': None,
        'statics': {},
        'solved_problem': [],
        'tried_but_unsolved_problem': [],
        'submission_info': []
    }

    _USER_RANK_INFO = {
        'rank': None,
        'handle': None
    }

    _USER_RANK_WORKBOOK_INFO = {
        'rank': None,
        'handle': None,
        'number_of_clear_workbook': None,
        'last_clear': None
    }

    _VS_INFO = {
        'handle1' : None,
        'handle2' : None,
        'both_solved_problem' : [],
        'only_1_solved_problem' : [],
        'only_2_solved_problem' : []
    }

    _session = None

    def __init__(self):
        self._session = requests.session()
        self._getInfo()

    def _getInfo(self):
        url = self._BOJ_URL + self._STATUS
        submit_html = self._session.get(url).text
        soup = BeautifulSoup(submit_html, "html.parser")

        language_list = soup.find("select", {"name": "language_id"})
        result_list = soup.find("select", {"name": "result_id"})

        for op in language_list.find_all("option"):
            self._LANGUAGE_MAP[op.text.lower()] = int(op.get('value'))
        for op in result_list.find_all("option"):
            self._RESULT_MAP[op.text] = int(op.get('value'))

    def login(self, ID, password, auto_login=False):
        login_form = deepcopy(self._LOGIN_FORM)
        login_form['login_user_id'] = ID
        login_form['login_password'] = password
        login_form['auto_login'] = auto_login
        res = self._session.post(self._BOJ_URL + self._SIGNIN, data=login_form)

    def logout(self):
        logout_form = deepcopy(self._LOGOUT_FORM)
        res = self._session.post(self._BOJ_URL + self._LOGOUT, data=logout_form)

    def problem(self, problem_id):
        problem_info = deepcopy(self._PROBLEM_INFO)

        url = self._BOJ_URL + self._PROBLEM + str(problem_id)

        problem_info['problem_id'] = problem_id

        problem_html = self._session.get(url).text
        soup = BeautifulSoup(problem_html,"html.parser")

        problem_info['problem_title'] = soup.find('span', id='problem_title').text
        spans=soup.find('span', id='problem_title').parent.find_all('span')[2:]
        for span in spans:
            problem_info['info'].append(span.text)

        tds = soup.find('table',{'id':'problem-info'}).tbody.tr.find_all('td')
        order = ['time_limit', 'memory_limit', 'number_of_submission', 'number_of_accepted_submission', 'number_of_accepted_people', 'accept_rate']
        for id, key in enumerate(order):
            problem_info[key] = tds[id].text

        problem_info['problem_description'] = soup.find('div', id='problem_description').text.strip()
        problem_info['problem_input'] = soup.find('div', id='problem_input').text.strip()
        problem_info['problem_output'] = soup.find('div', id='problem_output').text.strip()

        idx = 1
        while True:
            try:
                sample_input = soup.find('pre', id="sample-input-{}".format(idx)).text
                sample_output = soup.find('pre', id="sample-output-{}".format(idx)).text
            except:
                break
            problem_info['sample_input'].append(sample_input)
            problem_info['sample_output'].append(sample_output)
            idx += 1

        problem_info['problem_hint'] = soup.find('div', id='problem_hint').text

        extras = ['source','problem_association','problem_tags']
        for key in extras:
            section = soup.find('section',id=key)
            try:
                p = section.p
                problem_info[key].append(p.text.replace('\t','').strip())
            except:
                pass
            try:
                lis = section.find_all('li')
                for li in lis:
                    problem_info[key].append(li.text.replace('\t','').strip())
            except:
                pass

        return problem_info

    def problem_set(self,page=1,search=None):
        url = self._BOJ_URL + self._PROBLEMSET
        url += "?page={}".format(page)
        if search is not None:
            url += "&search={}".format(search)

        problem_set_html = self._session.get(url).text
        soup = BeautifulSoup(problem_set_html, "html.parser")

        trs = soup.find('table', id="problemset").tbody.find_all('tr')

        order = ['problem_id', 'problem_title', 'info', 'number_of_accepted_submission',
                 'number_of_submission', 'accept_rate']
        problem_set = []

        for tr in trs:
            problem_info = deepcopy(self._PROBLEM_SMALL_INFO)
            for idx, td in enumerate(tr.find_all('td')):
                if idx == 2:
                    for span in td.find_all('span'):
                        problem_info[order[idx]].append(span.text)
                else:
                    problem_info[order[idx]] = td.text
            problem_set.append(problem_info)

        return problem_set

    def submit(self, problem_id, source, language="c++11", code_open="open"):
        url = self._BOJ_URL + self._SUBMIT + str(problem_id)
        csrf_key = None

        if type(language) != type(int):
            language = self._LANGUAGE_MAP[language.lower()]

        submit_html = self._session.get(url).text
        soup = BeautifulSoup(submit_html, "html.parser")

        csrf_key = soup.find("input", {'name': 'csrf_key'}).get('value')

        submit_form = deepcopy(self._SUBMIT_FORM)
        submit_form['problem_id'] = problem_id
        submit_form['code_open'] = code_open
        submit_form['language'] = language
        submit_form['source'] = source
        submit_form['csrf_key'] = csrf_key

        res = self._session.post(url, data=submit_form)

    def workbook_list(self,page=1):
        url = self._BOJ_URL + self._WORKBOOK + "list"
        url += "?page={}".format(page)

        workbook_list_html = self._session.get(url).text
        soup = BeautifulSoup(workbook_list_html, "html.parser")

        trs = soup.find('table', id="problemset").tbody.find_all('tr')

        order = ['workbook_id', 'author', 'title', '',
                 'number_of_clear_users']
        workbook_list = []

        for tr in trs:
            workbook_info = deepcopy(self._WORKBOOK_SMALL_INFO)
            for idx, td in enumerate(tr.find_all('td')):
                if idx == 3:
                    pass
                else:
                    workbook_info[order[idx]] = td.text
            workbook_list.append(workbook_info)

        return workbook_list

    def workbook_ranklist(self, page=1):
        url = self._BOJ_URL + self._WORKBOOK + "ranklist"
        url += "?page={}".format(page)

        workbook_ranklist_html = self._session.get(url).text
        soup = BeautifulSoup(workbook_ranklist_html, "html.parser")

        trs = soup.find('table', id="problemset").tbody.find_all('tr')

        order = ['rank', 'handle', '', 'number_of_clear_workbook',
                 'last_clear']
        workbook_ranklist = []

        for tr in trs:
            user_info = deepcopy(self._USER_RANK_WORKBOOK_INFO)
            for idx, td in enumerate(tr.find_all('td')):
                if idx == 2:
                    pass
                else:
                    user_info[order[idx]] = td.text
            workbook_ranklist.append(user_info)

        return workbook_ranklist

    def workbook(self, workbook_id):
        view_url = self._BOJ_URL + self._WORKBOOK + "view/" + str(workbook_id)
        clear_url = self._BOJ_URL + self._WORKBOOK + "clear/" + str(workbook_id)

        workbook = deepcopy(self._WORKBOOK_INFO)

        view_html = self._session.get(view_url).text
        view_soup = BeautifulSoup(view_html, "html.parser")
        clear_html = self._session.get(clear_url).text
        clear_soup = BeautifulSoup(clear_html, "html.parser")

        workbook['title'] = view_soup.find('span',id='workbook_title').text
        workbook['comment'] = view_soup.find('span',id='workbook_comment').text
        workbook['author'] = view_soup.find('blockquote').a.text

        trs = view_soup.find('table', id="anothersortable").tbody.find_all('tr')

        order = ['problem_id', 'problem_title', 'info', 'number_of_accepted_submission',
                 'number_of_submission', 'accept_rate']
        problem_set = []

        for tr in trs:
            problem_info = deepcopy(self._PROBLEM_SMALL_INFO)
            for idx, td in enumerate(tr.find_all('td')):
                if idx == 2:
                    for span in td.find_all('span'):
                        problem_info[order[idx]].append(span.text)
                else:
                    problem_info[order[idx]] = td.text
            problem_set.append(problem_info)

        workbook['problem'] = problem_set

        users = clear_soup.find('p', {'class': "lead"}).find_all('a')

        clear_users = []

        for user in users:
            clear_users.append(user.text)

        workbook['clear_users'] = clear_users

        return workbook

    def submission(self, submission_id):
        url = self._BOJ_URL + self._SUBMISSION + str(submission_id)

        submission_html = self._session.get(url).text
        soup = BeautifulSoup(submission_html, "html.parser")

        submission = deepcopy(self._SUBMISSION_INFO)

        submission['source'] = soup.find('textarea',id="source").text

        order = ['submission_id', 'user_id', 'problem_id', 'problem_title', 'result',
                 'memory', 'time', 'language', 'code_size', 'submission_time']

        tds = soup.find('table').tbody.find_all('td')
        for idx, td in enumerate(tds):
            submission[order[idx]]=td.text.strip()
            if idx == 9:
                submission['submission_time_2'] = td.a.get('title')

        return submission

    def status(self, page=1, **option):
        #top=None, problem_id=None, user_id=None, language=None, result=None, group_id=None, workbook_id=None, school_id=None
        url = self._BOJ_URL + self._STATUS + '?'
        for key,value in option.items():
            if key == 'language':
                url += 'language_id={}&'.format(self._LANGUAGE_MAP[value])
            else:
                url += '{}={}&'.format(key,value)
        url = url[:-1]

        order = ['submission_id', 'user_id', 'problem_id', 'result',
                 'memory', 'time', 'language', 'code_size', 'submission_time']
        submissions = []

        for _ in range(page):
            status_html = self._session.get(url).text
            soup = BeautifulSoup(status_html, "html.parser")

            trs = soup.find('table', id='status-table').tbody.find_all('tr')
            for tr in trs:
                submission = deepcopy(self._SUBMISSION_INFO)
                for idx, td in enumerate(tr.find_all('td')):
                    submission[order[idx]] = td.text.strip()
                    if idx == 2:
                        submission['problem_title'] = td.a.get('title')
                    if idx == 8:
                        submission['submission_time_2'] = td.a.get('title')
                submissions.append(submission)

            next_page = soup.find('a',id='next_page')
            if next_page is None:
                break
            url = self._BOJ_URL[:-1] + next_page.get('href')
        return submissions

    def contest(self):
        pass

    def user(self, handle):
        url = self._BOJ_URL + self._USER + handle

        user_html = self._session.get(url).text
        soup = BeautifulSoup(user_html, "html.parser")

        user = deepcopy(self._USER_INFO)

        head = soup.find('div', {'class':'page-header'})
        user['handle'] = head.h1.text.strip()
        user['message'] = head.blockquote.text.strip()

        statics = soup.find('table', id='statics')

        for tr in statics.find_all('tr'):
            user['statics'][tr.th.text.strip()] = tr.td.text.strip()

        problem_list = soup.find_all('div', {'class': 'panel-body'})
        solved_problem_list = problem_list[0].find_all('span')
        unsolved_problem_list = problem_list[1].find_all('span')

        for idx in range(0,len(solved_problem_list), 2):
            user['solved_problem'].append((solved_problem_list[idx].text,solved_problem_list[idx+1].text))
        for idx in range(0,len(unsolved_problem_list), 2):
            user['tried_but_unsolved_problem'].append((unsolved_problem_list[idx].text,unsolved_problem_list[idx+1].text))

        return user

    def vs(self, handle1, handle2):
        url = self._BOJ_URL + self._VS + handle1 + '/' + handle2

        vs_html = self._session.get(url).text
        soup = BeautifulSoup(vs_html, "html.parser")

        vs = deepcopy(self._VS_INFO)

        vs['handle1'] = handle1
        vs['handle2'] = handle2

        problem_list = soup.find_all('div', {'class': 'panel-body'})

        both_solved_problem_list = problem_list[0].find_all('span')
        only_1_solved_problem_list = problem_list[1].find_all('span')
        only_2_solved_problem_list = problem_list[2].find_all('span')

        for idx, title in zip(both_solved_problem_list[::2], both_solved_problem_list[1::2]):
            vs['both_solved_problem'].append((idx.text, title.text))

        for idx, title in zip(only_1_solved_problem_list[::2], only_1_solved_problem_list[1::2]):
            vs['only_1_solved_problem'].append((idx.text, title.text))

        for idx, title in zip(only_2_solved_problem_list[::2], only_2_solved_problem_list[1::2]):
            vs['only_2_solved_problem'].append((idx.text, title.text))

        return vs


    def ranklist(self):
        pass

    def board(self):
        pass

    def group(self):
        pass

    def blog(self):
        pass

    def lectures(self):
        pass

