# Scientific computations: which is faster?
## Science vs math package vs numpy package
Ever wondered how efficient the math and numpy packages are?

New scientific formulas are highly efficient in the time complexity (including)
constants, while well-developed packages utilize the fastest possible implementation.

For the comparison, I selected three functions:
 > &pi;	&asymp; 3.14,    e 	&asymp; 2.72, and factorial (!)

## Why these functions? 

Constants are pre-computed in math and
numpy packages.
```angular2html
Precomputed is faster, but may not provide infinite accuracy.
```
Indeed, scientific formulas will compute the constants up to
that many digits as required which is an issue with &pi; and e.
Moreover, `math` and `numpy` return `float` values with stores
only a few digits after the dot. The computations above return
`Decimal` objects which has pre-specified accuracy.

Factorial faces another challenge: too large numbers. Python
handles this issue well: it does not have integer overflow issue.
Clearly, that would be a fair comparison between scientific formulas,
`math` package, and `numpy` package. Especially when numbers get
very large, and the time complexity is a game changer. However,
please be patient with this test -- it may be time-consuming.

## Installation and usage
Please make sure that `Docker` and `docker-compose` are installed. To start, clone
the repository in the preferred directory
```bash
git clone https://github.com/kate-melnykova/Efficient_computations_of_fn
```
To start the server, run
```bash
docker-compose up --build
```
The server should start automatically, and you will see the main page
![main page](https://github.com/kate-melnykova/Efficient_computations_of_fn/blob/master/docs/main_page.png "Main page")
Enter the parameter to see the comparison and press the button.
## Algorithm sources
Function `factorial.py` computes factorial by the formula introduced by
[Fikret Cihana, Fatih Aydinb, Adnan Fatih Kocamaz](https://pdfs.semanticscholar.org/7388/ef8a3fa31b2d01f2835b3beeccdb16c0616a.pdf)
(no parallel computing part) This method is claimed to be
significantly faster than recursive implementation.

Function `compute_pi.py` uses [Chudnovsky algorithm](https://en.wikipedia.org/wiki/Chudnovsky_algorithm)
for computing the value of pi.

Function `compute_e.py` utilizes [Brothers' Formulae](https://www.intmath.com/exponential-logarithmic-functions/calculating-e.php)


