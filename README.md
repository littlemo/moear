# MoEar

用来实现对网络文章的爬取、mobi打包、并投递到Kindle设备上

## Screenshots

<p align="center">
<img alt="" src="https://github.com/littlemo/moear/blob/master/docs/source/intro/images/web/0-index.png" width=280><img alt="" src="https://github.com/littlemo/moear/blob/master/docs/source/intro/images/web/1-subscription.png" width=280><img alt="" src="https://github.com/littlemo/moear/blob/master/docs/source/intro/images/web/2-deliver-log.png" width=280>
<img alt="" src="https://github.com/littlemo/moear/blob/master/docs/source/intro/images/kindle/1-book-toc1.png" width=280><img alt="" src="https://github.com/littlemo/moear/blob/master/docs/source/intro/images/kindle/3-book-toc3.png" width=280><img alt="" src="https://github.com/littlemo/moear/blob/master/docs/source/intro/images/kindle/5-post1.png" width=280>
</p>

## Badge

### GitHub

[![GitHub followers](https://img.shields.io/github/followers/littlemo.svg?label=github%20follow)](https://github.com/littlemo)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/littlemo/moear.svg)](https://github.com/littlemo/moear)
[![GitHub stars](https://img.shields.io/github/stars/littlemo/moear.svg?label=github%20stars)](https://github.com/littlemo/moear)
[![GitHub release](https://img.shields.io/github/release/littlemo/moear.svg)](https://github.com/littlemo/moear/releases)
[![Github commits (since latest release)](https://img.shields.io/github/commits-since/littlemo/moear/latest.svg)](https://github.com/littlemo/moear)

[![Github All Releases](https://img.shields.io/github/downloads/littlemo/moear/total.svg)](https://github.com/littlemo/moear/releases)
[![GitHub Release Date](https://img.shields.io/github/release-date/littlemo/moear.svg)](https://github.com/littlemo/moear/releases)

### 文档

[![Documentation Status](https://readthedocs.org/projects/moear/badge/?version=latest)](http://moear.readthedocs.io/zh_CN/latest/?badge=latest)

### 其他

[![license](https://img.shields.io/github/license/littlemo/moear.svg)](https://github.com/littlemo/moear)
[![](https://img.shields.io/badge/bitcoin-donate-green.svg)](https://keybase.io/littlemo)

## 项目描述

本项目为基于 `Django` 开发的站点服务，提供对已安装文章源的定时抓取、持久化功能，并根据用户需求，
进行 mobi 书籍格式的打包，最终推送到用户设置好的 Kindle 设备上。

其中，文章抓取与 mobi 打包功能均为基于 `stevedore` 包实现的扩展插件，
方便第三方插件实现新的爬虫/打包功能。

了解更多，可查看 [官方文档](http://moear.rtfd.io)

## 版本说明

当前最新版本（ `v1.0.0` ），已完整实现定时异步文章抓取、打包为 mobi 格式、投递到指定 kindle 设备上的核心功能。但仍有很多待完善的地方需要打磨，若您有任何想法，可以给我 Issues 。

## License

本项目采用 [![license](https://img.shields.io/github/license/littlemo/moear.svg)](https://github.com/littlemo/moear) 协议开源发布，请您在修改后维持开源发布，并为原作者额外署名，谢谢您的尊重。

若您需要将本项目应用于商业目的，请单独联系本人( [@littlemo](https://github.com/littlemo) )，获取商业授权。

## 问题

如果您在使用该应用时遇到任何问题，请在 GitHub 上查看本项目 [![moear](https://img.shields.io/badge/Repo-MoEar-brightgreen.svg)](https://github.com/littlemo/moear) ，并在其中提交 [Issues](https://github.com/littlemo/moear/issues) 给我，多谢您的帮助~~
