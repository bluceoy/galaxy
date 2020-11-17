my $rpath = `which R`;
`$rpath CMD BATCH --args dataset_3665.dat.tmp.R`;
