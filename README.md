# jupyter-powershell

## Install kernel 

```powershell
./install-kernel.ps1
```

## Run

Run from this folder to allow python load all the modules

```
PS C:\dev\> jupyter notebook --kernel=powershell
```

## Aknowledgement

This is an early prototype, but I tried to avoid unnessesary dependencies.

This kernel is heavily based on https://github.com/takluyver/bash_kernel (as jupyter kernel example) and 
https://github.com/wuub/SublimeREPL for calling PowerShell repl from python.

The former has complicated license, so here is a careful explanation of the used parts.

From https://github.com/wuub/SublimeREPL/blob/94e859eae3b9a665a818ff7e13e45edf303ef87b/LICENSE-LIB.txt

```
This means that, although the parts of SublimeREPL that I (wuub) wrote are published under BSD license and you're free to reuse them as you wish, the whole SublimeREPL package is as of now licensed under GPLv2.
```

I'd like to avoid GPLv2 dependencies (and I don't need any of that code), so I want to list all used code (BSD/MIT):

* killable process version is borrowed from SublimeRepl. It's originally licensed under MIT by Peter Astrand, I'm using wuub's version.
* `repl.py`, `subprocess_repl.py`, `powershell_repl.py` wrote by wuub, licensed under BSD/MIT.


### LICENSE

All code that I (vors) wrote is licensed under MIT v3 license.
