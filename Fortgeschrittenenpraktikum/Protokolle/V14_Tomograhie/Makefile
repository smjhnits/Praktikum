ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build/V14_main.pdf

build/V14_main.pdf: Praeambel_prak.tex Theorie.tex  V14_main.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V14_main.tex

full: Praeambel_prak.tex Theorie.tex V14_main.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V14_main.tex
		biber build/V14_main.bcf
		lualatex --output-directory=build V14_main.tex


build:
		mkdir -p build

clean:
		rm -rf build
.PHONY: clean all
