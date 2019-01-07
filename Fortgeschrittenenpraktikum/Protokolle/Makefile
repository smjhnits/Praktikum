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
		# mkdir -p V60_Diodenlaser/Tabellen
		# mkdir -p V60_Diodenlaser/Pics
		# mkdir -p V60_Diodenlaser/Python
		# touch V60_Diodenlaser/Auswertung.tex
		# touch V60_Diodenlaser/V60_main.tex
		# touch V60_Diodenlaser/Theorie.tex
		# touch V60_Diodenlaser/lit.bib
		# touch V60_Diodenlaser/Makefile
		# touch V60_Diodenlaser/Pics/savedatei.txt
		# touch V60_Diodenlaser/Python/savedatei.txt
	  # touch V60_Diodenlaser/Tabellen/savedatei.txt
		# cp -r Praeambel_prak.tex V60_Diodenlaser/

clean:
		# rm -rf V60_Diodenlaser
.PHONY: clean all
