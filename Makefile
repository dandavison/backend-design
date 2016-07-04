design.dot: backend_design/design.py
	python backend_design/design.py > design.dot


design.svg: design.dot
	dot -T svg -o design.svg design.dot
