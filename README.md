# Mangaplus Downloader

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![License](https://img.shields.io/badge/license-GPLv3-blue.svg)

## **mloader** - download manga from mangaplus.shueisha.co.jp

A fork of [hurlenko/mloader](https://github.com/hurlenko/mloader) that keeps it working, along with improved speed and reliability. See [what's different](#-whats-new).

## 🚩 Table of Contents

- [Installation](#-installation)
- [Usage](#-usage)
- [Command line interface](#%EF%B8%8F-command-line-interface)
- [What's new?](#-whats-new)

## 💾 Installation

The recommended installation method is using `uv`:

```bash
uv tool install git+https://github.com/infernalsaber/mloader.git
```


If you prefer `pip`, you can still install it directly:

```bash
pip install git+https://github.com/infernalsaber/mloader.git
```

After installation, the `mloader` command will be available. Check the [command line](#%EF%B8%8F-command-line-interface) section for supported commands.

## 📙 Usage

Copy the url of the chapter or title you want to download and pass it to `mloader`.

You can use `--title` and `--chapter` command line argument to download by title and chapter id.

You can download individual chapters or full title (but only available chapters).

Chapters can be saved as `CBZ` archives (default) or separate images by passing the `--raw` parameter.

## 🖥️ Command line interface

Currently `mloader` supports these commands

```
Usage: mloader [OPTIONS] [URLS]...

  Command-line tool to download manga from mangaplus

Options:
  --version                       Show the version and exit.
  -o, --out <directory>           Save directory (not a file)  [default:
                                  mloader_downloads]
  -r, --raw                       Save raw images  [default: False]
  -q, --quality [super_high|high|low]
                                  Image quality  [default: super_high]
  -s, --split                     Split combined images  [default: False]
  -c, --chapter INTEGER           Chapter id
  -t, --title INTEGER             Title id
  -b, --begin INTEGER RANGE       Minimal chapter to try to download
                                  [default: 0;x>=0]
  -e, --end INTEGER RANGE         Maximal chapter to try to download  [x>=1]
  -l, --last                      Download only the last chapter for title
                                  [default: False]
  --chapter-title                 Include chapter titles in filenames
                                  [default: False]
  --chapter-subdir                Save raw images in sub directory by chapter
                                  [default: False]
  --help                          Show this message and exit.
```

## ✨ What's new

- **It works** : Compatible with updated platform APIs
- **Speed**: With multiple workers and rotating ua, faster downloads
- **Resilience**: More resistant to site hiccups, [configurable](#-optional-settings)

### 🔧 Optional settings

Both are environment variables, for example `MAX_WORKERS=4 mloader <url>`.

| Setting         | What it does                                  | Default        |
| --------------- | --------------------------------------------- | -------------- |
| `MAX_WORKERS`   | How many pages to download at once (1 to 8)   | `8`            |
| `MANGAPLUS_URL` | Server address to use if MANGA Plus moves it  | current server |

