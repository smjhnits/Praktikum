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
		mkdir -p V27_Zeeman-Effekt/{Tabellen,Pics,Python}
		touch V27_Zeeman-Effekt/{Auswertung.tex,V27_Zeeman-Effekt.tex,Theorie.tex,lit.bib,Makefile}
		touch V27_Zeeman-Effekt/Pics/savedatei.txt
		touch V27_Zeeman-Effekt/Python/savedatei.txt
	  touch V27_Zeeman-Effekt/Tabellen/savedatei.txt
		cp -r Praeambel_prak.tex V27_Zeeman-Effekt/

clean:
		rm -rf V27_Zeeman-Effekt
.PHONY: clean all
