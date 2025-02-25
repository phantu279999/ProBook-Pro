class MetaAnalyzer:
    def __init__(self, seo_tips):
        self.seo_tips = seo_tips

    def process_html(self, soup):
        res = {
            'title': self.check_title(soup),
            'meta_description': self.check_meta_desc(soup),
            'meta_keywords': self.process_meta_keywords(soup),
            'revisit_after': self.process_revisit_after(soup),
            'op': self.process_open_graph(soup),
            'viewport': self.process_meta_viewport(soup)
        }

        return res

    def check_title(self, soup):
        result = {
            'name': 'Title',
            'tip': self.seo_tips['title'],
        }
        check = soup.find('title')
        if not check:
            result['msg'] = "Your website is not title."
            result['status'] = False
            result['data'] = ""
        else:
            text = check.text
            if 10 < len(text) < 70:
                result['msg'] = "Your title is {} characters. It is optimal".format(len(text))
                result['status'] = True
            else:
                result['msg'] = "Title of your website is greater than 70 characters"
                result['status'] = False
            result['data'] = text
        return result

    def process_meta_viewport(self, soup):
        result = {'name': 'Meta Viewport', 'tip': self.seo_tips['viewport']}

        check = soup.find('meta', attrs={'name': 'viewport'})
        if not check:
            result['msg'] = "Your site has not tag meta viewport"
            result['status'] = False
            result['data'] = ''
        else:
            content = check.get("content", "")
            if not content:
                result['msg'] = "Your tag viewport has not attribute content"
                result['status'] = False
            else:
                result['msg'] = "Your tag viewport is legal"
                result['status'] = True
            result['data'] = content
        return result

    def check_meta_desc(self, soup):
        result = {
            'name': 'Meta Description',
            'tip': self.seo_tips['meta_description']
        }
        text = soup.find('meta', attrs={'name': "description"})
        if not text:
            result['msg'] = "Your website is not tag 'Meta description'. Please check"
            result['status'] = False
            result['data'] = ""
        else:
            content = text.attrs.get('content', "")
            if 10 < len(content) < 250:
                result['msg'] = "Your meta description is {} characters. It is optimal".format(len(text))
                result['status'] = True
            elif 'content' not in text.attrs:
                result['msg'] = "Meta description is not attribute content"
                result['status'] = False
            else:
                result['msg'] = "Meta description content is greater than 250 characters"
                result['status'] = False
            result['data'] = content
        return result

    def process_meta_keywords(self, soup):
        result = {'name': 'Meta Keywords', 'tip': self.seo_tips['meta_keywords']}

        check = soup.head.find("meta", attrs={"name": "keywords"})
        if not check:
            result['msg'] = "Your website is not found Tag \'meta:keywords\'"
            result['status'] = False
            result['data'] = ""
        else:
            content = check.get("content", "")
            result['data'] = content
            if not content:
                result['msg'] = "Tag \'meta:keywords\' is not attribute 'content'"
                result['status'] = False
            else:
                result['msg'] = "Tag \'meta:keywords\' is passed"
                result['status'] = True
        return result

    def process_revisit_after(self, soup):
        result = {'name': 'Meta:Revisit After', 'tip': self.seo_tips['revisit_after']}
        check = soup.head.find('meta', attrs={"name": 'revisit-after'})
        if check:
            content_revisit = check.get("content", "")
            result['data'] = content_revisit
            if not content_revisit:
                result['msg'] = 'Your meta revisit-after has not attribute \'content\''
                result['status'] = False
            else:
                result['msg'] = 'Passed'
                result['status'] = True
        else:
            result['msg'] = "Not found tag meta revisit-after in your site"
            result['status'] = False
            result['data'] = ""
        return result

    def process_open_graph(self, soup):
        result = {'name': 'Open Graph', 'type_data': 'list', 'tip': self.seo_tips['open_graph']}

        open_graph = [
            [a["property"].replace("og:", ""), a.get("content", "")] for a in soup.select("meta[property^=og]")
        ]
        if not open_graph:
            result['msg'] = "Your site has not tag Open Graph"
            result['status'] = False
        else:
            result['msg'] = "Your site has tag Open Graph"
            result['status'] = True
        result['data'] = open_graph
        return result
