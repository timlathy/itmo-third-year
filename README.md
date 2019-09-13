## Rendering `.tex` reports

```sh
mkdir -p ~/texmf/tex/latex/labreport && \
  curl -s http://www.ifmo.ru/file/news/4246/itmo_logo_rus_vert_bw.eps | epstopdf -f -o=$HOME/texmf/tex/latex/labreport/itmo-ru.pdf && \
  curl -s http://www.ifmo.ru/file/news/4246/itmo_logo_en_vert_bw.eps | epstopdf -f -o=$HOME/texmf/tex/latex/labreport/itmo-en.pdf && \
  curl https://raw.githubusercontent.com/timlathy/itmo-third-year/master/labreport.cls -o ~/texmf/tex/latex/labreport/labreport.cls
```

(Note that you need to have `epstopdf` installed on your machine. It is available
in the `texlive-epstopdf` package in Fedora and as a part of `texlive-font-utils` in Ubuntu and Debian.)
