class ImagesAnalyzer:
    def __init__(self, seo_tips):
        self.seo_tips = seo_tips

    def process_html(self, soup):
        res = {
            'images': self.process_images(soup),
        }
        return res

    def process_images(self, soup):
        result = {
            'name': 'Images',
            'type_msg': 'list',
            'type_data': 'list',
            'data': [],
            'tip': self.seo_tips['images']
        }
        list_msg = []
        list_images = soup.body.find_all("img", src=True)
        for img in list_images:
            if not img.get("alt", ""):
                list_msg.append(f"Image({img['src']}) is have not attribute \'alt\'")
            result['data'].append(img['src'])

        if list_msg:
            result['msg'] = list_msg
            result['status'] = False
        else:
            result['msg'] = ['All images have \'alt\' attribute.']
            result['status'] = True

        return result