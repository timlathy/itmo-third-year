# Computer Systems Engineering, ITMO University, Third Year

## Rendering `.tex` Reports

```sh
mkdir -p ~/texmf/tex/latex/labreport && \
  curl -s http://www.ifmo.ru/file/news/4246/itmo_logo_rus_vert_bw.eps | epstopdf -f -o=$HOME/texmf/tex/latex/labreport/itmo-ru.pdf && \
  curl -s http://www.ifmo.ru/file/news/4246/itmo_logo_en_vert_bw.eps | epstopdf -f -o=$HOME/texmf/tex/latex/labreport/itmo-en.pdf && \
  curl https://raw.githubusercontent.com/timlathy/itmo-third-year/master/labreport.cls -o ~/texmf/tex/latex/labreport/labreport.cls
```

(Note that you need to have `epstopdf` installed on your machine. It is available
in the `texlive-epstopdf` package in Fedora and as a part of `texlive-font-utils` in Ubuntu and Debian.)

## Group Assignments

* [Distributed Computing, 6th term](https://github.com/quest-prophets/distra-timdali)

## See Also

* [Second year, 2018-2019](https://github.com/timlathy/itmo-second-year)
* [First year, 2017-2018](https://github.com/timlathy/itmo-first-year)
