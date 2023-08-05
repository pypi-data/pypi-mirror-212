import os
import zipfile


class abmatrix:
    def __init__(self):
        self.filename = ""
        self.iszip = False
        self.header = {}
        self.index = {}
        self.sample_index = {}

    def open(self, filename):
        if os.path.isfile(filename):
            self.filename = filename
            if zipfile.is_zipfile(filename):
                self.iszip = True
                zipstream = zipfile.ZipFile(filename, "r")
                self.fstream = zipstream.open("-", "r")
            else:
                self.fstream = open(filename, "r")
            offset = 0
            first_line = next(self.fstream)
            offset += len(first_line)
            is_header = True
            for line in self.fstream:
                if self.iszip:
                    line = line.decode("utf-8")
                if is_header:
                    if line.startswith("[Data]"):
                        sample_header = next(self.fstream)
                        if self.iszip:
                            sample_header = sample_header.decode("utf-8")
                        offset += len(sample_header)
                        sample_list = sample_header.rstrip("\n").split("\t")[1:]
                        for pos, sample in enumerate(sample_list):
                            self.sample_index[sample] = pos
                        is_header = False
                    else:
                        entry = line.rstrip("\n").split("\t")
                        if len(entry) < 2:
                            raise Exception("Malformed header")
                        else:
                            self.header[entry[0]] = entry[1]
                else:
                    locus_id = line.rstrip("\n").split("\t")[0]
                    self.index[locus_id] = offset
                offset += len(line)
        else:
            raise FileNotFoundError

    def locus(self, locus_id):
        output_list = []
        if type(locus_id) == list:
            for locus in locus_id:
                try:
                    offset = self.index[locus]
                except KeyError:
                    raise e
                else:
                    self.fstream.seek(offset)
                    line = self.fstream.readline()
                    if self.iszip:
                        line = line.decode("utf-8")
                    output_list.append(line.rstrip("\n"))
        else:
            try:
                offset = self.index[locus_id]
            except KeyError as e:
                raise e
            else:
                self.fstream.seek(offset)
                line = self.fstream.readline()
                if self.iszip:
                    line = line.decode("utf-8")
                output_list.append(line.rstrip("\n"))

        return output_list

    def samplelist(self):
        samplelist = [None] * len(self.sample_index)
        for key, value in self.sample_index.items():
            samplelist[value] = key
        return samplelist

    def genotype(self, locus_id, sample_id):
        output_list = []
        try:
            offset = self.index[locus_id]
        except KeyError as e:
            raise e
        else:
            self.fstream.seek(offset)
            line = self.fstream.readline()
            if self.iszip:
                line = line.decode("utf-8")
            locus_line = line.rstrip("\n").split("\t")
            _ = locus_line.pop(0)
            try:
                pos = self.sample_index[sample_id]
            except KeyError as e:
                raise e
            else:
                output_list.append(locus_line[pos])
        return output_list

    def close(self):
        self.fstream.close()
