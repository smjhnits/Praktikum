ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build/US1.pdf

build/US1.pdf: Praeambel_prak.tex Theorie.tex  US1.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build US1.tex

full: Praeambel_prak.tex Theorie.tex US1.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build US1.tex
		biber build/US1.bcf
		lualatex --output-directory=build US1.tex


build:
		mkdir -p build

clean:
		rm -rf build
.PHONY: clean all
