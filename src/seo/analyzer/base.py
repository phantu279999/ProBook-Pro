import os
import sys
import traceback
import validators
import requests
from bs4 import BeautifulSoup

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(project_root)

from src.common.log_base import BaseLogger
from src.seo import config

from src.seo.analyzer.meta import MetaAnalyzer
from src.seo.analyzer.headings import HeadingsAnalyzer
from src.seo.analyzer.technical import TechnicalAnalyzer
from src.seo.analyzer.links import LinkAnalyzer
from src.seo.analyzer.performance import PerformanceAnalyzer
from src.seo.analyzer.images import ImagesAnalyzer

logger = BaseLogger(name='ProcessSEO', log_file=project_root + "\\logs\\proccess-seo.log")


class BaseSEO:

    def __init__(self):
        self.seo_tips = config.seo_tips

        self.meta = MetaAnalyzer(self.seo_tips)
        self.heading = HeadingsAnalyzer(self.seo_tips)
        self.technical = TechnicalAnalyzer(self.seo_tips)
        self.link = LinkAnalyzer(self.seo_tips)
        self.performance = PerformanceAnalyzer(self.seo_tips)
        self.image = ImagesAnalyzer(self.seo_tips)

    def process_link(self, link):
        try:
            response = requests.get(link)
            if response.status_code == 200:
                return self.process_html(response.text, link)
        except Exception as e:
            print(traceback.format_exc())
            print("Error:", e)
        finally:
            logger.info(f"Process {link = } finished")

    def process_html(self, html, link):
        soup = BeautifulSoup(html, 'html.parser')
        res = {
            'url': self.process_url(link),
            'frames': self.process_frames(soup),
            'language': self.process_language(soup),
            'doctype': self.process_doctype(soup),
            'favicon': self.process_favicon(soup)
        }

        res = {**res, **self.technical.process_html(soup, link)}

        for process in [self.meta, self.heading, self.link, self.performance, self.image]:
            res = {**res, **process.process_html(soup)}
        return res

    def process_url(self, domain):
        result = {
            'name': 'URL',
            'tip': self.seo_tips['url']
        }
        if '_' in domain:
            result['msg'] = "Đường dẫn của trang có chứa ký tự '_'"
            result['status'] = False
        elif ' ' in domain:
            result['msg'] = "Đường dẫn của trang có chứa ký tự 'khoảng trắng'"
            result['status'] = False
        elif validators.url(domain) is False:
            result['msg'] = "Đường dẫn có thể không thân thiện với người dùng"
            result['status'] = False
        else:
            result['msg'] = "Đường dẫn thân thiện"
            result['status'] = True
        result['data'] = domain
        return result

    def process_frames(self, soup):
        result = {
            'name': 'Iframe',
            'data': '',
            'tip': self.seo_tips['frames']
        }

        check = soup.find_all("iframe")
        if check:
            result[
                'msg'] = f"Trang của bạn có {len(check)} thẻ iframe. Thông thường đây không phải là vấn đề đối với SEO nếu chúng được sử dụng đúng cách."
            result['status'] = False
        else:
            result["msg"] = "Trang web của bạn không có thẻ iframe."
            result["status"] = True

        return result

    def process_language(self, soup):
        result = {
            'name': 'Language',
            'tip': self.seo_tips['language']
        }

        check = soup.find('html').get("lang", "")
        if not check:
            result['msg'] = "Thẻ html không có thuộc tính 'lang'"
            result['status'] = False
        else:
            result['msg'] = "Thẻ html có thuộc tính 'lang'"
            result['status'] = True
        result['data'] = check
        return result

    def process_doctype(self, soup):
        result = {
            'name': 'Doctype',
            'data': "",
            'tip': self.seo_tips['doctype']
        }

        check_doctype = ('<!doctype html>' in str(soup)) or ('<!DOCTYPE html>' in str(soup))
        if not check_doctype:
            result['msg'] = "Không tìm thấy thẻ <!DOCTYPE html> trong trang web của bạn"
            result['status'] = False
        else:
            result['msg'] = "Passed"
            result['status'] = True

        return result

    def process_favicon(self, soup):
        result = {
            'name': 'Icon favicon',
            'tip': self.seo_tips['favicon']
        }

        for link in soup.head.find_all('link'):
            if 'icon' in link['rel']:
                result['msg'] = 'Trang web của bạn có thẻ favicon'
                result['status'] = True
                result['data'] = link.get('href', '')
                break
        else:
            result['msg'] = 'Trang web của bạn không có thẻ favicon'
            result['status'] = False
            result['data'] = ""
        return result
