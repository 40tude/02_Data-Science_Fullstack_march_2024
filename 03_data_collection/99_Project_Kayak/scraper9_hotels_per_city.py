# recoit un nom de ville dans la ligne de commande
# tient compte des dates de debut et de fin de séjour
# genère un fichier hotels_list.json pour la ville en question

import sys
import logging
import scrapy

from pathlib import Path
from scrapy.crawler import CrawlerProcess
from datetime import datetime, timedelta

import include_kayak as k

k_CurrentDir = Path(__file__).parent
k_CityName = ""
k_LenStay = 3
k_InHowManyDays = 15


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def build_url(city_str):

    # typiquement
    # checkin  = today + 15 jours
    # checkout = today + 15 jours + 3 jours
    aujourdhui = datetime.today()
    checkin = aujourdhui + timedelta(days=k_InHowManyDays)
    checkin_str = checkin.strftime("%Y-%m-%d")

    checkout = checkin + timedelta(days=k_LenStay)
    checkout_str = checkout.strftime("%Y-%m-%d")

    # https://www.booking.com/searchresults.fr.html?ss=Paris&checkin=2024-09-03&checkout=2024-09-06&group_adults=2&no_rooms=1&group_children=0
    return f"https://www.booking.com/searchresults.fr.html?ss={city_str}&checkin={checkin_str}&checkout={checkout_str}&group_adults=2&no_rooms=1&group_children=0"


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class HotelsListSpider(scrapy.Spider):

    name = "HotelsListSpider"

    def start_requests(self):

        # try:
        #   with open(kCurrentDir/kAssetsDir/kOneCityFile, 'r') as f:
        #     data = json.load(f)
        # except FileNotFoundError:
        #   print(f"Are you sure the file {kOneCityFile} exists ?")

        # # Not yet usefull but we never know...
        # # As today, it creates a list of url with only one url
        # urls = []
        # for entry in data:
        #   cityname = entry['city']
        #   url = build_url(cityname)
        #   urls.append(url)

        urls = []
        url = build_url(k_CityName)
        urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # TODO the constant guys need a review. Indeed, I'm not sure these hard coded selectors will survive a long time
        # TODO At least they work fine 07/04/2024
        # kH3HotelSelector = ".aab71f8e4e"
        # kNameSelector = ".f6431b446c.a15b38c233::text"
        # kUrlSelector = ".a78ca197d0::attr(href)"

        # 19 08 2024
        # Check assets/kH3HotelSelector.png, kNameSelector.png and kUrlSelector.png to see from where the values below come from
        # kH3HotelSelector = ".b9687b0063"

        # bodyconstraint-inner > div:nth-child(8) > div > div.caa83e2398 > div.a84de7f213 > div.b9687b0063 > div.d830fa48ad.db402c28f2 > div.f9958fb57b > div:nth-child(3)                                                                            > div.d8ff70c6e0.bb80b6397f > div.c655c9a144 > div > div.adc8292e09.ea1e323a59.fffdb20d34.fbe4119cc7.fd229921e5 > div.c324bdcee4.ec7ca45eb7 > div > div:nth-child(1) > div            > h3 > a > div.e037993315.f5f8fe25fa
        # bodyconstraint-inner > div:nth-child(8) > div > div.caa83e2398 > div.a84de7f213 > div.b9687b0063 > div.d830fa48ad.db402c28f2 > div.f9958fb57b > div.e01df12ddf.a0914461b0.d46a3604b5.ba1c6fdc7f.f550b7da28.b9a2fd8068.cb4a416743.b0cae6862c > div.d8ff70c6e0.bb80b6397f > div.c655c9a144 > div > div.adc8292e09.ea1e323a59.fffdb20d34.fbe4119cc7.fd229921e5 > div.c324bdcee4.ec7ca45eb7 > div > div:nth-child(1) > div.a8323349e9 > h3 > a > div.e037993315.f5f8fe25fa
        # bodyconstraint-inner > div:nth-child(8) > div > div.caa83e2398 > div.a84de7f213 > div.b9687b0063 > div.d830fa48ad.db402c28f2 > div.f9958fb57b > div:nth-child(9) >                                                                            div.d8ff70c6e0.bb80b6397f > div.c655c9a144 > div > div.adc8292e09.ea1e323a59.fffdb20d34.fbe4119cc7.fd229921e5 > div.c324bdcee4.ec7ca45eb7 > div > div:nth-child(1) > div            > h3 > a > div.e037993315.f5f8fe25fa
        kH3HotelSelector = ".d3e8e3d21a"
        kNameSelector = ".e037993315.f5f8fe25fa::text"
        kUrlSelector = ".f0ebe87f68::attr(href)"

        counter = 0
        for hotel in response.css(kH3HotelSelector):

            counter += 1
            if counter == 21:
                break

            hotel_name = hotel.css(kNameSelector).extract_first()
            url = hotel.css(kUrlSelector).get().split("?")[0]

            processed_data = {
                "hotel": hotel_name,
                "url": url,
            }
            yield processed_data


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv) == 1:
        # for testing/debug purpose
        k_CityName = "Paris"
    else:
        k_CityName = sys.argv[1]

    # if it exists delete previous version of scrapy log file
    log_file_path = k_CurrentDir / k.AssetsDir / k.ScrapyLogFile
    if log_file_path.exists():
        log_file_path.unlink()

    # if it exists delete previous version of hotels_list.json
    hotels_file_path = k_CurrentDir / k.AssetsDir / k.HotelsListFile
    if hotels_file_path.exists():
        hotels_file_path.unlink()

    process = CrawlerProcess(
        settings={
            "USER_AGENT": "Chrome/97.0",
            "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
            "FEEDS": {
                k_CurrentDir / k.AssetsDir / k.HotelsListFile: {"format": "json"},
            },
            "LOG_STDOUT": False,
            "LOG_FILE": k_CurrentDir / k.AssetsDir / k.ScrapyLogFile,
        }
    )

    process.crawl(HotelsListSpider)
    process.start()


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# If files exist, delete them before the CrawlerProcess own it
# if Path.exists(k_CurrentDir / k.AssetsDir / k.ScrapyLogFile):
#     (k_CurrentDir / k.AssetsDir / k.ScrapyLogFile).unlink()

# process = CrawlerProcess(
#     settings={
#         "USER_AGENT": "Chrome/97.0",
#         "LOG_LEVEL": logging.INFO,  # CRITICAL, ERROR, WARNING, INFO, DEBUG...
#         "FEEDS": {
#             k_CurrentDir / k.AssetsDir / k.HotelsListFile: {"format": "json"},
#         },
#         "LOG_STDOUT": False,
#         "LOG_FILE": f"{k_CurrentDir}/{k.AssetsDir}/{k.ScrapyLogFile}",
#     }
# )
