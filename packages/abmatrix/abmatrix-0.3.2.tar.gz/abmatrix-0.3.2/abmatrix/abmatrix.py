import os
import zipfile


class abmatrix:
    def __init__(self):
        self.filename = ""
        self.iszip = False
        self.header = {}
        self.index = {}
        self.sample_index = {}

    def read(self, filename):
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
                        elif len(entry) > 2:
                            nread = 0
                            key = ""
                            value = ""
                            for elem in entry:
                                if len(elem) > 1:
                                    if nread < 1:
                                        key = elem
                                        nread += 1
                                    else:
                                        value = elem
                                        break
                            self.header[key] = value
                        else:
                            self.header[entry[0]] = entry[1]
                else:
                    locus_id = line.rstrip("\n").split("\t")[0]
                    self.index[locus_id] = offset
                offset += len(line)
        else:
            raise FileNotFoundError

    def write(self, filename, genotypes):
        # Update header metadata
        new_sample_list = []
        for key in genotypes[0].keys():
            if key != "id":
                new_sample_list.append(key)
        new_sample_size = len(new_sample_list)
        new_locus_size = len(genotypes)
        new_header = self.header
        new_header["Num Samples"] = new_sample_size
        new_header["Total Samples"] = new_sample_size
        new_header["Num SNPs"] = new_locus_size
        new_header["Total SNPs"] = new_locus_size

        with open(filename, "w") as f:
            f.write("[Header]\n")
            for key, value in new_header.items():
                f.write("{}\t{}\n".format(key, value))
            f.write("[Data]\n")
            sample_header = "\t".join(new_sample_list)
            f.write("\t{}\n".format(sample_header))
            for locus in genotypes:
                f.write(locus["id"])
                for sample in new_sample_list:
                    f.write("\t{}".format(locus[sample]))
                f.write("\n")

    def subset(self, locus_list, **kwargs):
        output_list = []
        if "samples" in kwargs:
            sample_list = kwargs["samples"]
        else:
            sample_list = list(self.sample_index.keys())
        if type(locus_list) != list:
            raise Exception("reduce needs list of locus identifiers")
        for locus in locus_list:
            locus_dict = {"id": locus}
            try:
                offset = self.index[locus]
            except KeyError:
                for sample_id in sample_list:
                    locus_dict[sample_id] = "--"
            else:
                self.fstream.seek(offset)
                line = self.fstream.readline()
                if self.iszip:
                    line = line.decode("utf-8")
                locus_array = line.rstrip("\n").split("\t")
                _ = locus_array.pop(0)
                for sample_id in sample_list:
                    try:
                        pos = self.sample_index[sample_id]
                    except KeyError as e:
                        raise e
                    else:
                        locus_dict[sample_id] = locus_array[pos]
            finally:
                output_list.append(locus_dict)
        return output_list

    def close(self):
        self.fstream.close()
