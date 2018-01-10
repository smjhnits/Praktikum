ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build11/TheoBlatt11.pdf

build11/TheoBlatt11.pdf: Praeambel_Theo.tex Theo_Header.tex Aufgaben_Jonah.tex Navier_Stokes.tex TheoBlatt11.tex| build11
		lualatex --output-directory=build11 TheoBlatt11.tex
		lualatex --output-directory=build11 TheoBlatt11.tex

build11:
		mkdir -p build11

clean:
		rm -rf build11
.PHONY: clean all
