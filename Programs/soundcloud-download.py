import requests as rq
from bs4 import BeautifulSoup as bs
import re, sys, json, argparse

if "idlelib" in sys.modules: #If using IDLE:
    class args:
        url = None
        output = None
    args.url = input("SoundCloud URL? ")
    args.output = input("Destination (default: title of track)? ")
    if args.output == "":
        args.output = None
else:
    parser = argparse.ArgumentParser(description="Download a SoundCloud track as a .mp3 file.")
    parser.add_argument("url", help="The URL for the SoundCloud music, like \"https://soundcloud.com/author/song\"")
    parser.add_argument("-O", "--output", help="Specify output file")
    args = parser.parse_args()

def get(url):
    print("Fetching '%s'..." % url, file=sys.stderr)
    return rq.get(url).text

def get_soundcloud_data(url):
    page = get(url)
    soup = bs(page, "html.parser")
    hls = None
    client_id = None
    # Find MP3 HLS URL
    for i in soup.find_all("script", {"src": False}):
        search = re.search(
            '{"url":"(https://api-v2.soundcloud.com/media/soundcloud:tracks:.*?/stream/hls)","preset":"mp3_0_0"',
            i.text
        )
        if search:
            hls = search.group(1)
            break
    
    for i in sorted(#For each <script crossorigin> tag (Sorted backwards, prioritizing anything with 48 in it)
            soup.find_all("script", {"crossorigin": True}),
            key=(lambda x: ("\x7F"*100 if "48" in x["src"] else x["src"])), 
            reverse=True):
        if re.match("https://a-v2\.sndcdn\.com/assets/.*\.js", i["src"]):
            js = get(i["src"])
            match = re.search(r'client_id:"([A-Za-z0-9]*?)"', js)
            if match:
                client_id = match.group(1)
                break
    
    return {"hls": hls, "client_id": client_id, "_soup": soup}
    

def main(url):
    global m3u8
    data = get_soundcloud_data(url)
    url = data["hls"] + "?client_id=" + data["client_id"]
    print("Found refrence URL:", url, file=sys.stderr)
    m3u8 = get(json.loads(get(url))["url"])
    last_index = re.search("^(.*?)\n#EXT-X-ENDLIST$", m3u8, re.MULTILINE).group(1)
    mp3_download = re.sub("/media/[0-9]*?/", "/media/0/", last_index)
    if args.output:
        title = args.output
    else:
        title = data["_soup"].find("meta", {"property": "og:title"})["content"]
        alphabet = "".join([chr(i) for i in range(65, 91)])
        title = "".join([i for i in title if i in alphabet + alphabet.lower()]) + ".mp3"
    print("Saving as", title, end="")
    with open(title, "wb") as f:
        f.write(rq.get(mp3_download).content)

if __name__ == "__main__":
    main(args.url)
