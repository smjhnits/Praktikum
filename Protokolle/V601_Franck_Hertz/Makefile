iifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build/V601.pdf

build/V601.pdf: Praeambel_prak.tex Theorie.tex  V601.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V601.tex

full: Praeambel_prak.tex Theorie.tex V601.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V601.tex
		biber build/V601.bcf
		lualatex --output-directory=build V601.tex


build:
		mkdir -p build

clean:
		rm -rf build
.PHONY: clean all
