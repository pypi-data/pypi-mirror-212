import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from lxml import html


class Jobs:
    
    def __init__ (self, keyword):
        self.keyword = keyword
        self.job_links = []
        self.jobs = []
        
    def xpath_match(self, col_name, index):
        match = {"職務類別" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div/div//*/div/div/u",
             "工作待遇" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div/p[1]",
             "工作性質" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "上班地點" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div/div/span[1]",
             "遠端工作" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div", 
             "上班時段" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "休假制度" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "可上班日" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "需求人數" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "管理責任" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "出差外派" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[2]/div",
             "法定項目" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[4]/div[{index + 1}]/div//*/a",
             "其他福利" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[4]/div[{index + 1}]/div//*/a",
             "工作經歷" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div",
             "學歷要求" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div",
             "科系要求" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div",    
             "擅長工具" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div//*/a/u",   
             "工作技能" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div//*/a/u",
             "具備證照" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[2]/div//*/p/a/u",
             "其他條件" : f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div/div/p",
            }
        return match.get(col_name)

    def search_jobs(self, max_pages = 30):
        page = 1
        data = []
        print(f"開始搜尋關鍵字: {self.keyword}")
        while True:
            url = f'https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={self.keyword}&expansionType=area%2Cspec%2Ccom%2Cjob%2Cwf%2Cwktm&order=15&asc=0&page={page}&mode=s&jobsource=2018indexpoc&langFlag=0&langStatus=0&recommendJob=1&hotJob=1'
            res = requests.get(url)
            soup = BeautifulSoup(res.text, features="lxml")
            jobs = soup.find_all('article', class_='b-block--top-bord job-list-item b-clearfix js-job-item')
            if not jobs:
                break
            print("現在正在讀取第" + str(page) + "頁")
            for job in jobs:
                title = job['data-job-name'].strip()
                company = job('li')[1].text.strip()
                URL = 'https:' + job.find("a", class_='js-job-link')['href']
                dict1 = {"公司名稱": company, "職缺名稱": title, "職缺連結": URL}
                data.append(dict1)
            if page == max_pages:
                break
            page += 1
        if data:
            self.job_links = pd.DataFrame(columns = data[0].keys(), data = data)
            print("-"*20)
            print("已完成搜尋，請使用find_jobs爬取工作資料")
            print("-"*20)
        else:
            print("查詢失敗")
        return self.job_links
        
    def save_jobs_link(self):
        if not self.job_links:
            print("無資料可儲存")
            return
        path = self.keyword + r"-職缺連結.xlsx" #定義檔案路徑 #當檔案名稱有中文要加r
        df.to_excel(path, index = False)
        print("檔案儲存", path)
    
    def load_jobs_link(self, path = None):
        if not path:
            path = self.keyword + "-職缺連結.xlsx"
        if path not in os.listdir:
            print(f"找不到{path} 之資料，請先使用find_jobs & save_to_excel產生職位列表檔案")
            return
        self.job_links = pd.read_excel(path)
        return self.job_links
    
    def list2string(self, list_): #修改list資料變成string，因為在excel中比較好處理
        if type(list_) == str:
            return list_
        elif not list_:#空list
            return ""
        elif type(list_) == list:
            try:
                output = ",".join(list_)
            except:
                output = ""
            return output
        else:
            #print("型態錯誤，非list&str, 回傳空白")
            return ""
    
    #從個別職缺的網頁中取得資料
    def creep_job(self, url):
        res = requests.get(url)
        tree = html.fromstring(res.text)
        data_dict = {}
        title = tree.xpath("/html/body/div[2]/div/div[1]/div[2]/div/div/div[1]/h1")
        company = tree.xpath("/html/body/div[2]/div/div[1]/div[2]/div/div/div[1]/div/a[1]")
        work = tree.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[1]/p")
       
        data_dict["職務名稱"] = title[0].text.strip()
        #data_dict["公司名稱"] = company[0].text #上面好像有了
        for index in range(2,15):
            p1 = tree.xpath(f"/html/body/div[2]/div/div[2]/div/div[1]/div[1]/div[2]/div[{index}]/div[1]/h3")
            if p1:
                col_name = p1[0].text.strip()     
                xpath = self.xpath_match(col_name, index)
                data_dict[col_name] = []
            else:
                continue
            if not xpath:
                print(i, "no xpath")
                continue
            p2 = tree.xpath(xpath)
            for n in p2:
                data_dict[col_name].append(n.text.strip())
        
        #條件要求
        language = tree.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[2]/div/p")
        if not language[0].text: #代表並非"不拘"
            language_set = []
            language_set_e = tree.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[4]/div[2]/div//*/a/u")
            for n in language_set_e:
                language_set.append(n.text)
        else:
            language_set = "不拘"
        data_dict["語文條件"] = self.list2string(language_set)

        for index in range(10):
            p1 = tree.xpath(f"/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/div[{index}]/div[1]/h3")
            if p1:
                col_name = p1[0].text.strip()
                if col_name not in data_dict.keys(): #避免蓋掉已經存在的部分
                    data_dict[col_name] = []
                xpath = self.xpath_match(col_name, index)
            else:
                continue
            if not xpath:
                continue
            p2 = tree.xpath(xpath)
            for n in p2:
                data_dict[col_name].append(n.text.strip())
        
        other_requirements = tree.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/div/div[2]/div/div/p")


        #福利相關
        for index in range(1,8):
            p1 = tree.xpath(f"/html/body/div[2]/div/div[2]/div/div[1]/div[4]/div[{index}]/div/h3")
            if p1:
                col_name = p1[0].text.strip()
                data_dict[col_name] = []
                xpath = self.xpath_match(col_name, index)
            else:
                continue
            if not xpath:
                print(f"{col_name}: no xpath")
                continue
            p2 = tree.xpath(xpath)
            for n in p2:
                data_dict[col_name].append(n.text.strip())
        
        recruit_incentives = tree.xpath("/html/body/div[2]/div/div[2]/div/div[1]/div[4]/div[6]/div/p")#div6
        if recruit_incentives:
            data_dict["招募福利"] = recruit_incentives[0].text

        return data_dict

    def find_jobs(self, max_jobs = -1):
        #爬取所有頁面的資料
        if max_jobs == -1:
            max_jobs = self.job_links.shape[0]
        data = []
        for i in range(self.job_links.shape[0]):
            company = self.job_links["公司名稱"].iloc[i]
            job = self.job_links["職缺名稱"].iloc[i]
            url = self.job_links["職缺連結"].iloc[i]
            dict_data_jobs = {
                "公司名稱" : company,
                "職缺名稱" : job,
                "職缺連結" : url
            }
            try:
                job_data = self.creep_job(url)
                job_data = {**dict_data_jobs, **job_data}
                data.append(job_data)
                print(f"正在爬取第{i+1}/{min(self.job_links.shape[0], max_jobs)}個工作")
            except KeyboardInterrupt:
                break
            except:
                continue
            if i == max_jobs-1:
                break        
        df = pd.DataFrame(columns = data[0].keys(), data = data)
        self.jobs = df
        print("資料已爬取完畢，請用self.jobs檢視資料或以save_jobs儲存檔案")
        return self.jobs
    
    def save_jobs(self):
        if self.jobs is None:
            print("尚未爬取職位資料，請先find jobs")
            return
        for column in self.jobs.columns:
            self.jobs[column] = self.jobs[column].apply(self.list2string)
        path = self.keyword + r"-職位資料爬蟲.xlsx"
        self.jobs.to_excel(path, index = False)
        print(f"{path}資料已儲存")
           
if __name__ == "__main__":
    keyword = "影像數據分析"
    jobs = Jobs(keyword)
    jobs.search_jobs(max_pages = 2)
    jobs.find_jobs()
    jobs.save_jobs()
    
