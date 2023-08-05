all: a.py n.py p.py r.py s.py v.py

a.py n.py r.py s.py v.py: wn.py
	python $< $(basename $@) > $@

p.py: wp.py
	python $< $(basename $@) > $@

.PHONY: clean
clean:
	rm -f {a,n,p,r,s,v}.py
