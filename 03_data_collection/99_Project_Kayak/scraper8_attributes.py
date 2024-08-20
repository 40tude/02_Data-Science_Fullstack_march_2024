# lit la liste des hotels dans hotels_list.json
# genère un fichier hotels_attributes avec une ligne d'attirbuts par hotel

import json
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
    # however we loose the // ant it is sloooow
    # 1 min to get the attributs for 25 hotels
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
        # TODO At least they work fine 07/04/2024
        # kScoreSelector = ".a3b8729ab1.d86cee9b25::text"
        # kDescription2Selector = (
        #     ".a53cbfa6de.b3efd73f69::text"  # <p data-testid="property-description" class="a53cbfa6de b3efd73f69">....
        # )
        # klatlng = "div.hotel-sidebar-map hotel-sidebar-map-a11y a::attr(href)"  # <div class="hotel-sidebar-map hotel-sidebar-map-a11y">....

        kScoreSelector = ".d0522b0cca.fd44f541d8::text"
        kDescription2Selector = ".e2585683de.c8d1788c8c::text"
        # klatlng = "div.hotel-sidebar-map hotel-sidebar-map-a11y a::attr(href)"  # <div class="hotel-sidebar-map hotel-sidebar-map-a11y">....

        score = response.css(kScoreSelector).get().replace(",", ".")
        description = response.css(kDescription2Selector).get()

        # url = response.css("div.hotel-sidebar-map a::attr(data-atlas-latlng)").extract()
        # <div class="b95907b7ce" style="background-image: url(&quot;https://maps.googleapis.com/maps/api/staticmap?key=AIzaSyBsCRN3eiZNxm0nbI9snuHn3_shiZ3I6zQ&amp;channel=hotel&amp;center=48.8551725227304%2C2.36022859811783&amp;size=261x182&amp;zoom=13&amp;signature=Xxfoh14CsX8ZR2ZatU_vjGJ_ZH4=&quot;);"><div class="f96723525b"><div class="d3f3aeebf0" data-testid="map-entry-point-marker"><span class="d3a235084b" data-testid="map-entry-pin-icon"><span class="b2142222c3"><span class="b235b4f8e2"></span><svg viewBox="-1 -1 26 32" class="af04624a2c"><path d="M24 12.4286C24 19.2927 12 29 12 29C12 29 0 19.2927 0 12.4286C0 5.56446 5.37258 0 12 0C18.6274 0 24 5.56446 24 12.4286Z"></path></svg></span><svg class="cd891e017f" viewBox="0 0 12 4"><ellipse cx="6" cy="2" rx="6" ry="2"></ellipse></svg></span></div><button data-map-trigger-button="1" type="button" class="dba1b3bddf e99c25fd33 f8a5a77b19 a86bcdb87f bec09c39da bbe6fc3743"><span class="eed450ee2f">Voir sur la carte</span></button></div></div>
        url = response.css(".b95907b7ce").get()
        # hotel_sidebar_static_map_capla > div > div
        latitude = url[0].split(",")[0]
        longitude = url[0].split(",")[1]
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
