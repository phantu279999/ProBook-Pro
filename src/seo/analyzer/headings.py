class HeadingsAnalyzer:
    def __init__(self, seo_tips):
        self.seo_tips = seo_tips

    def process_html(self, soup):
        res = {
            'headings': self.process_headings(soup),
        }
        return res

    def process_headings(self, soup):
        result = {
            'name': 'Headings',
            'type_data': 'dict',
            'tip': self.seo_tips['headings']
        }
        list_h1 = [it.text for it in soup.find_all("h1")]
        list_h2 = [it.text for it in soup.find_all("h2")]
        list_h3 = [it.text for it in soup.find_all("h3")]
        list_h4 = [it.text for it in soup.find_all("h4")]
        list_h5 = [it.text for it in soup.find_all("h5")]
        list_h6 = [it.text for it in soup.find_all("h6")]

        if len(list_h1) == 0:
            result['msg'] = "Your website is not found tag h1"
            result['status'] = False
        elif len(list_h1) > 1:
            result['msg'] = "Your web site have greater than 1 tag h1. Optimal a page should contain only 1 tag h1"
            result['status'] = False
        elif len(list_h2) == 0:
            result['msg'] = "Your website is not found tag h2"
            result['status'] = False
        else:
            result['msg'] = 'Your website had optimal tag h1'
            result['status'] = True
        result['data'] = {
            'h1': list_h1, 'h2': list_h2, 'h3': list_h3, 'h4': list_h4, 'h5': list_h5, 'h6': list_h6,
        }
        return result
