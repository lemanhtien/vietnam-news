
import  os

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
    def update(self, path_file_json_data, type_update="text/json"):
        cmd_update_data = "java -Dtype={2} -Durl=http://{0}:{1}/solr/{3}/update -jar {5} {4}" \
            .format(self.server_domain, self.server_port, type_update, self.server_db_name, path_file_json_data,
                    self.server_post_tool)
        # print (cmd_update_data)
        os.system(cmd_update_data)


if __name__ =="__main__":
    solr =  Solr_helper()
    solr.set_solr_home("/mnt/01CDF1ECE3AB4280/DH/NAM_5/Ki_1/TimkiemTrinhDien/BTL/solr-6.2.1")
    solr.update("/mnt/01CDF1ECE3AB4280/DH/NAM_5/Ki_1/TimkiemTrinhDien/BTL/vietnam-news/data-train/techtalk/Cong\ nghe/31fa871c7d521106e28c45f567a63445c33e1186.json")

