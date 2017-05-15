ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: main.pdf

main.pdf: Praeambel_prak.tex theorie.tex  main.tex auswertung.tex lit.bib | build
		lualatex --output-directory=build main.tex

full: Praeambel_prak.tex theorie.tex main.tex auswertung.tex lit.bib | build
		lualatex --output-directory=build main.tex
		biber build/main.bcf
		lualatex --output-directory=build main.tex


build:
		mkdir -p build

clean:
		rm -rf build
.PHONY: clean all
