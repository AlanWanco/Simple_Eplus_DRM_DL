import base64, re, requests, os, argparse, subprocess
from datetime import datetime

parser = argparse.ArgumentParser(description='eplusDRM下载')
parser.add_argument('--url-mpd', help='推流的mpd地址', required=True, type=str)# args.url_mpd
parser.add_argument('--cookie-mpd', help='输入推流MPD的cookie', required=True, type=str)# args.cookie_mpd
parser.add_argument('--auth', '-a', help='输入推流开始后可以获取的token', required=True, type=str)
args = parser.parse_args()

url_mpd = args.url_mpd
cookies_mpd = args.cookie_mpd
auth_token = args.auth

cookies_dict_mpd = {key: value for key, value in (pair.split('=') for pair in cookies_mpd.split(';'))}

api_url = "https://cdrm-project.com/api"
license_url = "https://lic.drmtoday.com/license-proxy-widevine/cenc/?specConform=true"
headers = {'accept': '"*/*"','content-length': '"316"','Connection': 'keep-alive','X-Dt-Auth-Token': auth_token}

MATCH_IV = (r'IV=(?P<m3u8_iv>.*?)(?=\n|$)')
MATCH_STREAM = 'https://vod.live.eplus.jp/out/v1/(?P<base>.*?)/'
MATCH_UUID = r"""cenc:default_KID=\"(?P<mpd_url>.*?)\""""

formatted_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
path = os.getcwd()
file = f'eplus_drm_{formatted_datetime}'

def get_key():
    r = requests.post(api_url, headers=headers,json={"license":license_url,"pssh":pssh}).json()
    # print(r)
    key = r['keys'][0]['key'].split(':')[1]
    mpd_key = r['keys'][0]['key']
    print("获得key：", key, "获得KID:KEY：", mpd_key)
    return mpd_key

def get_pssh(keyId):
	array_of_bytes = bytearray(b'\x00\x00\x008pssh\x00\x00\x00\x00')
	array_of_bytes.extend(bytes.fromhex('edef8ba979d64acea3c827dcd51d21ed'))    #是谷歌drm的 system id，不用改
	array_of_bytes.extend(b'\x00\x00\x00\x18\x12\x10')
	array_of_bytes.extend(bytes.fromhex(keyId.replace('-', '')))
	array_of_bytes.extend(b'H\xe3\xdc\x95\x9b\x06')
	return base64.b64encode(bytes.fromhex(array_of_bytes.hex()))

def createpsshfromkid(kid):
	kid = kid.replace('-', '')
	if len(kid) == 32 and isinstance(kid, bytes):
		raise AssertionError('Wrong KID length')
	return get_pssh(kid).decode('utf-8')

def find_base(match, text):
    result = re.search(match, text)
    print('获得base值：', result.group("base"))
    return result.group("base")

def mpd_download(file, path, cookies_mpd, url_mpd):
    print('=======调用N_m3u8DL-RE下载回放=======')
    command = fr'.\N_m3u8DL-RE --save-name "{file}" --save-dir "{path}" --download-retry-count 5 --auto-select --thread-count 16 --mux-after-done format=mp4 --check-segments-count --ffmpeg-binary-path .\ffmpeg.exe -H "Cookie: {cookies_mpd}" --del-after-done --key "{mpd_key}" --decryption-binary-path .\mp4decrypt.exe {url_mpd}'
    # print(command)
    subprocess.call(command)

if __name__ == "__main__":
    try:
        res = requests.get(url_mpd, cookies=cookies_dict_mpd)
        if res.status_code==200:
            mpd_base = find_base(MATCH_STREAM, url_mpd)
            m = re.search(MATCH_UUID, res.text)
            if m:
                uuid = m.group("mpd_url")
                print("获得UUID", uuid)
                pssh = createpsshfromkid(uuid)
                print('获得PSSH值', pssh)
                mpd_key = get_key()
        else:
            print('未能访问MPD地址')

        if mpd_key:
            mpd_download(file, path, cookies_mpd, url_mpd)
        else:
            print('没有返回正确的key！检查auth token是否有问题')

    except Exception as e:
        print(e)
