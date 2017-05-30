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
		#mkdir -p V601_Franck_Hertz/{Tabellen,Pics,Python}
		#touch V601_Franck_Hertz/{Auswertung.tex,V601.tex,Theorie.tex,lit.bib,Makefile}
		#touch V601_Franck_Hertz/Pics/savedatei.txt
		#touch V601_Franck_Hertz/Python/savedatei.txt
		#touch V601_Franck_Hertz/Tabellen/savedatei.txt
		#cp -r Praeambel_prak.tex V601_Franck_Hertz/

clean:
		#rm -rf V601_Franck_Hertz
.PHONY: clean all
