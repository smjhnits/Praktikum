ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build/V61_main.pdf

build/V61_main.pdf: Praeambel_prak.tex Theorie.tex  V61_main.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V61_main.tex

full: Praeambel_prak.tex Theorie.tex V61_main.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V61_main.tex
		biber build/V61_main.bcf
		lualatex --output-directory=build V61_main.tex


build:
		mkdir -p build

clean:
		rm -rf build
.PHONY: clean all
