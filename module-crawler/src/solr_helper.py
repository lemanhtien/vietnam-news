#!/usr/local/bin/python
# coding: utf-8

import os
import requests
import json

from web import *
from libs_support import *
from rss_parser import *
from database import *
from threading import Timer
import time

class Solr_helper:

    """ Ho tro He thong tu dong cap nhat du lieu - su dung post.jar de tu dong cap nhat du lieu moi vao he thong  theo
    tung khoang thoi gian nhat dinh """

    def __init__(self, db_name = "btl-tktdtt", domain = "localhost", port = 8983, solr_home = "."):
        self.server_db_name = db_name
        self.server_port = port
        self.server_domain = domain
        self.server_db_name = db_name

        #default
        self.set_solr_home(solr_home)

    # Cai dat cua solr
    def set_post_tool(self, path_tool):
        self.server_post_tool = path_tool
    def set_solr_home(self, path_home):
        if(path_home.endswith("/")): path_home = path_home[:-1]
        self.server_solr_home = path_home
        self.server_post_tool = path_home +"/example/exampledocs/post.jar"

    # update du lieu json web vao he thong
    def update_use_tool(self, path_file_json_data, type_update="text/json"):
        # use java tool
        cmd_update_data = "java -Dtype={2} -Durl=http://{0}:{1}/solr/{3}/update -jar {5} {4}" \
            .format(self.server_domain, self.server_port, type_update, self.server_db_name, path_file_json_data,
                    self.server_post_tool)
        print (cmd_update_data)
        # os.system(cmd_update_data)

    # update du lieu json web vao he thong
    def update(self, data_json):
        # post paterm: curl 'http://localhost:8983/solr/testBTL/update/json/docs' -H 'Content-type:application/json' -d '[{},{}]'
        # use Data with Index Handlers (DIH) Http post
        url = "http://{0}:{1}/solr/{2}/update/json/docs" \
            .format(self.server_domain, self.server_port, self.server_db_name)
        headers = dict()
        headers['Content-type'] = 'application/json'
        try:
            r = requests.post(url=url,data=data_json,headers=headers)
            r.close()
            return r.text  # .encode('utf-8', 'inorge')
        except Exception, e:
            print('Exception' + str(e))
            return None

    def reload(self):
        # post paterm: curl "http://localhost:8983/solr/admin/cores?action=RELOAD&core=mycore"
        # use Data with Index Handlers (DIH) Http post
        url = "http://{0}:{1}/solr/admin/cores?action=RELOAD&core={2}" .format(self.server_domain, self.server_port,self.server_db_name)
        try:
            r = requests.post(url=url)
            r.close()
            return r.text  # .encode('utf-8', 'inorge')
        except Exception, e:
            print('Exception' + str(e))
            return None

def crawl_data_to_file_from_link_rss(path_folder_save, link_rss):
    parser = rss_parser(link_rss)
    webs = parser.get_list_web()
    for web_x in  webs:
        web_x.write_to_file(path_folder_save)

def crawl_data_to_file(path_folder_save):
    rss_page_links = [
        "http://vietbao.vn/vn/rss",
        "http://vnexpress.net/rss",
        "http://dantri.com.vn/rss",
        "http://vtv.vn/rss",
        "http://techtalk.vn/"
    ]

    idSleep = 0
    if not os.path.exists(path_folder_save):
        os.makedirs(path_folder_save)

    # Cac trang co rss
    while True:
        for link_rss in rss_page_links:
            args = []
            args.append(path_folder_save)
            args.append(link_rss)
            threadCrawl = Timer(1, crawl_data_to_file_from_link_rss, args)
            threadCrawl.start()  # chay luong moi

        # nghi 15 phut cho lan crawl tiep theo
        idSleep += 1
        print "Id sleep to run new thread: {0}".format(idSleep)
        time.sleep(15*60)


