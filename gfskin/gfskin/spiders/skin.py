from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from requests import get
from pathlib import Path




class SkinSpider(CrawlSpider):
    name = "skin"
    allowed_domains = ["gamepress.gg"]
    start_urls = ["https://gamepress.gg/girlsfrontline/t-doll-costumes-list"]
    rules = (
        Rule(LinkExtractor(allow='t-doll-costumes-list', deny="cas"), callback='parse_image'),
        Rule(LinkExtractor(allow='t-doll-costumes-list')),
    )

    def parse_image(self, response):
        image_list1 = response.css("div.costume-normal.costume-image.show-expl img::attr(src)").getall()
        image_list2 = response.css("div.costume-damaged.costume-image.show-expl img::attr(src)").getall()
        root_dir = Path("girls_frontline_skin")
        if not root_dir.exists():
            root_dir.mkdir()
        for (image_name1, image_name2) in zip(image_list1, image_list2):
            link1 = "https://gamepress.gg" + f"{image_name1}"
            link2 = "https://gamepress.gg" + f"{image_name2}"

            save_path1 = root_dir / f"{image_name1.split('/')[-1]}"
            save_path2 = root_dir / f"{image_name2.split('/')[-1]}"

            if not save_path1.exists():
                image1 = get(link1)
                with open(save_path1, "wb") as file:
                    file.write(image1.content)

            if not save_path2.exists():
                image2 = get(link2)
                with open(save_path2, "wb") as file:
                    file.write(image2.content)