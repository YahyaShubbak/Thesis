# $cleanup_mode = 1;
$out_dir = "technical/build";
$bibtex_use = 1.5;
$pdflatex = "lualatex -shell-escape -interaction=nonstopmode -halt-on-error -synctex=1 %O %S";
# $pdflatex = "pdflatex -interaction=nonstopmode -halt-on-error -synctex=1 %O %S";
$pdf_mode = 1;
@default_files = ("thesis.tex");
$clean_ext = "bbl run.xml auxlock TikZ/thesis-figure*.pdf thesis-figure*.log thesis-figure*.md5 thesis-figure*.run.xml thesis-figure*.dpth"
