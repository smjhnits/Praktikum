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
		# mkdir -p V49_gepulste_NMR/Tabellen
		# mkdir -p V49_gepulste_NMR/Pics
		# mkdir -p V49_gepulste_NMR/Python
		# touch V49_gepulste_NMR/Auswertung.tex
		# touch V49_gepulste_NMR/V61_main.tex
		# touch V49_gepulste_NMR/Theorie.tex
		# touch V49_gepulste_NMR/lit.bib
		# touch V49_gepulste_NMR/Makefile
		# touch V49_gepulste_NMR/Pics/savedatei.txt
		# touch V49_gepulste_NMR/Python/savedatei.txt
	  # touch V49_gepulste_NMR/Tabellen/savedatei.txt
		# cp -r Praeambel_prak.tex V49_gepulste_NMR/

clean:
		#rm -rf V49_gepulste_NMR
.PHONY: clean all
