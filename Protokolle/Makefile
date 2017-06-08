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
		#mkdir -p V602_Roentgenemission/{Tabellen,Pics,Python}
		#touch V602_Roentgenemission/{Auswertung.tex,V602_Roentgenemission.tex,Theorie.tex,lit.bib,Makefile}
		#touch V602_Roentgenemission/Pics/savedatei.txt
		#touch V602_Roentgenemission/Python/savedatei.txt
		#touch V602_Roentgenemission/Tabellen/savedatei.txt
		#cp -r Praeambel_prak.tex V602_Roentgenemission/

clean:
		#rm -rf V602_Roentgenemission
.PHONY: clean all
