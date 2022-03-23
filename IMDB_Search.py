import eg,re
from urllib import quote
from urllib2 import urlopen

#config
max_titles = 4
display_time = 10

b_url = "https://www.imdb.com"
s_url = "/find?q="
dv = eg.plugins.DVBViewer

result = dv.GetCurrentShowDetails()
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

search_page = urlopen(b_url + s_url + title).read()
m = re.findall('class="result_text".*?<a href="(/title/tt[0-9]{4,12}/).*?>(.*?)</a>(.*?)<', search_page)

length = len(m)
if length > max_titles:
    length = max_titles

out_str = ""
if length > 0:
    for i in range(length):
        print m[i][0]
        genres_str = ""
        title_page = urlopen(b_url + m[i][0]).read()
        genres_html = re.findall('<div class="ipc-chip-list.*?data-testid="genres">(.*?)</div>', title_page)
        if genres_html:
            genres = re.findall('"ipc-chip.*?presentation">(.*?)<', genres_html[0])
            for gn in genres:
                genres_str += gn + " "
        print genres_str
        rating = re.findall('itemprop="ratingValue">(.*?)<', title_page)
        if not rating:
            rating = re.findall('class="AggregateRatingButton__RatingScore.*?">(.*?)<', title_page)
            if not rating:
                rating = re.findall('class=".*?aggregate-rating__score.*?">.*?>(.*?)<', title_page)
        if rating:
            out_str += m[i][1] + " " + m[i][2] + " " + rating[0] + " " + genres_str + "\n"
            
if out_str != "":
    dv.ShowInfoinTVPic(out_str.decode('utf8','ignore'), display_time)
else:
    dv.ShowInfoinTVPic("Nothing found", display_time)
