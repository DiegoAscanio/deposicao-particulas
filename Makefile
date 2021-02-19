all:
	python setdaup.py build_ext --inplace
	python setdarsup.py build_ext --inplace
	python setdbup.py build_ext --inplace
	mkdir -p simulacoes/{DA,DARS,DB}
