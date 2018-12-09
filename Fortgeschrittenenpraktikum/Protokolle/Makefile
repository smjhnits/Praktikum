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
		# mkdir -p V18_Germaniumdetektor/Tabellen
		# mkdir -p V18_Germaniumdetektor/Pics
		# mkdir -p V18_Germaniumdetektor/Python
		# touch V18_Germaniumdetektor/Auswertung.tex
		# touch V18_Germaniumdetektor/V18_main.tex
		# touch V18_Germaniumdetektor/Theorie.tex
		# touch V18_Germaniumdetektor/lit.bib
		# touch V18_Germaniumdetektor/Makefile
		# touch V18_Germaniumdetektor/Pics/savedatei.txt
		# touch V18_Germaniumdetektor/Python/savedatei.txt
	  # touch V18_Germaniumdetektor/Tabellen/savedatei.txt
		# cp -r Praeambel_prak.tex V18_Germaniumdetektor/

clean:
		# rm -rf V18_Germaniumdetektor
.PHONY: clean all
