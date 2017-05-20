ifeq (,$(shell sh -c 'cygpath --version 2> /dev/null'))
  # Unix
  pwd := $$(pwd)
  translate = $1
else
  # Windows mit MSys2/Cygwin
  pwd := $$(cygpath -m "$$(pwd)")
  translate = $(shell echo '$1' | sed 's/:/;/g')
endif

all: build

build:
		#mkdir -p V503_Der_Milikan_Versuch/{Tabellen,Pics,Python}
		#touch V503_Der_Milikan_Versuch/{Auswertung.tex,V503.tex,Theorie.tex,lit.bib,Makefile}
		#cp -r Praeambel_prak.tex V503_Der_Milikan_Versuch/

clean:
		#rm -rf V503_Der_Milikan_Versuch
.PHONY: clean all
