import eg,re
from urllib import quote
import requests

# settings ------------------------
language     = 'de-CH'
#language     = 'en-US'
headers      = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0','Accept-Language':language}
max_titles   = 3
display_time = 10
b_url        = "https://www.imdb.com"
s_url        = "/find/?q="
# ---------------------------------

dv           = eg.plugins.DVBViewer
result       = dv.GetCurrentShowDetails()
if result['description'] == "":
    dv.ShowInfoinTVPic(result['title'], display_time)
    eg.Exit()

#cut some text
title = re.split('( [(-]{1,2})', result['title'])[0]
print title
dv.ShowInfoinTVPic("IMDB Search: '" + title + "'", display_time)

#prepare for http get request
title = title.encode('utf8', 'ignore')
title = quote(title)

search_page = requests.get(b_url + s_url + title, headers=headers)
m = re.findall('li class=".*?find-title-result.*?href="(/title/tt[0-9]{4,12}/).*?>(.*?)</a.*?([0-9]{4})</label>', search_page.content)

length = len(m)
if length > max_titles:
    length = max_titles

out_str = ""
if length > 0:
    for i in range(length):
        print m[i][1]
        genres_str = ""
        print b_url + m[i][0]
        title_page = requests.get(b_url + m[i][0], headers=headers)
        print "page loaded"
        genres_html = re.findall('<div class="ipc-chip-list.*?data-testid="genres".*?scroller">(.*?)</div>', title_page.content)
        if genres_html:
            genres = re.findall('<span.*?"ipc-chip__text">(.*?)</span>', genres_html[0])
            for gn in genres:
                print "genre found:" + gn
                genres_str += gn + " "
        print genres_str
        rating = re.findall('aggregate-rating__score.*?span.*?>(.*?)<', title_page.content)
        if not rating:
            rating = re.findall('class="AggregateRatingButton__RatingScore.*?">(.*?)<', title_page.content)
            if not rating:
                rating = re.findall('itemprop="ratingValue">(.*?)<', title_page.content)
        if rating:
            out_str += m[i][1] + " " + m[i][2] + " " + rating[0] + " " + genres_str + "\n"
            
if out_str != "":
    dv.ShowInfoinTVPic(out_str.decode('utf8','ignore'), display_time)
else:
    dv.ShowInfoinTVPic("Nothing found", display_time)
