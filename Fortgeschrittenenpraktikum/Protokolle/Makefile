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
		#mkdir -p V01_kosmische_Myonen/{Tabellen,Pics,Python}
		#touch V01_kosmische_Myonen/{Auswertung.tex,V01_main.tex,Theorie.tex,lit.bib,Makefile}
		#touch V01_kosmische_Myonen/Pics/savedatei.txt
		#touch V01_kosmische_Myonen/Python/savedatei.txt
	  #touch V01_kosmische_Myonen/Tabellen/savedatei.txt
		#cp -r Praeambel_prak.tex V01_kosmische_Myonen/

clean:
		#rm -rf V01_kosmische_Myonendqfw
.PHONY: clean all
