from pathlib import Path

import scrapy
import re
from mhscrape.items import Monster

def content_filter(items, default):
    return [item for item in items if item.strip() and item not in [default]]

def generation_object(data, object_name):
    cleaned_data = [item.strip() for item in data if item.strip()]
    data_object = []
    i = 0
    while i < len(cleaned_data):
        if i < len(cleaned_data) - 3 and cleaned_data[i + 1] == '(':
            match = re.search(r'\d+', cleaned_data[i + 2])  # Extracts '3' from '3rd Gen'
            generation = match.group() if match else None
            data_object.append({f"{object_name}": cleaned_data[i], "generation": generation})  # Store ailment with extracted generation
            i += 4  # Skip processed elements
        else:
            data_object.append({f"{object_name}": cleaned_data[i], "generation": None})  # Ailment without generation condition
            i += 1

    return data_object

def clean_paragraphs(data):
    return " ".join(data).strip().replace('\n', '').replace(' .', '.').replace(' ,', ',').replace('  ', ' ') if data else None

def clean_table(data):
    clean_data = [cell.strip() for cell in data if cell.strip()]
    if not clean_data:
        return []
    
    headers = []
    for i, cell in enumerate(clean_data):
        if all(len(word) > 1 for word in cell.split()):
            headers.append(cell)
        else:
            break
    
    data_rows = clean_data[len(headers):]

    rows = []
    row_length = len(headers)
    for i in range(0, len(data_rows), row_length):
        row = data_rows[i:i + row_length]

        while len(row) < row_length:
            row.append(None)
        row_dict = dict(zip(headers, row))
        rows.append(row_dict)
    
    return rows

def generation_convert_to_num(data):
    ordinal_map = {
        "First": 1,
        "Second": 2,
        "Third": 3,
        "Fourth": 4,
        "Fifth": 5,
        "Sixth": 6,
        "Seventh": 7,
    }
    # Only returning the first element, since it will be the lowest generation that it was introduced- can say 'greater than 1st gen' essentially
    return ordinal_map.get(data[0], 0) 

class MonsterSpider(scrapy.Spider):
    name = "monsters"

    def start_requests(self):
        urls = [
            "https://monsterhunter.fandom.com/wiki/Rathalos",
            "https://monsterhunter.fandom.com/wiki/Rathian",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = Monster()

        item["en_name"] = response.css("h2[data-source='Name']::text").get()
        item["jp_name"] = response.css("rb[lang='ja-Hani']::text").get()
        item["en_title"] = content_filter(response.css("div[data-source='English Title'] *::text").getall(), 'English Title')
        item["monster_class"] = content_filter(response.css("div[data-source='Monster Type'] *::text").getall(), 'Monster Class')
        item["elements"] = generation_object(content_filter(response.css("div[data-source='Element'] *::text").getall(), 'Elements'), 'element')
        item["ailments"] = generation_object(content_filter(response.css("div[data-source='Ailments'] *::text").getall(), 'Ailments'), 'ailment')
        item["weakest_to_elements"] = generation_object(content_filter(response.css("div[data-source='Weakest to'] *::text").getall(), 'Weakest to'), 'weakest_to')
        item["habitats"] = content_filter(response.css("div[data-source='Habitats'] *::text").getall(), 'Habitat')
        item["generation"] = generation_convert_to_num(content_filter(response.css("div[data-source='Generation'] *::text").getall(), 'Generation'))

        physiology = clean_paragraphs(response.xpath("//h2[span[@id='Physiology']]//following-sibling::p[1]//text()").getall())
        if physiology:
            item["physiology_desc"] = physiology

        abilities = clean_paragraphs(response.xpath("//h2[span[@id='Abilities']]//following-sibling::p[1]//text()").getall())
        if abilities:
            item["abilities_desc"] = abilities

        behavior = clean_paragraphs(response.xpath("//h2[span[@id='Behavior']]//following-sibling::p[1]//text()").getall())
        if behavior:
            item["behavior_desc"] = behavior

        habitat = clean_paragraphs(response.xpath("//h2[span[@id='Habitat']]//following-sibling::p[1]//text()").getall())
        if habitat:
            item["habitat_desc"] = habitat
        
        item["games"] = content_filter(response.xpath("//h3[span[@id='Main_Series']]//following-sibling::ul[1]//text()").getall(), '(Introduced)')

        item["item_effectiveness"] = clean_table(response.xpath("//h3[span[@id='MHW_Damage_Effectiveness']]//following-sibling::table[1]//text()").getall())

        yield item
        # page = response.url.split("/")[-2]
        # filename = f"monsters-{page}.html"
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")

# response.css("div::attr(data-source)").getall() <- this will return what the attributes are named, but not the content inside of them
