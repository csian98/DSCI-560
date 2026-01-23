from logparser.IPLoM import LogParser

log_format = "<Month> <Day> <Time> <Host> <Process>: <Content>"

parser = LogParser(
    log_format=log_format,
    indir="../data/raw/",
    outdir="../data/iplom/",
)

parser.parse("Linux_2k.log")
