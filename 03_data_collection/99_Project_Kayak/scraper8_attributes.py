# lit la liste des hotels dans hotels_list.json
# genère un fichier hotels_attributes avec une ligne d'attirbuts par hotel

import json
import re
from pathlib import Path
import logging
import scrapy
from scrapy.crawler import CrawlerProcess

import include_kayak as k

k_CurrentDir = Path(__file__).parent


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class OneHotelSpider(scrapy.Spider):
    name = "OneHotelSpider"
    # make the url are parsed in order
    # however we loose the // and it is sloooow
    # 1 min to get the attributes for 25 hotels
    # custom_settings = {
    #   'CONCURRENT_REQUESTS': '1'
    # }

    def start_requests(self):

        try:
            with open(k_CurrentDir / k.AssetsDir / k.HotelsListFile, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Are you sure the file {k.HotelsListFile} exists ?")

        hotel_rank = 0
        for entry in data:
            yield scrapy.Request(url=entry["url"], callback=self.parse, meta={"rank": hotel_rank})
            hotel_rank += 1

    def parse(self, response):

        # get back the rank of the hotel
        rank = response.meta.get("rank")

        # TODO this guys need a review. Indeed, I'm not these hard coded selectors will survive a long time
        # 07 04 2024
        # kScoreSelector = ".a3b8729ab1.d86cee9b25::text"
        # kDescription2Selector = (
        #     ".a53cbfa6de.b3efd73f69::text"  # <p data-testid="property-description" class="a53cbfa6de b3efd73f69">....
        # )
        # kLatLng = "div.hotel-sidebar-map hotel-sidebar-map-a11y a::attr(href)"  # <div class="hotel-sidebar-map hotel-sidebar-map-a11y">....

        # 19 08 2024
        # Check assets/kScoreSelector.png, kDescription2Selector.png and kLatLng.png to see from where the values below come from
        kScoreSelector = ".d0522b0cca.fd44f541d8::text"
        kDescription2Selector = ".e2585683de.c8d1788c8c::text"
        kLatLng = "a[data-atlas-latlng]::attr(data-atlas-latlng)"

        score = response.css(kScoreSelector).get().replace(",", ".")
        description = response.css(kDescription2Selector).get()

        # valeur de l'attribut 'data-atlas-latlng'
        latlng = response.css(kLatLng).get()
        latitude, longitude = latlng.split(",")
        # print(latitude, longitude)

        processed_data = {
            "rank": rank,
            "score": score,
            "latitude": latitude,
            "longitude": longitude,
            "description": description,
        }
        yield processed_data


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # If it exists delete previous version of scrapy log file
    log_file_path = k_CurrentDir / k.AssetsDir / k.ScrapyLogFile
    if log_file_path.exists():
        log_file_path.unlink()
    # if Path.exists(k_CurrentDir / k.AssetsDir / k.ScrapyLogFile):
    #     (k_CurrentDir / k.AssetsDir / k.ScrapyLogFile).unlink()

    # If it exists delete previous version of attributes attributes file
    attr_file_path = k_CurrentDir / k.AssetsDir / k.HotelsAttributes
    if attr_file_path.exists():
        attr_file_path.unlink()
    # if Path.exists(k_CurrentDir / k.AssetsDir / k.HotelsAttributes):
    #       (k_CurrentDir / k.AssetsDir / k.HotelsAttributes).unlink()

    process = CrawlerProcess(
        settings={
            "USER_AGENT": "Chrome/97.0",
            "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
            "FEEDS": {
                k_CurrentDir / k.AssetsDir / k.HotelsAttributes: {"format": "json"},
            },
            "LOG_STDOUT": False,
            "LOG_FILE": f"{k_CurrentDir}/{k.AssetsDir}/{k.ScrapyLogFile}",
        }
    )

    process.crawl(OneHotelSpider)
    process.start()
