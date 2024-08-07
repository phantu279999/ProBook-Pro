# ProBook(Project Tool)

This project is a web application integrate tools (like: Check SEO, Crawl Video Channel Youtube, etc...)

## MAIN APP
Manage tools in my website

#### TOOL Check SEO
<img src="https://raw.githubusercontent.com/phantu279999/ProBook-Pro/master/media/helper/interface_seo.png">

#### TOOL Crawl VideoChannel Youtube
<img src="https://raw.githubusercontent.com/phantu279999/ProBook-Pro/master/media/helper/interface_video_youtube.png">



## NEWS APP
This application manages posts, and it uses the Redis cache layer

```bash
  |MODEL| ----> |SERVICE| -----> update data redis
```

When updating a model, it will be stored in the Redis queue, and there is a service that retrieves the data in the Redis queue and updates accordingly to that model.