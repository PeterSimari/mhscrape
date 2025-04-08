from pathlib import Path

import scrapy
import re
from mhscrape.items import Skill, Levels, Stats

class SkillsSpider(scrapy.Spider):
    name = "skills"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_id = 0

    def start_requests(self):
        urls = [
            "https://mhwilds.kiranico.com/data/skills"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        skill_sections = response.xpath("//h3/following-sibling::div/table")
        for section in skill_sections:
            rows = section.xpath(".//tr")
            section_type = section.xpath("preceding::h3[1]/text()").get()
            for skill in rows:
                item = Skill()
                item["id"] = self.item_id
                item["type"] = section_type
                item["name"] = skill.xpath(".//td[1]/a/span/text()").get()
                if skill.xpath(".//td[2]/span/text()").get():
                    item["description"] = skill.xpath(".//td[2]/span/text()").get()
                else:
                    item["description"] = skill.xpath(".//td[2]/div/text()").get()
                relative_url = skill.xpath(".//td[1]/a/@href").get()
                if relative_url:
                    url = response.urljoin(relative_url)
                    yield response.follow(url, self.parse_skill_page, meta={"item": item})
                else:
                    yield item
                self.item_id += 1
            

    def parse_skill_page(self, response):
        item = response.meta["item"]
        levels = []
        level_rows = response.xpath("//h2/following::table[1]/tbody/tr")
        for entry in level_rows:
            level = Levels()
            level["level"] = entry.xpath(".//td[1]/span/text()").get()[2:]
            level["description"] = entry.xpath(".//td[3]/span/text()").get()
            # stats = [Stats()] 
            
            #only if it has numbers... if not, just keep it as the description of the skill. that should be enough for us to go off of. i guess.
            # if entry.xpath(".//td[3]/span/text()").get().contains("+"):
            #     match = re.match(r"(?P<type>\w+)\s+\+(?P<multiplier>\d+)%\s+Bonus:\s+\+(?P<buff>\d+)", entry.xpath(".//td[3]/span/text()"))
            #     if match:
            #         stats["type"] = match.group("type")
            #         stats["buff"] = match.group("buff")
            #         stats["multiplier"] = match.group("multiplier")
            
            # level["stats"] = stats
            levels.append(level)
            item["levels"] = levels

        print("YURRR")
        yield item
