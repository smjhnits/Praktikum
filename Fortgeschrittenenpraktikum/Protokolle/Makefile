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
		# mkdir -p V46_Faraday/Tabellen
		# mkdir -p V46_Faraday/Pics
		# mkdir -p V46_Faraday/Python
		# touch V46_Faraday/Auswertung.tex
		# touch V46_Faraday/V46_main.tex
		# touch V46_Faraday/Theorie.tex
		# touch V46_Faraday/lit.bib
		# touch V46_Faraday/Makefile
		# touch V46_Faraday/Pics/savedatei.txt
		# touch V46_Faraday/Python/savedatei.txt
	  # touch V46_Faraday/Tabellen/savedatei.txt
		# cp -r Praeambel_prak.tex V46_Faraday/

clean:
		#rm -rf V46_Faraday
.PHONY: clean all
