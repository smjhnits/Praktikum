ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build/V27_Zeeman-Effekt.pdf

build/V27_Zeeman-Effekt.pdf: Praeambel_prak.tex Theorie.tex  V27_Zeeman-Effekt.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V27_Zeeman-Effekt.tex

full: Praeambel_prak.tex Theorie.tex V27_Zeeman-Effekt.tex Auswertung.tex lit.bib | build
		lualatex --output-directory=build V27_Zeeman-Effekt.tex
		biber build/V27_Zeeman-Effekt.bcf
		lualatex --output-directory=build V27_Zeeman-Effekt.tex


build:
		mkdir -p build

clean:
		rm -rf build
.PHONY: clean all
