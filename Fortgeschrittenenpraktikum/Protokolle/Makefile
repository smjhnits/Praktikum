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
		#mkdir -p V21_Optisches_Pumpen/{Tabellen,Pics,Python}
		#touch V21_Optisches_Pumpen/{Auswertung.tex,V21_main.tex,Theorie.tex,lit.bib,Makefile}
		#touch V21_Optisches_Pumpen/Pics/savedatei.txt
		#touch V21_Optisches_Pumpen/Python/savedatei.txt
	  #touch V21_Optisches_Pumpen/Tabellen/savedatei.txt
		#cp -r Praeambel_prak.tex V21_Optisches_Pumpen/

clean:
		#rm -rf V21_Optisches_Pumpen
.PHONY: clean all