def crawl_data():
    max_count_web = 500
    rss_page_links = [
        #"http://vietbao.vn/vn/rss",
        #"http://vnexpress.net/rss",
        "http://dantri.com.vn/rss",
        #"http://vtv.vn/rss",
        "http://techtalk.vn/"
    ]
    web_mannual_page_links = [
        # "vtv.vn"  ,
        "kenh14.vn"
    ]

    # Cai dat bo loc crawl web
    # Web_filter.set_last_time("2016-10-26, 22:20:08+07:00")  # Bai viet moi hon ke tu thoi diem xxx
    # Web_filter.set_limit_time("2016-10-26, 22:20:08+07:00", "2016-10-26, 23:20:08+07:00")  # Bai viet trong khoang tg
    Web_filter.set_max_count_web_each_domain(100000)  # moi domain khong vuot qua 1000
    Web_filter.set_max_count_web_each_sublabel(1000)  # moi label trong 1 domain k vuot qua 100

    # Cac trang co rss
    data = "["
    for link_rss in rss_page_links:
        parser = rss_parser(link_rss)
        webs = parser.get_list_web()
        for web_x in  webs:
            data += (web_x.get_json()+",")

    if data.__len__() > 1:
        data = data[:-1]+"]"
        solr = Solr_helper(db_name="btl-tktdtt")
        solr.set_solr_home("/mnt/01CDF1ECE3AB4280/DH/NAM_5/Ki_1/TimkiemTrinhDien/BTL/solr-6.2.1")

        print (solr.update(data))
        print (solr.reload())

def query():
    # http://localhost:8983/solr/btl-tktdtt/select?indent=on&q=*:*&wt=json	
    # http://localhost:8983/solr/btl-tktdtt/select?q=*:*&sort=dist(0,%2010,%2010)%20desc
    # http://localhost:8983/solr/btl-tktdtt/select?q=title:Thiên thần+url:thien-than
    None



