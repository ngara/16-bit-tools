---
layout: post
title: Starting Out
date: 2020-11-30 07:06:00
permalink: /blog/2020/11/30/
# preview: /blog/images/pngfile.png
# other data
---

Here I am.  This is the first post on my journey to explore and understand the inner workings of the IBM PC.  Along the way, I plan to develop some tools to help deconstruct and understand whatever it is that I run across.

The first challenge I have decided to pursue is to attempt to disassemble the PC game XONIX.  It is a simple game, where you are a square attempting to move around the screen, and there is a bouncing square and a ball or two trying to stop you.  It looks something like this:

![XONIX.EXE](http://quadrax.wz.cz/app/images/xonix_dos.png)

The directory listing for the Xonix game looks something like this:

```
Directory of C:\GAMES\XT\XONIX\.
.              <DIR>            27-11-2020 19:35
..             <DIR>            27-11-2020 19:35
BASRUN   EXE              31744 05-07-1982 12:00
HISCORES XNX                256 02-08-1988 23:07
XONIX    BIN               4104 03-25-1984 14:11
XONIX    EXE               8576 03-25-1984 12:07
XONIX    SE                4096 03-25-1984 12:07
```

The program is run by typing `XONIX` or `XONIX.EXE` but it requires the `BASRUN.EXE` file to be available because it was originally a BASIC program compiled with the Microsoft Basic Compiler.  The original source code is not available on the Internet as far as I can tell.  If someone knows where to find it, please [contact me](mailto:ngara23@gmail.com).

I will start by running XONIX.EXE with a debugger: the recommended debugger is [`DEBUGX`](https://sites.google.com/site/pcdosretro/enhdebug).  I will also be trying to use [`NDISASM`](https://www.nasm.us/) on it, but I need a tool that will decode the MZ executable format in order to understand the executable better.  That's where [16-bit-tools](https://github.com/ngara/16-bit-tools) will come in handy.

More to come.
