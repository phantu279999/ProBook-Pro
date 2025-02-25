class LinkAnalyzer:
    def __init__(self, seo_tips):
        self.seo_tips = seo_tips

    def process_html(self, soup):
        res = {
            'external_link': self.process_external_link(soup),
        }

        return res

    def process_external_link(self, soup):
        result = {
            'name': 'External Link',
            'msg': 'Passed',
            'type_data': 'list',
            'status': True
        }
        links = soup.body.find_all("a", href=True)

        list_external = []
        for link in links:
            if link['href'].startswith('http'):
                if link.get('rel', '') != 'nofollow':
                    result['msg'] = 'Link external should has attribute rel=nofollow'
                    result['status'] = False
                list_external.append(link['href'])
        result['data'] = list_external
        return result
