ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build/V503.pdf

build/V503.pdf: Praeambel_prak.tex Theorie.tex  V503.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V503.tex

full: Praeambel_prak.tex Theorie.tex V503.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V503.tex
		biber build/V503.bcf
		lualatex --output-directory=build V503.tex


build:
		mkdir -p build

clean:
		rm -rf build
.PHONY: clean all
