# tenhou_mjlog

## 使用方法

- 将库clone到本地
- 从天凤官网上下载`scraw[year].zip`并放入`scraw/`目录下
- 运行`python get_mjlog.py`

## 注意事项

1. 如果已经解压zip文件及gz文件中的`html`文件进`html/`目录, 请注释掉`main`函数中的`unzip()`.
2. 如果已经从html文件中解析牌谱链接至`html/raw_urls.txt`, 请注释掉`main`函数中的`parse()`.
