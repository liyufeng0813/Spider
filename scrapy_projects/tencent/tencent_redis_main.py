from scrapy import cmdline
from tencent import save_item


cmdline.execute("scrapy crawl tencent_redis".split())
save_item.save()
