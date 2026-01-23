from logparser.Spell import LogParser

log_format = "<Month> <Day> <Time> <Host> <Process>: <Content>"

parser = LogParser(
    log_format=log_format,
    indir="../data/raw/",
    outdir="../data/spell/",
    tau=0.5		# LCS similarity threshold
)

parser.parse("Linux_2k.log")
