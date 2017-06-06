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
		mkdir -p US1/{Tabellen,Pics,Python}
		touch US1/{Auswertung.tex,US1.tex,Theorie.tex,lit.bib,Makefile}
		touch US1/Pics/savedatei.txt
		touch US1/Python/savedatei.txt
		touch US1/Tabellen/savedatei.txt
		cp -r Praeambel_prak.tex US1/

clean:
		rm -rf US1
.PHONY: clean all
