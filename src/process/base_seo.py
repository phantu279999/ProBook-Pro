from bs4 import BeautifulSoup


class BaseSEO:

	def __init__(self):
		...

	def process_html(self, html):
		soup = BeautifulSoup(html, 'html.parser')
		self.check_title(soup)
		self.check_meta_desc(soup)

	def check_title(self, soup):
		res = {}
		text = soup.find('title').text
		if 10 < len(text) < 70:
			res['msg'] = "Your title is {} characters. It is optimal".format(len(text))
			res['status'] = True
		else:
			res['msg'] = "Title of your website is greater than 70 characters"
			res['status'] = False
		return res

	def check_meta_desc(self, soup):
		res = {}
		text = soup.find('meta', attrs={'name': "description"})
		if not text:
			res['msg'] = ""
			res['status'] = False
			return res
		if 10 < len(text.attrs['content']) < 250:
			res['msg'] = ""
			res['status'] = True
		else:
			res['msg'] = ""
			res['status'] = False

		return res

	@staticmethod
	def process_url(soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Công cụ tìm kiếm và khách truy cập có thể tương tác với trang web của bạn hiệu quả hơn khi bạn sử dụng 
	        URL mô tả nội dung của trang (ví dụ: http://www.company.com/companyinformation).
	        URL cực kỳ quan trọng đối với chiến dịch SEO của bạn.
	        Đảm bảo sử dụng các URL giúp Google™ lập chỉ mục trang web của bạn dễ dàng.
	    """

		if '_' in domain:
			status = False
			msg = 'Trang web của bạn có chứa dấu gạch dưới \"_\"'
			print(msg)
		elif ' ' in domain:
			status = False
			msg = 'URL của bạn chứa khoảng trắng'
			print(msg)
		elif validators.url(domain) is False:
			status = False
			msg = 'URL của bạn không thân thiện'
			print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_canonical(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Thẻ liên kết chuẩn là một phần tử HTML giúp quản trị viên web ngăn chặn các vấn đề trùng
	        lặp nội dung bằng cách chỉ định phiên bản ''chuẩn'' hoặc ''ưa thích'' 
	        của trang web như một phần của tối ưu hóa công cụ tìm kiếm.
	     """
		check = soup.head.find("link", attrs={"rel": "canonical"})
		if not check:
			status = False
			msg = "Thẻ CANONICAL không tìm thấy ở trong head"
			print(msg)
		else:
			if not check.get("href", ""):
				status = False
				msg = "Thẻ canonical không có thuôc tính HREF"
				print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_title(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Tiêu đề trang hiệu quả nhất dài khoảng 10-70 ký tự, bao gồm cả khoảng trắng.
	        Giữ tiêu đề của bạn ngắn gọn và chắc chắn rằng chúng chứa các từ khóa tốt nhất của bạn .
	        Mỗi trang nên có tiêu đề độc quyền của riêng mình.
	        Công cụ nổi bật: Đây là công cụ tối ưu hóa đoạn trích cho phép bạn xem tiêu đề 
	        của mình trông như thế nào trên Google™ và các kết quả tìm kiếm khác.
	    """
		check = soup.head.title
		if not check:
			status = False
			msg = "Thẻ TITLE không có trong head"
			print(msg)
		else:
			if len(check) > 70:
				status = False
				msg = """
	            Nội dung của thẻ title của trang vượt qua 70 ký tự.
	             Giữ title ngắn gọn và chắc chắn chúng chứa từ khóa tốt nhất"""
				print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_meta_description(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Mô tả meta rất hữu ích vì chúng thường chỉ ra cách các trang của bạn được hiển thị trong kết quả tìm kiếm.
	        Để đạt hiệu quả tối ưu, mô tả meta phải dài từ 160-300 ký tự.
	        Mô tả meta của bạn phải ngắn gọn và chứa các từ khóa tốt nhất của bạn
	        Đảm bảo mỗi trang trên trang web của bạn có mô tả meta riêng.
	    """

		check = soup.head.find("meta", attrs={"name": "description"})
		if not check:
			status = False
			msg = "Thẻ META DESCRIPTION không có trong head"
			print(msg)
		else:
			if not check.get("content", ""):
				status = False
				msg = "Thẻ meta description không có thuộc tính CONTENT"
				print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_meta_keywords(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Từ khóa meta là những từ hoặc cụm từ liên quan đến nội dung trang web của bạn. 
	        Trước đây, mọi người đã cố gắng tận dụng thẻ này nên bây giờ nó không
	        ảnh hưởng đến thứ hạng tìm kiếm của bạn như trước đây.
	    """

		check = soup.head.find("meta", attrs={"name": "keywords"})
		if not check:
			status = False
			msg = "Thẻ META KEYWORDS không có trong head"
			print(msg)
		else:
			if not check.get("content", ""):
				status = False
				msg = "Thẻ meta keywords không có thuộc tính CONTENT"
				print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_headings(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Tiêu đề ban đầu (<H1>) nên bao gồm các từ khóa tốt nhất của bạn.
	        Chỉ sử dụng một tiêu đề <H1> trên mỗi trang sẽ củng cố SEO của bạn.
	    """
		list_h1 = soup.find_all("h1")

		if len(list_h1) == 0:
			status = False
			msg = "Trang web của bạn không có thẻ H1 nào."
			print(msg)
		elif len(list_h1) > 1:
			status = False
			msg = "Trang web của bạn có nhiều hơn 1 thẻ H1. Tối ưu nhất là một trang chỉ cần 1 thẻ H1"
			print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_images(self, soup, domain):
		result = dict()
		status = True
		list_msg = []
		tips = """
	        Chúng tôi khuyên bạn nên thêm văn bản ALT vào hình ảnh của mình
	        để các công cụ tìm kiếm lập chỉ mục chúng dễ dàng hơn.
	     """
		list_images = soup.body.find_all("img", src=True)
		for img in list_images:
			if not img.get("alt", ""):
				status = False
				msg = f"Image({img['src']}) không có thuộc tính ALT"
				print(msg)
				list_msg.append(msg)

		result["msg"] = list_msg
		result["status"] = status
		result["domain"] = [domain] * len(list_msg)
		result["tips"] = [tips] * len(list_msg)

		return result

	def process_frames(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = "Bạn nên tránh sử dụng các khung khi tối ưu hóa trang web của mình."

		check = soup.find_all("iframe")
		if check:
			status = False
			msg = f"Tìm thấy {len(check)} thẻ IFRAME lưu ý thẻ này sử dụng cẩn thận"
			print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_schema(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Sử dụng dữ liệu đánh dấu trên các trang web của bạn là một cách mạnh mẽ để tăng khả năng
	        hiển thị của bạn đối với các công cụ tìm kiếm và đạt được tỷ lệ nhấp chuột cao hơn,
	        từ đó có thể dẫn đến xếp hạng tốt hơn.
	    """
		json_schema = soup.find('script', attrs={'type': 'application/ld+json'})
		if not json_schema:
			status = False
			msg = "Tôi không tìm thấy thẻ schema nào trong trang. Vui lòng kiểm tra lại"
			print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_open_graph(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Giao thức Open Graph cho phép bất kỳ trang web nào trở thành một đối tượng phong phú trong biểu đồ xã hội.
	        Chẳng hạn, điều này được sử dụng trên Facebook để cho phép bất kỳ trang web nào có chức năng giống như 
	        bất kỳ đối tượng nào khác trên Facebook.
	    """

		open_graph = [[a["property"].replace("og:", ""), a.get("content", "")] for a in
					  soup.select("meta[property^=og]")]
		if not open_graph:
			status = False
			msg = "Trang của bạn không có thẻ Open Graph"
			print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_amp(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        AMP là một cách để tạo trang web cho nội dung tĩnh hiển thị nhanh.
	        AMP HTML là HTML có một số hạn chế về hiệu suất đáng tin cậy và một số 
	        tiện ích mở rộng để xây dựng nội dung phong phú ngoài HTML cơ bản.
	    """

		if urlparse(domain).path == "/":
			status = True
			data = requests.get(domain).content
			soup = BeautifulSoup(data, "html.parser")

			check_doctype = ('<!doctype html>' in str(soup)) or ('<!DOCTYPE html>' in str(soup))

			check_head = (soup.find('head')) is not None
			check_body = (soup.find('body')) is not None

			check_charset = (soup.find('meta', attrs={'charset': True})) is not None

			check_amp = (soup.find('style', attrs={'amp-boilerplate': True})) is not None
			check_amp_2 = (soup.find('link', attrs={'rel': 'amphtml'})) is not None

			check_canonical = (soup.find('link', attrs={'rel': 'canonical'})) is not None
			check_viewport = (soup.find('meta', attrs={'name': 'viewport'})) is not None
			if all([check_doctype, check_head, check_body, check_charset, (check_amp or check_amp_2), check_canonical,
					check_viewport]):
				print('Chúc mừng trang của bạn có phiên bản AMP hợp lệ')
			else:
				status = False
				msg = 'Có vẻ trang của bạn không có phiên bản AMP' \
					  '(giúp thiết bị di động được tăng tốc và giao diện đẹp hơn).'
				print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_meta_viewport(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Chế độ xem kiểm soát cách hiển thị trang web trên thiết bị di động.
	        Nếu không có chế độ xem, thiết bị di động sẽ hiển thị trang ở độ rộng màn hình máy tính để bàn thông thường, 
	        được điều chỉnh tỷ lệ để vừa với màn hình.
	        Đặt chế độ xem cho phép kiểm soát chiều rộng và tỷ lệ của trang trên các thiết bị khác nhau.
	    """

		check = soup.find('meta', attrs={'name': 'viewport'})
		if not check:
			status = False
			msg = "Trang của bạn không có thẻ viewport"
			print(msg)
		else:
			if check.get("content", ""):
				status = False
				msg = "Thẻ meta viewport của bạn không có thuộc tính CONTENT"
				print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_robots_txt(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Tệp này hạn chế hoạt động của trình thu thập thông tin của công cụ 
	        tìm kiếm và ngăn chúng truy cập vào các trang và thư mục nhất định.
	    """

		if urlparse(domain).path == "/":
			check_status = requests.get(domain + '/robots.txt')
			if check_status.status_code != 200:
				status = False
				msg = 'Trang của bạn hiện tại chưa có file robots.txt'
				print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_xml_sitemaps(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Sơ đồ trang web XML liệt kê các URL có thể được thu thập thông tin và có thể cung cấp các 
	        thông tin khác như tần suất bạn cập nhật, lần cập nhật cuối cùng của bạn diễn ra khi nào và tầm quan trọng.
	        Với sơ đồ trang web XML, các công cụ tìm kiếm có thể lập chỉ mục trang web của bạn chính xác hơn.
	        Mặc dù nó đã được tranh luận, nhưng chúng tôi khuyên bạn nên gửi sơ đồ trang 
	        web XML tới Công cụ quản trị trang web của Google™.
	    """

		if urlparse(domain).path == "/":
			if domain.endswith("/"):
				status_code = requests.get(domain + "sitemap.xml")
			else:
				status_code = requests.get(domain + "/sitemap.xml")

			if status_code != 200:
				status = False
				msg = "Có vẻ trang của bạn không có file SITEMAP XML. Vui lòng kiểm tra lại"
				print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_lang(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Dưới đây là một số gợi ý cho các trang web đa ngôn ngữ:
	        Bạn nên khai báo ngôn ngữ nội dung trong mã HTML của mỗi trang.
	    """

		check = soup.find('html').get("lang", "")
		if not check:
			status = False
			msg = "Thẻ html của bạn không có thuộc tính LANG"
			print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_doctype(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Việc chỉ định một loại tài liệu sẽ hỗ trợ trình duyệt web hiển thị chính xác nội dung của bạn.
	    """

		check_doctype = ('<!doctype html>' in str(soup)) or ('<!DOCTYPE html>' in str(soup))
		if not check_doctype:
			status = False
			msg = "Tôi không tìm thấy loại thẻ <!DOCTYPE html> chỉ định loại trang của bạn"
			print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result

	def process_favicon(self, soup, domain):
		result = dict()
		status = True
		msg = ""
		tips = """
	        Đảm bảo rằng biểu tượng yêu thích của bạn phản ánh thương hiệu của bạn .
	        Mẹo nổi bật: Nếu bạn muốn khách truy cập của mình có trải nghiệm tốt hơn, 
	        hãy xem biểu tượng yêu thích tuyệt vời này .
	    """

		for link in soup.head.find_all('link'):
			if 'icon' in link['rel']:
				break
		else:
			status = False
			msg = 'Trang của bạn không có thẻ FAVICON'
			print(msg)

		result["msg"] = msg
		result["status"] = status
		result["domain"] = domain
		result["tips"] = tips

		return result
