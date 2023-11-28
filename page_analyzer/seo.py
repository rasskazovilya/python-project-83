import bs4


def get_seo_data(response):
    bs = bs4.BeautifulSoup(response.text, "html.parser")
    seo_data = {}

    seo_data["h1"] = bs.h1.string if bs.h1 else ""
    seo_data["title"] = bs.title.string if bs.title else ""
    desc_tag = bs.find("meta", attrs={"name": "description"})
    seo_data["desc"] = desc_tag.get("content") if desc_tag else ""

    return seo_data
