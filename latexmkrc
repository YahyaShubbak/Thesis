# $cleanup_mode = 1;
$out_dir = "technical\\build";
$bibtex_use = 1.5;
$pdf_previewer = "start c:\\Users\\YaSh\\AppData\\Local\\SumatraPDF\\SumatraPDF.exe %O %S";
$pdflatex = "lualatex -shell-escape -interaction=nonstopmode -halt-on-error -synctex=0 %O %S";
# $pdflatex = "pdflatex -interaction=nonstopmode -halt-on-error -synctex=1 %O %S";
$pdf_mode = 4;
@default_files = ("thesis.tex");
$clean_ext = "bbl run.xml auxlock TikZ\\thesis-figure*.pdf thesis-figure*.log thesis-figure*.md5 thesis-figure*.run.xml thesis-figure*.dpth";
