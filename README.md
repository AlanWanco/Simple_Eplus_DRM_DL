# Simple_Eplus_DRM_DL
一个配合N_m3u8DL-RE简单下载eplusDRM视频的工具
## 快速开始
```
eplus_drm_archive_download.exe --url-mpd <mpd_url> --cookie-mpd <Cookie> --auth <auth_token>
```
## Release内bat脚本用法：
打开`运行我.bat`依次输入`mpd地址`、`mpd对应的cookie`和`auth验证的url`
## 注意！！：
* 需要提前安装好微软的vc库才能正常使用mp4decrypt，N_m3u8DL-RE也有一些环境要求
* 解压路径里不能有非英文字符否则解码mp4decrypt可能会报错

## `mpd地址`、`mpd对应的cookie`和`auth验证token`的获取方法：
1. 用记事本打开`find_mpd.js`，全部复制内容
2. 用edge打开武士道系live的eplus网页，按F12进入开发者工具，在上面一行菜单栏里寻找`控制台`栏，点进去
3. 随便找个地方右键`清除控制台`，然后输入脚本内容的时候可能会要你输入一行文字才能让你粘贴脚本内容，输入就行
4. 粘贴find_mpd.js的内容后回车，会出现一行`https://vod.live.eplus.jp/out/v1/`开头的链接，右键复制，这就是`mpd地址`

5. 把开发者工具从`控制台`调到`网络`一栏，在网络一栏下面有一栏，（里面可能有保留日志禁用缓存之类的那一行），找到前面icon里的`启用筛选器`和后面有文字说明的`禁用缓存`，这两个全部点上
6. 在筛选器里输入mpd，然后切换回eplus网页本身，把复制过来的`https://vod.live.eplus.jp/out/v1/`开头的链接粘贴进`eplus网页`的`地址栏`
7. 这时候你的浏览器应该会提示你下载好了mpd文件，不管它，点开`开发者工具`-`网络`这时候下面可能有一个mpd文件的行，名称和`https://vod.live.eplus.jp/out/v1/`开头链接的结尾是一致的，点击那一行，出现资源详情
8. 点击`标头`一栏，找到`响应标头`下的Cookie一行，把Cookie一栏下那么长的内容（
`CloudFront-Key-Pair-Id`开头的那些，不包括"Cookie"）全部复制，这样我们就得到了`mpd对应的cookie`

9、接下来继续在开发者工具这里，把筛选框内的「mpd」删除，换成「drm」，如果这里出不来东西的话，就保持这个筛选框不变，切回网页后点击刷新，同时点击播放网页回放，这时候才会出现几条内容，我们点击「get_auth_token_drm?...」开头的那段，复制这段的url地址，这样我们就有了`auth验证的url`。

10. 回到最开头，打开运行我.bat，分别输入`mpd地址`、`mpd对应的cookie`和`auth验证的url`
# Tips
* cookie和验证token都很长，可以找个记事本记一下，复制的时候注意一下前后不要带空格，cookie结尾不要带分号
* Cookie的过期时间是一小时，token的过期时间最短只有几分钟，尽量快速下载
* eplus不用挂代理，有可能出问题的地方大概也就auth验证那里，出问题的话Cookie和Auth多刷新几次试试。
* **以及cookie一小时刷新一次，其他两个字符串都不需要重新获取，记得开个记事本记录一下就行。**
* 程序跑完就下完了，记得文件夹结构最好不要动，eplus_drm_archive_download.exe、N_m3u8DL-RE.exe、mp4decrypt.exe、ffmpeg.exe、google_aosp_on_ia_emulator_14.0.0_9389cec2_4464_l3和运行我.bat这六个一定要在同一个文件夹内。
* 最后合并音视频文件时如果出现大量WARN报错（如下图），检查mp4decrypt.exe的路径是否存在非英文字符或者mp4decrypt.exe的依赖是否正常安装
![f325c1fe9adc267bd18b29490d421680](https://github.com/AlanWanco/Simple_Eplus_DRM_DL/assets/45628961/2d161d6c-d187-41c6-ad7e-606642dfa242)

