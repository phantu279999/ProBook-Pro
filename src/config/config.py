seo_tips = {
	"title": """The most effective page titles are about 10-70 characters long, including spaces.
	Keep your titles concise and make sure they contain your best keywords.""",
	"meta_description": "Meta descriptions are useful because they often dictate how your pages are shown in search results.",
	"url": "Search engines and visitors can interact with your website more effectively when you use URLs that describe the pages content (for example: http://www.company.com/companyinformation)",
	"canonical": "A canonical link tag is an HTML element that helps webmasters prevent duplicate content issues by specifying the ''canonical'' or ''preferred'' version of a webpage as part of search engine optimization.For more information, please see this Google article.",
	"meta_keywords": "",
	"revisit_after": "",
	"headings": """You can include keywords in your headings.
	The initial heading (<H1>) should include your best keywords.
	Using only one <H1> heading per page will strengthen your SEO.""",
	"images": "We suggest adding ALT text to your images so that it's easier for search engines to index them.",
	"frames": "It's hard for search engines to index pages with frames since it does not follow the standard layout for a website.",
	"schema": "Using markup data on your webpages is a powerful way to increase your visibility to search engines and gain higher click-through rates, which may in turn lead to better rankings.",
	"open_graph": "The Open Graph protocol enables any web page to become a rich object in a social graph. For instance, this is used on Facebook to allow any web page to have the same functionality as any other object on Facebook.",
	"AMP": "AMP is a way to build web pages for static content that render fast.",
	"viewport": "A viewport controls how a webpage is displayed on a mobile device. Without a viewport, mobile devices will render the page at a typical desktop screen width, scaled to fit the screen. Setting a viewport gives control over the page's width and scaling on different devices.",
	"robots_txt": "This file restricts the activity of search engine crawlers and stops them from accessing certain pages and directories.",
	"xml_sitemaps": "An XML sitemap lists URLs that can be crawled and may offer other information such as how often you update, when your last update occurred and importance.",
	"language": """Here are some suggestions for multilingual sites:

	⋅ You should declare the contents language in the HTML code of each page.
	⋅ You should also declare the language code in the URL (for example: company.com/es/contact.html).
	⋅ If you plan on building a multilingual site, refer to the tips found here""",
	"doctype": "Specifying a document type assists web browsers in displaying your content correctly",
	"favicon": "Featured tip: If you want a better experience for your visitors, have a look at this great favicon.",
}

config_mysql = {
	"host": "127.0.0.1",
	"port": 3306,
	"db": "probook",
	"username": "root",
	"password": "1234"
}

config_redis = {
	"host": "127.0.0.1",
	"port": 6379,
	"db": 2,
	"username": "",
	"password": ""
}

config_redis_queue = {
	"host": "127.0.0.1",
	"port": 6379,
	"db": 3,
	"username": "",
	"password": ""
}
