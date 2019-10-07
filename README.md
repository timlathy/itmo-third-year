## Rendering `.tex` reports

```sh
mkdir -p ~/texmf/tex/latex/labreport && \
  curl -s http://www.ifmo.ru/file/news/4246/itmo_logo_rus_vert_bw.eps | epstopdf -f -o=$HOME/texmf/tex/latex/labreport/itmo-ru.pdf && \
  curl -s http://www.ifmo.ru/file/news/4246/itmo_logo_en_vert_bw.eps | epstopdf -f -o=$HOME/texmf/tex/latex/labreport/itmo-en.pdf && \
  curl https://raw.githubusercontent.com/timlathy/itmo-third-year/master/labreport.cls -o ~/texmf/tex/latex/labreport/labreport.cls
```

(Note that you need to have `epstopdf` installed on your machine. It is available
in the `texlive-epstopdf` package in Fedora and as a part of `texlive-font-utils` in Ubuntu and Debian.)

## Tech Showcase

* `Applied-Mathematics-5th-Term/Lab1-Shannon-Entropy`:
creating a native Python extension in Rust to speed up text processing; visualizing results with Jupyter/Pandas
* `Applied-Mathematics-5th-Term/Lab2-Prefix-Codes`:
implementing a recursive prefix code generator in Racket, embedding results in a TeX table (via `csvsimple`)
* `Mathematical-Modeling-5th-Term/Lab1`:
building and solving a system of equations based on a graph definition with SymPy
