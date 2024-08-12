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

action = {
	"News": {
		"query": ("""SELECT id, title, sapo, url, avatar, date_create, status, is_home, is_focus, created_by, 
		edited_by FROM news_news ORDER BY date_create DESC LIMIT 1000;""", []),
		"key_redis": [
			{
				"type": "sorted",
				"key": ("news", []),
				"item": ('news:pk{}', ['id']),
				"score": "date_create",
				"obj": "item"
			}
		]
	},
	"NewsDetail": {
		"query": ("""SELECT id, title, sapo, url, avatar, date_create, status, is_home, is_focus, created_by, 
		edited_by FROM news_news WHERE id = {};""", ["id"]),
		"key_redis": [
			{
				"type": "string",
				"key": ("news:pk{}", ['id']),
				"item": ("*", []),
				"obj": "item"
			}
		]
	},
	"NewsContent": {
		"query": ("SELECT id, body, newsid_id FROM news_newscontent WHERE newsid_id = {};", ['newsid_id']),
		"key_redis": [
			{
				"type": "hash",
				"key": ("newscontent", []),
				"field": ("news:pk{}", ["newsid_id"]),
				"item": ("{}", ["body"]),
				"obj": "item"
			}
		]
	},
	"Category": {
		"query": ("SELECT * FROM news_category;", []),
		"key_redis": [
			{
				"type": "string",
				"key": ("categories", []),
				"item": ("*", []),
				"obj": "all"
			}
		]
	},
	"CategoryNews": {
		"query": ("""SELECT  nc.categoryid_id, nc.newsid_id, n.date_create FROM news_categorynews nc
					INNER JOIN news_news n ON n.id = nc.newsid_id
					WHERE categoryid_id = {};""", ["categoryid_id"]),
		"key_redis": [
			{
				"type": "sorted",
				"key": ("newsincate:pk{}", ['categoryid_id']),
				"item": ('news:pk{}', ['newsid_id']),
				"score": "date_create",
				"obj": "item"
			}
		]
	},
	"Tag": {
		"query": ("SELECT * FROM news_tag;", []),
		"key_redis": [
			{
				"type": "string",
				"key": ("tags:id{}", ['id']),
				"item": ("*", []),
				"obj": "item"
			},
			{
				"type": "string",
				"key": ("tags:url{}", ['url']),
				"item": ("*", []),
				"obj": "item"
			}
		]
	},
	"TagNews": {
		"query": (
			"""SELECT tn.tagid_id, tn.newsid_id, t.created_date FROM news_tagnews tn
				INNER JOIN news_tag t ON t.id = tn.tagid_id
				WHERE tn.tagid_id = {};""", ["tagid_id"]
		),
		"key_redis": [
			{
				"type": "sorted",
				"key": ("newsintag:tagid{}", ['tagid_id']),
				"item": ('news:pk{}', ['newsid_id']),
				"score": "created_date",
				"obj": "item"
			},
			{
				"type": "sorted",
				"key": ("newsintag:newsid{}", ['newsid_id']),
				"item": ('tags:id{}', ['tagid_id']),
				"score": "created_date",
				"obj": "item"
			},
		]
	},
	"Topic": {},
	"TopicNews": {},
}
