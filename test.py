from BOJ import Boj
from pprint import pprint
from getpass import getpass


def submit_test():
    source="""
    #include<stdio.h>
    int main(){
        int a,b;
        scanf("%d%d",&a,&b);
        printf("%d",a+b);
    }
    """

    boj = Boj()
    boj.login(input("ID :"),getpass("password :"))
    boj.submit(1000,source)
    boj.logout()


def problem_test():
    boj = Boj()
    pprint(boj.problem(1000))
    pprint(boj.problem(14923))
    pprint(boj.problem(14680))


def problemset_test():
    boj = Boj()
    pprint(boj.problem_set())


def status_test():
    boj = Boj()
    pprint(boj.status())
    pprint(boj.status(group_id=543))
    pprint(boj.status(group_id=543,problem_id=1000,user_id="sys7961",language='c++11',page=2))


def submission_test():
    boj = Boj()
    boj.login(input("ID :"),getpass("password :"))
    pprint(boj.submission(7273030))
    boj.logout()


def workbook_test():
    boj = Boj()
    pprint(boj.workbook(1774))


def workbook_list_test():
    boj = Boj()
    pprint(boj.workbook_list(1))


def workbook_ranklist_test():
    boj = Boj()
    pprint(boj.workbook_ranklist(1))


def user_test(handle):
    boj = Boj()
    pprint(boj.user(handle))

def vs_test(handle1, handle2):
    boj = Boj()
    pprint(boj.vs(handle1, handle2))

def board_list_test():
    boj = Boj()
    pprint(boj.boardlist())
