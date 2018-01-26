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
		#mkdir -p V61_HeNe_Laser/Tabellen
		#mkdir -p V61_HeNe_Laser/Pics
		#mkdir -p V61_HeNe_Laser/Python
		#touch V61_HeNe_Laser/Auswertung.tex
		#touch V61_HeNe_Laser/V61_main.tex
		#touch V61_HeNe_Laser/Theorie.tex
		#touch V61_HeNe_Laser/lit.bib
		#touch V61_HeNe_Laser/Makefile
		#touch V61_HeNe_Laser/Pics/savedatei.txt
		#touch V61_HeNe_Laser/Python/savedatei.txt
	  #touch V61_HeNe_Laser/Tabellen/savedatei.txt
		#cp -r Praeambel_prak.tex V61_HeNe_Laser/

clean:
		#rm -rf V61_HeNe_Laser
.PHONY: clean all
