from crawler_with_threading import *
from crawler_without_threading import *


def check_if_equal(list_1, list_2):
    if len(list_1) != len(list_2):
        return False
    return sorted(list_1) == sorted(list_2)


def test_crawl():

    res_hola_re = ['https://fonts.gstatic.com', 'https://github.com/bkwg', 'https://gmpg.org/xfn/11',
                   'https://hola.re/', 'https://hola.re/#content', 'https://hola.re///s.w.org',
                   'https://hola.re/2021/02/23/ta428-analysis/',
                   'https://hola.re/2021/02/27/dead-simple-dta-tool-using-frida/',
                   'https://hola.re/2021/03/07/cfg-generation/',
                   'https://hola.re/comments/feed/', 'https://hola.re/feed/',
                   'https://hola.re/mailto:bkwg@hola.re',
                   'https://hola.re/wp-content/plugins/enlighter/cache/enlighterjs.min.css?ver=0A0B0C',
                   'https://hola.re/wp-content/themes/wp-indigo/assets/css/style.css?ver=5.7',
                   'https://hola.re/wp-content/uploads/2021/02/cropped-mim-180x180.png',
                   'https://hola.re/wp-content/uploads/2021/02/cropped-mim-192x192.png',
                   'https://hola.re/wp-content/uploads/2021/02/cropped-mim-32x32.png',
                   'https://hola.re/wp-includes/css/dist/block-library/style.min.css?ver=5.7',
                   'https://hola.re/wp-includes/wlwmanifest.xml', 'https://hola.re/wp-json/',
                   'https://hola.re/xmlrpc.php?rsd', 'https://vitathemes.com']

    assert check_if_equal(web_crawler_opt(test=True, url='https://hola.re/'), res_hola_re)
    print('Crawling OK')


def test_threading():

    # test on youtube.com
    youtube_crawl = web_crawler(test=True, url='https://youtube.com/')
    youtube_crawl_threads = web_crawler_opt(test=True, url='https://youtube.com/')
    # assert check_if_equal(google_crawl, google_crawl_threads)
    assert len(youtube_crawl) == len(youtube_crawl_threads)
    print(f'TEST PASSED FOR https://youtube.com/')

    # test on Google.com
    google_crawl = web_crawler(test=True, url='https://google.com/')
    google_crawl_threads = web_crawler_opt(test=True, url='https://google.com/')
    #assert check_if_equal(google_crawl, google_crawl_threads)
    assert len(google_crawl) == len(google_crawl_threads)  # only size : url change because of the dynamic creation of links
                                                           # (maybe due to tokens or cookies)
    print(f'TEST PASSED FOR https://google.com/')

    # test on Monzo.com
    monzo_crawl = web_crawler(test=True, url='https://monzo.com')
    monzo_crawl_threads = web_crawler_opt(test=True, url='https://monzo.com')
    assert check_if_equal(monzo_crawl, monzo_crawl_threads)
    print(f'TEST PASSED FOR https://monzo.com')

    # test on Epita.fr
    epita_crawl = web_crawler(test=True, url='https://epita.fr')
    epita_crawl_threads = web_crawler_opt(test=True, url='https://epita.fr')
    assert check_if_equal(epita_crawl, epita_crawl_threads)
    print(f'TEST PASSED FOR https://epita.fr')

    print("TESTING DONE")


if __name__ == "__main__":

    test_crawl()
    test_threading()

    print("CRAWLING OK")
    print("THREADING OK")

