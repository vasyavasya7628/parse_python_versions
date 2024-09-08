from playwright.sync_api import sync_playwright, Playwright

from utils import write_to_exel_output


def run(pw: Playwright):
    browser = pw.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.python.org/downloads/")

    table_titles = page.locator("#content > div > section > div.row.download-list-widget > div")
    table_content = page.locator("#content > div > section > div.row.download-list-widget > ol")
    titles_data = parse_table_to_list(table_titles.all(), "span")
    content_data = parse_table_to_list(table_content.all(), "li > span")
    titles_data.extend(content_data)
    # превращаем список в список кортежей [(),() ...], чтобы exel съел
    it = iter(titles_data)
    a = list(zip(it, it, it, it))

    write_to_exel_output(a, "out")
    context.close()
    browser.close()


def parse_table_to_list(html_block, locator="span"):
    t_data = []
    for table_item in html_block:
        html_block = table_item.locator(f"{locator}")
        for span_element in html_block.all():
            a_element = span_element.locator("a")
            if a_element.is_visible() and a_element.inner_text().find("Python") == -1:
                if a_element.get_attribute("href").find("downloads") != -1:
                    t_data.append(f"https://www.python.org{a_element.get_attribute("href")}")
                else:
                    t_data.append(a_element.get_attribute("href"))
            else:
                t_data.append(span_element.inner_text())
    return t_data


with sync_playwright() as playwright:
    run(playwright)
