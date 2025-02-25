import requests
from urllib.parse import urlparse


class TechnicalAnalyzer:
    def __init__(self, seo_tips):
        self.seo_tips = seo_tips

    def process_html(self, soup, link):
        res = {
            'robots_txt': self.process_robots_txt(link),
            'sitemaps': self.process_xml_sitemaps(link),
            'canonical': self.process_canonical(soup),
        }

        return res

    def process_robots_txt(self, domain):
        result = {
            'name': 'Robots TXT',
            'data': '',
            'tip': self.seo_tips['robots_txt']
        }

        if urlparse(domain).path == "/" and requests.head(domain + '/robots.txt').status_code != 200:
            result['msg'] = 'Your site has not file robots.txt'
            result['status'] = False
        else:
            result['msg'] = "Your site has file robots.txt"
            result['status'] = True

        return result

    def process_xml_sitemaps(self, domain):
        result = {
            'name': 'XML Sitemap',
            'data': "",
            'tip': self.seo_tips['xml_sitemaps']
        }

        url = domain.strip("/") + "/sitemap.xml"
        if urlparse(domain).path == "/" and requests.head(url).status_code != 200:
            result['msg'] = "Your site has not file sitemap.xml"
            result['status'] = False
        else:
            result['msg'] = "Your site has file sitemap.xml"
            result['status'] = True

        return result

    def process_canonical(self, soup):
        result = {
            'name': 'Canonical',
            'tip': self.seo_tips['canonical']
        }

        check = soup.head.find("link", attrs={"rel": "canonical"})
        if not check:
            result['msg'] = "Tag Canonical is not found"
            result['status'] = False
            result['data'] = ""
        else:
            get_url = check.get("href", "")
            result['data'] = get_url
            if not get_url:
                result['msg'] = "Tag Canonical is not attribute \'href\'"
                result['status'] = False
            elif 'http' not in get_url:
                result['msg'] = "Tag Canonical href is not contain link please add link start \'http\'(Full link)"
                result['status'] = False
            else:
                result['msg'] = 'A canonical tag is set for this page and the link is working fine'
                result['status'] = True
        return result