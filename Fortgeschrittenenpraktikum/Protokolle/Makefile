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
		#mkdir -p V14_Tomograhie/Tabellen
		#mkdir -p V14_Tomograhie/Pics
		#mkdir -p V14_Tomograhie/Python
		#touch V14_Tomograhie/Auswertung.tex
		#touch V14_Tomograhie/V14_main.tex
		#touch V14_Tomograhie/Theorie.tex
		#touch V14_Tomograhie/lit.bib
		#touch V14_Tomograhie/Makefile
		#touch V14_Tomograhie/Pics/savedatei.txt
		#touch V14_Tomograhie/Python/savedatei.txt
	  #touch V14_Tomograhie/Tabellen/savedatei.txt
		#cp -r Praeambel_prak.tex V14_Tomograhie/

clean:
		#rm -rf V14_Tomograhie
.PHONY: clean all
