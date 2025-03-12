$cleanup_mode = 1;
$out_dir = "technical/build";
$bibtex_use = 1.5;
# $pdflatex = "lualatex -interaction=nonstopmode -halt-on-error %O %S";
$pdflatex = "pdflatex -interaction=nonstopmode -halt-on-error %O %S";
$pdf_mode = 1;
@default_files = ("thesis.tex");
$clean_ext = "bbl run.xml"
