use warnings;
use strict ;

my $in = "all.tuna.maf";
my $out = "$0.out";

my %hash ;
$/ = 'a score=';
open O , "> $out";
open I , "< $in";
while (<I>){
	chomp;
	next if /^#/ ;
	my @a = split /\n+/,$_;
	shift @a ;
	next if @a<10 ; ###the species
	my $light = 1 ;
	my $line = "<\n";
	foreach my $a (@a){
		my @b = split /\s+/,$a ;
		next if @b<6;
		my $id = "$b[1]:$b[2]:$b[3]:$b[4]:$b[5]";
		my $fasta = $b[6];
		my $len = ($fasta =~ s/([a-zA-Z])/$1/g);
		if ($len < 23){
			$light = 0 ;
			last ;
		}
		$line .= sprintf (">%-60s $fasta\n",$id);
	}
	next if ($light == 0) ;
	print O "$line\n";
}
close I ;
close O ;
