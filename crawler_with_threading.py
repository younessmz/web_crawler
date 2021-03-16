import concurrent.futures
import time
import requests as req
from bs4 import BeautifulSoup


def display_crawl(res):
    for i in res:
        print(f"********** {i['url']} ********** Sub_Domain {i['sub_domain']}")
        children = list(set(i['children']))
        for j in children:
            print(f"    ----{j}")


def remove_link_from_list_of_dicts(pages, link):
    for i in range(len(pages)):
        if pages[i]['url'] == link:
            pages.pop(i)

    return pages


def crawl_page_opt(page):

    url = page['url']  # get the url we want to crawl

    sub_domain = page['sub_domain']  # get which sub_domain we are in

    page_to_crawl = []  # Create the list of links we want to visit on this page

    children = []  # Create the list of links encountered in this page

    visited = page['visited']

    crawl = page['crawl']

    sub_domain_max = page['sub_domain_max']

    if sub_domain > sub_domain_max:
        return 1

    tags = ('a', 'area', 'base', 'link')  # All the tags that might contain a link in the html file

    soup = BeautifulSoup(req.get(url).text, features="html.parser")  # parsing the html

    for tag in tags:  # Parsing all tags
        for tag_content in soup.findAll(tag):  # Parsing the content of all tags found

            link = tag_content.get('href')  # Getting the actual link

            if link is not None:
                # if the link starts with http or https tha means it is not on the same domain than the start url
                # it is an external link
                if "http" in link or link in visited or link == '#' or link == '/':  # not the same domain
                    if link == '#' or link == '/':
                        link = url + link

                    children.append(link)  # Adding the link to the list of links in this page
                    visited.append(link)  # Adding the link to the visited list so we do not crawl it after

                else:  # same domain
                    # dict creation containing the url and the sub_domain number
                    new_link = {
                        'url': url + link,
                        'sub_domain': sub_domain + 1,
                        'sub_domain_max': sub_domain_max,
                        'visited': visited,
                        'crawl': crawl
                    }
                    page_to_crawl.append(new_link)  # Adding this page to the list of pages to crawl
                    children.append(url + link)  # Adding the link to the list of links in this page
                    visited.append(url)  # Adding this page to the list of pages we visited

    # Dict containing the url, the sub_domain number and the list of links on this page
    obj = {
        'url': url,
        'sub_domain': sub_domain,
        'children': children
    }

    crawl.append(obj)  # Adding this dict to the list of all pages crawled

    # If the list is empty we stop
    if not page_to_crawl:
        return 1

    # Recursively calling the function on the list of links found on this page with multi Threading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(crawl_page_opt, page_to_crawl)

    visited = list(set(visited))

    crawl_result = {
        'pure_crawl_result': crawl,  # list of dict containing visited website along with all the links they contain
                                     # for display purpose
        'visited_websites': sorted(visited)  # list of all the visited website during the crawling
    }

    return crawl_result


def web_crawler_opt(test=False, url=None):

    if test is False:
        url = input("Enter the url of the website you want to crawl : ")

    url = url

    start_time = time.time()

    page = {
        'url': url,
        'sub_domain': 0,
        'sub_domain_max': 1,
        'visited': [],
        'crawl': []
    }

    crawl_result = crawl_page_opt(page)

    res = sorted(crawl_result['pure_crawl_result'], key=lambda k: k['sub_domain'])

    if not test:
        display_crawl(res)

    print("--- %s seconds ---" % (time.time() - start_time))

    return crawl_result['visited_websites']


if __name__ == "__main__":
    web_crawler_opt()
