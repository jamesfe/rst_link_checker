# docs link checker

I don't like it when the docs have bad links, so I wrote this quick script to search for RST files, then check if the links work.

I didn't put much effort into using auth or interpreting the problems, if it's not 2xx it's treated as bad, which isn't exactly how the Internet works.

You can use it if you want.  There is a 1sec delay between HTTP calls to ensure we are not inadvertently DOS'ing someone.  Be nice!

```
pip install -r requirements.txt
# change some config vars in checker.py (this is a todo)
./src/checker.py
```
