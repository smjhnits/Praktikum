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
		#mkdir -p V41_Molwärme/Tabellen
		#mkdir -p V41_Molwärme/Pics
		#mkdir -p V41_Molwärme/Python
		#touch V41_Molwärme/Auswertung.tex
		#touch V41_Molwärme/V61_main.tex
		#touch V41_Molwärme/Theorie.tex
		#touch V41_Molwärme/lit.bib
		#touch V41_Molwärme/Makefile
		#touch V41_Molwärme/Pics/savedatei.txt
		#touch V41_Molwärme/Python/savedatei.txt
	  #touch V41_Molwärme/Tabellen/savedatei.txt
		#cp -r Praeambel_prak.tex V41_Molwärme/

clean:
		#rm -rf V41_Molwärme
.PHONY: clean all
