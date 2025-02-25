class PerformanceAnalyzer:
    def __init__(self, seo_tips):
        self.seo_tips = seo_tips

    def process_html(self, soup):
        res = {
            'schema': self.process_schema(soup),
            'amp': self.process_amp(soup),
        }

        return res

    def process_schema(self, soup):
        result = {
            'name': 'Script:schema',
            'data': '',
            'tip': self.seo_tips['schema']
        }

        json_schema = soup.find('script', attrs={'type': 'application/ld+json'})
        if not json_schema:
            result['msg'] = "Your site has not tag script schema."
            result['status'] = False
        else:
            result['msg'] = "Your site has script schema."
            result['status'] = True

        return result

    def process_amp(self, soup):
        result = {
            'name': 'AMP',
            'data': '',
            'tip': self.seo_tips['AMP']
        }

        check_doctype = ('<!doctype html>' in str(soup)) or ('<!DOCTYPE html>' in str(soup))

        check_head = (soup.find('head')) is not None
        check_body = (soup.find('body')) is not None

        check_charset = (soup.find('meta', attrs={'charset': True})) is not None

        check_amp = (soup.find('style', attrs={'amp-boilerplate': True})) is not None
        check_amp_2 = (soup.find('link', attrs={'rel': 'amphtml'})) is not None

        check_canonical = (soup.find('link', attrs={'rel': 'canonical'})) is not None
        check_viewport = (soup.find('meta', attrs={'name': 'viewport'})) is not None
        if all([
            check_doctype, check_head, check_body, check_charset, (check_amp or check_amp_2), check_canonical,
            check_viewport]
        ):
            result['msg'] = "Your site is friendly with AMP"
            result['status'] = True
        else:
            result['msg'] = "Your site isn\'t friendly with AMP"
            result['status'] = False

        return result