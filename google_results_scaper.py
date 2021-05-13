from selenium import webdriver # Requires prior webdriver installation (non-pip)
import re

def get_google_search_results_links(queries, n_pages):
    # initializations
    site_links = []
    for query in queries:
        # driver set up
        driver = webdriver.Chrome()
        driver.get("http://www.google.com")

        # User agreement
        try:
            element = driver.find_element_by_id("L2AGLb")
            element.click()
        except:
            pass
        try:
            element = driver.find_element_by_xpath("//*[@id=\"introAgreeButton\"]/span/span")
            element.click()
        except:
            pass

        # search
        element = driver.find_element_by_xpath("/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
        element.send_keys(query)
        element.submit()

        # grab 1st page
        driver.get(driver.current_url)
        results = driver.find_elements_by_class_name("yuRUbf")
        for result in results:
            link = result.find_element_by_xpath("a[@href]").get_attribute("href")
            site_links.append(link)

        # Grab page pattern
        table = driver.find_elements_by_xpath("//*[@id=\"xjs\"]/table")[0]
        pages = table.find_elements_by_class_name("fl")
        base_pattern = pages[0].get_attribute("href")

        # generate other pages
        for i in range(10, n_pages*10, 10):
            link = re.sub("start=\d+&", "start={}&".format(str(i)), base_pattern)
            driver.get(link)
            results = driver.find_elements_by_class_name("yuRUbf")
            if len(results) > 0:
                for result in results:
                    link = result.find_element_by_xpath("a[@href]").get_attribute("href")
                    site_links.append(link)
            else:
                break
        driver.close()
    site_links = list(set(site_links))
    print("Found {} unique links.".format(len(site_links)))
    return site_links
def make_screenshots_of_webpage(links):
    n = 0
    for URL in links:
        file_name = str(n) + ".png"
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(URL)

        # Closes consent box
        try:
            driver.find_element_by_xpath("//*[@id=\"qc-cmp2-ui\"]/div[2]/div/button[2]").click()
        except:
            pass

        # Credit for this goes to Klaidonis from https://stackoverflow.com/a/57338909/15523956
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
        driver.find_element_by_tag_name('body').screenshot(file_name)
        driver.quit()
        n += 1





