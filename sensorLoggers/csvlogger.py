import logging
import csv
import cfg
import logentry
import abssensorlogger
class Logger(abssensorlogger.Logger):
    def __init__(self):
        self.logger = logging.getLogger("PB.logger.csv")
        self.logger.info("Starting with target: %s", cfg.cfg["logTarget"])
        self.fieldnames = ["time", "currentInReading","currentOutReading","voltageReading","luxReading","relayStatus"]
        self.writer = csv.DictWriter(open(cfg.cfg["logTarget"], 'w'), fieldnames=self.fieldnames)
        self.writer.writeheader()
    def recordEntry(self, entry):
        assert type(entry) == logentry.Entry
        self.logger.debug("Writing %s", repr(entry))
        self.writer.writerow(entry)
