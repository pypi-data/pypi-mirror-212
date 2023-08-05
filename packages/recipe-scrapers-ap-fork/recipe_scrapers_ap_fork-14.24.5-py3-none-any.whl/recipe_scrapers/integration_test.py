import recipe_scrapers


def scrape_me(url_path, **options):
    host_name = recipe_scrapers._utils.get_host_name(url_path)

    try:
        scraper = recipe_scrapers.SCRAPERS[host_name]
        return scraper(url_path, **options)
    except KeyError:
        pass

    options.pop("wild_mode")
    wild_scraper = recipe_scrapers._factory.SchemaScraperFactory.generate(url_path, **options)
    return wild_scraper


if __name__ == "__main__":
    scraper = scrape_me("https://www.mob.co.uk/life/best-cookbooks-for-christmas-2021", wild_mode=True, allow_redirects=False, timeout=10)


    print(f"host: {scraper.host()}")
    print(f"title: {scraper.title()}")
    print(f"image: {scraper.image()}")
    print(f"ingredients: {scraper.ingredients()}")
    print(f"instructions: {scraper.instructions()}")
    print(f"canonical_url: {scraper.canonical_url()}")
    print(f"language: {scraper.language()}")

