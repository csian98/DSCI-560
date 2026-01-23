from logparser.Drain import LogParser

log_format = "<Month> <Day> <Time> <Host> <Process>: <Content>"

parser = LogParser(
    log_format=log_format,
    indir="../data/raw/",
    outdir="../data/drain/",
    depth=4,	# parse tree depth
    st=0.4		# similarity threshold
)

parser.parse("Linux_2k.log")