if __name__ == "__main__":
    t = 1
    t = t +  1

    # Cai dat bo loc crawl web
    # Web_filter.set_last_time("2016-10-26, 22:20:08+07:00")  # Bai viet moi hon ke tu thoi diem xxx
    # Web_filter.set_limit_time("2016-10-26, 22:20:08+07:00", "2016-10-26, 23:20:08+07:00")  # Bai viet trong khoang tg
    Web_filter.set_max_count_web_each_domain(1000000000)  # moi domain khong vuot qua 1000
    Web_filter.set_max_count_web_each_sublabel(100000)  # moi label trong 1 domain k vuot qua 100



    # solr =  Solr_helper( db_name = "btl-tktdtt")
    # solr =  Solr_helper( db_name = "t2")
    # solr.set_solr_home("/mnt/01CDF1ECE3AB4280/DH/NAM_5/Ki_1/TimkiemTrinhDien/BTL/solr-6.2.1")
    # # # solr.update("/mnt/01CDF1ECE3AB4280/DH/NAM_5/Ki_1/TimkiemTrinhDien/BTL/vietnam-news/data-train/techtalk/Cong\ nghe/31fa871c7d521106e28c45f567a63445c33e1186.json")
    # #
    # data_test = []
    # data_test.append({
    # "code": "be07dcc96faeae2e5c30d5ab37d9da09230f33ae",
    # "title": "Z.com chính thức ra mắt Data Center tại Việt Nam",
    # "url": "http://dantri.com.vn/vi-tinh/zcom-chinh-thuc-ra-mat-data-center-tai-viet-nam-20161208203202433.htm",
    # "labels": "Dân trí/Sức mạnh số/Máy tính - Mạng",
    # "content": "\r\n    Ngày 08/12/2016, Z.com chính thức đưa vào khai thác và cung cấp dịch vụ Hosting, Cloud tại Data Center (viết tắt DC) đặt tại Việt Nam nhằm nâng cao chất lượng dịch vụ và đáp ứng nhu cầu ngày càng tăng của thị trường.\r\nTheo đó, Z.com sẽ cung cấp các dịch vụ Web Hosting, WordPress Hosting, Cloud VPS trên cả 4 DC bao gồm: Việt Nam; Nhật Bản; Singapore; Hoa Kỳ và các dịch vụ Email Hosting, Cloud Hosting trên DC Việt Nam. Việc triển khai Data Center tại Việt Nam sẽ giúp khách hàng có nhiều sự lựa chọn hơn và chất lượng dịch vụ tốt hơn nhiều so với trước đây.Đồng thời, trong thời gian này, Z.com cũng triển khai thêm các dịch vụ mới như sau:Email Hosting: Dịch vụ thư điện tử được cung cấp trên một hệ thống máy chủ chuyên biệt với những tính năng bảo mật cao. Cloud Hosting: Dịch vụ lưu trữ website được hoạt động trên nền công nghệ điện toán đám mây (Cloud computing). WordPress Hosting (nâng cấp): Với việc tăng thêm 2 gói WordPress Hosting và không giới hạn số lượng người truy cập, đây sẽ là sự lựa chọn tuyệt vời cho các bạn muốn tạo Website nhưng không biết về kỹ thuật.Cùng với việc đưa vào hoạt động các dịch vụ mới, Z.com cũng thực hiện nhiều chương trình ưu đãi, khuyến mãi đặc biệt cho sự kiện này:Đăng ký WordPress Hosting chỉ với 9,000 VNĐ/tháng, đối với gói Start. Giảm 50% khi đăng ký WordPress Hosting với các gói Professional; Enterprise. Giảm 50% khi transfer Web Hosting, Email Hosting, Cloud Hosting từ các DC nước ngoài về DC tại Việt Nam của Z.com.Khi sử dụng các gói Web Hosting, VPS,… với DC đặt tại nước ngoài, website của bạn sẽ phải đối mặt với nguy cơ chậm kết nối, không kết nối được khi đường cáp quang quốc tế (AAG) gặp trục trặc. Với tần suất đứt cáp như hiện nay thì việc lựa chọn gói Web Hosting, VPS,… với DC đặt tại Việt Nam sẽ là giải pháp tốt và an toàn nhất cho người sử dụng.Theo Nghị định về “Quản lý, cung cấp, sử dụng dịch vụ Internet và thông tin trên mạng” thì Tổ chức, doanh nghiệp thiết lập trang thông tin điện tử tổng hợp có quyền và nghĩa vụ sau đây:“Có ít nhất 01 hệ thống máy chủ đặt tại Việt Nam đáp ứng việc thanh tra, kiểm tra, lưu trữ, cung cấp thông tin theo yêu cầu của cơ quan quản lý nhà nước có thẩm quyền và giải quyết khiếu nại của khách hàng đối với việc cung cấp dịch vụ theo quy định của Bộ Thông tin và Truyền thông;”Nghị định được đăng tải đầy đủ trên trên webiste:http://moj.gov.vn/vbpq/lists/vn%20bn%20php%20lut/view_detail.aspx?itemid=28618",
    # "image_url": "https://dantri4.vcmedia.vn/zoom/80_50/2016/maytinh-1481203687425.jpg",
    # "date": "2016-12-09T09:00:00Z"
    # })
    #
    # data_test.append({
    # "code": "5ccad1b5813bc3833e27f08ea800e7c9dcaaa67d",
    # "title": "Angelina Jolie yêu cầu Brad Pitt mời bác sĩ tâm lý mới",
    # "url": "http://dantri.com.vn/giai-tri/angelina-jolie-yeu-cau-brad-pitt-moi-bac-si-tam-ly-moi-20161209114206897.htm",
    # "labels": "Dân trí/Giải trí",
    # "content": "\nDân trí Angelina Jolie muốn Brad Pitt mời một bác sĩ điều trị tâm lý mới nhằm giúp hai người và 6 đứa con tìm được những lời khuyên hợp lý vượt qua những áp lực từ cuộc cãi cọ trên máy bay từ Pháp về Mỹ hồi tháng 9 vừa rồi.\r\n Theo nguồn tin từ TMZ, luật sư của Angelina Jolie đã viết thư điện tử cho luật sư của Brad Pitt vào ngày 1/12 vừa rồi và yêu cầu bên Brad Pitt lựa chọn một bác sĩ tâm lý giỏi nhằm giúp những đứa con của họ vượt qua những áp lực tâm lý từ vụ việc không hay xảy ra trên máy bay 3 tháng trước. Angelina Jolie đã yêu cầu Brad Pitt mời bác sĩ tâm lý mới nhằm giúp các con cô điều trị tâm lý và vượt qua cú sốc về vụ cãi nhau trên phi cơ riêng từ Pháp về Mỹ hồi tháng 9 vừa rồi. Được biết, trên chuyến bay từ Pháp về Mỹ hồi tháng 9 vừa rồi, Brad Pitt đã bị nghi ngờ có hành động bạo hành với cậu con trai cả, Maddox. Sau sự việc này, Angelina Jolie đã đệ đơn lên tòa án yêu cầu được ly dị với Brad Pitt sau 2 năm chung sống và muốn giành quyền nuôi cả 6 đứa con. Những cáo buộc này khiến Brad Pitt bị điều tra suốt hai tháng nhưng tháng 11 vừa rồi, FBI đã khẳng định, anh hoàn toàn vô tội.Tuy nhiên, phía Angelina Jolie vẫn không hài lòng với những phán quyết mới nhất của tòa và cho rằng, nam diễn viên 52 tuổi cần nỗ lực hơn nữa để giúp các con của anh vượt qua những khủng hoảng và ức chế tinh thần từ vụ việc không hay xảy ra trên máy bay hồi tháng 9/2016. Phía nữ diễn viên 41 tuổi tin rằng, những đứa con của cô đã có những ấn tượng không mấy tốt đẹp từ những gì xảy ra trên máy bay lúc đó. Nữ diễn viên xinh đẹp cho rằng, các con cô bị ảnh hưởng tâm lý nặng nề từ những hành động của Brad Pit đối với Maddox trên phi cơ hồi tháng 9/2016 dù nam diễn viên 52 tuổi đã được chứng minh vô tội. Trang TMZ còn đưa thêm thông tin, tháng 9 vừa rồi, cả Brad Pitt và Angelina Jolie đã đồng ý tham dự những buổi điều trị tâm lý của cả gia đình, đây là một trong những hoạt động nằm trong thỏa thuận tạm thời về việc ly dị của hai ngôi sao nổi tiếng. Họ vẫn đang bàn bạc, thảo luận để có những thống nhất cuối cùng về việc phân chia quyền nuôi con hậu ly dị. Song, trong tài liệu trình lên tòa án, luật sư của Brad Pitt cho hay, hai cậu con trai Maddox và Pax không muốn gặp cha ruột.Ngày 7/12 vừa rồi, Brad Pitt đã yêu cầu có một phiên xét xử khẩn cấp về việc phân chia quyền nuôi con giữa anh và Angelina Jolie khi hai người chia tay nhưng đã bị tòa từ chối. Do đó, Brad Pitt sẽ phải chờ đợi tới ngày 12/1 tới đây mới có thể gặp gỡ Angelina Jolie tại tòa và bàn bạc về quyền của họ đối với các con sau ly dị. Angelina Jolie đệ đơn ly dị từ tháng 9/2016 và vẫn đang chiến đấu với chồng cũ để giành quyền nuôi 6 đứa con sau khi hai người chia tay. Trong đơn gửi lên tòa, Brad Pitt bày tỏ sự lo lắng của anh tới tâm lý của tụi trẻ do vụ ly dị này gây ra. Nhưng phía Angelina lại cho rằng, những gì Brad Pitt đang làm chỉ nhằm mục đích bảo vệ danh tiếng của bản thân chứ không hề nghĩ tới các con.Brad Pitt và Angelina Jolie kết hôn vào mùa hè năm 2014 tại Pháp nhưng chỉ sau 2 năm chung sống, cặp đôi đã quyết định chia tay. Trước đó, họ đã ở bên nhau 10 năm và có tới 6 đứa con chung, ba con ruột và ba con nuôi. Theo mong muốn của Angelina Jolie, cô muốn được giành toàn quyền nuôi 6 đứa con trong khi Brad Pitt khát khao được cùng vợ chăm sóc các con sau khi hai người ly dị.Sắp tới, Angelina Jolie sẽ đưa các con về Los Angeles sống. Mẹ con cô đã \"ấn náu\" tại Malibu kể từ khi cô đệ đơn ly dị Brad Pitt vào tháng 9/2016.Mi Vân (tổng hợp)",
    # "image_url": "https://dantri4.vcmedia.vn/zoom/80_50/2016/3b12b55f00000578-4012752-image-a-1-1481194854432-1481258252944-crop-1481258280959.jpg",
    # "date": "2016-12-09T12:19:00Z"
    # })
    # data_json = (json.dumps(data_test,indent=4, separators=(',', ': '), ensure_ascii=False))
    # solr.update(data_json)
    # print (solr.reload())

    # crawl_data()
    crawl_data_to_file('DataOffline')
