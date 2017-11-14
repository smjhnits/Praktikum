ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build6/TheoBlatt6.pdf

build6/TheoBlatt6.pdf: Praeambel_Theo.tex Theo_Header.tex  Aufgaben3.tex  Blatt06.tex TheoBlatt6.tex| build6
		lualatex --output-directory=build6 TheoBlatt6.tex
		lualatex --output-directory=build6 TheoBlatt6.tex

build6:
		mkdir -p build6

clean:
		rm -rf build6
.PHONY: clean all
