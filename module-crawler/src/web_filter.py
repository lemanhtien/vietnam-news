
from web import *

class Web_filter(object):

    """Lop tinh - gom cac phuong thuc tinh de loc doi tuong web truoc khi crawl noi dung ve """

    def __init__(self):
        None

    # thoi gian cuoi cung de 1 trang web dc chap nhan crawl ve, cac trang web publish sau thoi diem nay se dc chap nhan
    lst_link_code_crawled = []
    # thoi gian cuoi cung de 1 trang web dc chap nhan crawl ve, cac trang web publish sau thoi diem nay se dc chap nhan
    check_last_time = None
    # so web toi da 1 sublabel
    check_max_count_web_each_sublabel = None
    # so web toi da 1 domain
    check_max_count_web_each_domain = None
    # khoang thoi gian gioi han
    start_time= None
    finish_time = None

    # Cai dat thoi gian cua bai viet cuoi cung voi dinh dang: 2014-07-29, 22:45:00+07:00
    @staticmethod
    def set_last_time(date_time_string):
        try:
            # Parse thu tg - ko parse dc thi thoi
            Web_filter.check_last_time = dateutil_parser.parse(date_time_string)
        except:
            None
    @staticmethod
    def set_max_count_web_each_sublabel(number):
        Web_filter.check_max_count_web_each_sublabel = number

    @staticmethod
    def set_max_count_web_each_domain(number):
        Web_filter.check_max_count_web_each_domain = number

    # Cai dat gioi han khoang thoi gian
    # vd: set_limit_time( '2014-07-29, 22:45:00+07:00',  '2014-07-29, 22:50:00+07:00')
    # chi lay cac bai viet co nhan thoi gian trong khoang tu  22:45 - 22:50
    @staticmethod
    def set_limit_time(start_time_string, finish_time_string):
        Web_filter.start_time =  dateutil_parser.parse(start_time_string)
        Web_filter.finish_time = dateutil_parser.parse(finish_time_string)

    @staticmethod
    def remove_all_check():
        Web_filter.check_last_time = None
        Web_filter.check_max_count_web_each_sublabel = None
        Web_filter.check_max_count_web_each_domain = None

    @staticmethod
    def check(web_x, count_web_each_sublabel = 100000, count_web_each_domain = 100000):
        b_ret = True
        try:
            # Kiem tra xem web nay da crawler hay chua
            if b_ret == True:
                link_encode = web_x.get_code()
                b_ret = link_encode not in Web_filter.lst_link_code_crawled

            if b_ret == True and Web_filter.check_last_time != None:
                b_ret = web_x.get_date_obj() > Web_filter.check_last_time

            if b_ret == True and Web_filter.check_max_count_web_each_sublabel != None:
                b_ret = count_web_each_sublabel < Web_filter.check_max_count_web_each_sublabel

            if b_ret == True and Web_filter.check_max_count_web_each_domain != None:
                b_ret = count_web_each_domain < Web_filter.check_max_count_web_each_domain

            if b_ret == True and Web_filter.start_time != None and Web_filter.finish_time != None :
                b_ret = (web_x.get_date_obj() > Web_filter.start_time and web_x.get_date_obj() < Web_filter.finish_time)

        except Exception,e :
            print ("[Exception - check filter]"+str(e))
            b_ret = False

        return b_ret

    @staticmethod
    def add_link_code_crawled(link_encode):
        # Kiem tra link_code da duoc crawled hay chua
        if (link_encode not in Web_filter.lst_link_code_crawled):
            # them vao ds neu link_code ko co
            Web_filter.lst_link_code_crawled.append(link_encode)
            # Gioi han cho ds luu tru link_code ko vuot qua 10000 moi nhat
            # Do moi lan crawl chi duoc 2000 nen khong can thiet kiem tra phan tu xa truoc do
            if (Web_filter.lst_link_code_crawled.__len__() > 10000):
                Web_filter.lst_link_code_crawled = Web_filter.lst_link_code_crawled[5000:]



            # set_last_time = staticmethod(set_last_time)
    # set_max_count_web_each_sublabel = staticmethod(set_max_count_web_each_sublabel)
    # set_max_count_web_each_domain = staticmethod(set_max_count_web_each_domain)
    # remove_all_check = staticmethod(remove_all_check)
    # check = staticmethod(check)

#
#
#
#
#
#
if __name__ == '__main__':
    # Web_filter.set_max_count_web_each_domain(100)
    hy= web("324hihihi", "", "","","", "")
    hy2 = web("324hihihi", "", "", "", "", "")
    print hy.get_json()
    print Web_filter.check(hy,10)
    Web_filter.add_link_code_crawled(hy.get_code())
    print Web_filter.check(hy2, 10)
