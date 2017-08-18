import os
import errno

import urlparse
import scrapy

from scrapy.http import Request

class paper_spider(scrapy.Spider):
    name = "paper_spider"

    allowed_domains = ["thecvf.com"]
    root_urls = "http://openaccess.thecvf.com/content_cvpr_2017/"
    root_dir = "../retrieves/"
    schedule_urls = "http://cvpr2017.thecvf.com/program/main_conference/"#program/main_conference#program_schedule.html"
    start_urls = ["http://openaccess.thecvf.com/content_cvpr_2017/papers/"]

    def parse(self, response):
        # Download papers       
        # Download supplementaries
        # Download htmls
        # Download csv files
        
        quest_list = [ 'cvpr papers', 'supplementaries', 'paper briefs', 'csv files', 'schedule files']

        suffix_map = { 'cvpr papers'     : ('paper.pdf'), \
                       'supplementaries' : ('supplemental.pdf.pdf', 'supplemental.zip.zip'), \
                       'paper briefs'    : ('paper.html'), \
                       'csv files'       : ('.csv'), \
                       'schedule files'  : ('.schedule.html') \
                     }
        
        url_map    = { 'cvpr papers'     : self.root_urls + "papers/", \
                       'supplementaries' : self.root_urls + "supplemental/", \
                       'paper briefs'    : self.root_urls + "html/", \
                       'csv files'       : self.root_urls + "", \
                       'schedule files'  : self.schedule_urls \
                     }
        
        dir_map    = { 'cvpr papers'     : self.root_dir + 'papers/', \
                       'supplementaries' : self.root_dir + 'supplemental/', \
                       'paper briefs'    : self.root_dir + 'html/', \
                       'csv files'       : self.root_dir, \
                       'schedule files'  : self.root_dir  \
                     }

        for quest in quest_list:
            request = Request(url_map[quest], callback = self.do_quest)
            request.meta['limitation'] = 0
            request.meta['url'] = url_map[quest]
            request.meta['dir'] = dir_map[quest]
            request.meta['suffix'] = suffix_map[quest]

            if quest == 'schedule files':
                request.meta['type'] = 'save'
            else:
                request.meta['type'] = 'download'

            yield request


    
    def do_quest(self, response):
        
        limitation = (int)(response.meta['limitation'])
        src_url = response.meta['url']
        dst_dir = response.meta['dir']
        wanted_suffix = response.meta['suffix']
        quest_type = response.meta['type']

        if not os.path.exists(dst_dir):
            try:
                os.makedirs(dst_dir)
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

        catched_time = 0

        if (quest_type == 'download'):
            for a in response.xpath('//a[@href]/@href'):
                link = a.extract()
                if link.endswith(wanted_suffix):
                    
                    is_searched = False

                    for root, dirs, files in os.walk(dst_dir):
                        if link in files:
                            is_searched = True
                            break

                    if is_searched:
                        continue

                    catched_time = catched_time + 1
                    if limitation != 0 and catched_time > limitation:
                        break
                    link = urlparse.urljoin(src_url, link)
                    request = Request(link, callback = self.save_file)
                    request.meta['dir'] = dst_dir
                    yield request

        else:
            for a in response.xpath('//table'):
                link = a.extract()
                if link.endswith("</table>"):
                    with open(dst_dir + "table_file"+(str)(catched_time)+wanted_suffix, 'wb') as f:
                        f.write(link.encode('utf-8'))


    def save_file(self, response):
        dst_dir = response.meta['dir']
        path = response.url.split('/')[-1]
        with open(dst_dir + path, 'wb') as f:
            f.write(response.body)
