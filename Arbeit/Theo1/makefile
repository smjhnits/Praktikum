ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build/T1_main.pdf

build/T1_main.pdf: Praeambel_Theo.tex Theo_Header.tex  Aufgaben.tex  T1_main.tex| build
		lualatex --output-directory=build T1_main.tex

build:
		mkdir -p build

clean:
		rm -rf build
.PHONY: clean all
