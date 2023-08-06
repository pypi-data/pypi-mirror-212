#!/usr/bin/env python
# Copyright 2018 - 2020 H2O.ai;  -*- encoding: utf-8 -*-

import datatable
import daimojo.cppmojo
import os
import sys
import time
from datetime import datetime


class model:
    def __init__(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)

        self.modelfile = os.path.abspath(filename)
        self.cppmodel = daimojo.cppmojo.model(self.modelfile, daimojo.__path__[0])

        if not self.cppmodel.is_valid():
            print("Driverless AI license error!", file=sys.stderr)
            sys.stderr.flush()
            sys.exit(-1)

        self.uuid = self.cppmodel.uuid()
        self.mojo_version = self.cppmodel.mojo_version()
        self.created_time = time.ctime(self.cppmodel.created_time())
        self.missing_values = self.cppmodel.missing_values()
        self.feature_names = self.cppmodel.feature_names()
        self.feature_types = self.cppmodel.feature_types()
        self.output_names = self.cppmodel.output_names()
        self.output_types = self.cppmodel.output_types()
        self.format_string = self.cppmodel.format_string()
        self.has_treeshap = self.cppmodel.has_treeshap()
        self.dai_version = self.cppmodel.dai_version()
        self.transformed_names = self.cppmodel.transformed_names()

    def predict(self, pydt, pred_contribs=False, debug=False):
        if type(pydt) != datatable.Frame:
            print("datatable.Frame expected!", file=sys.stderr)
            sys.stderr.flush()
            sys.exit(-1)

        if pred_contribs:
            if self.dai_version == "":
                print("'pred_contribs' is only support with mojo file generated from DAI 1.9.0 or later.", file=sys.stderr)
                sys.stderr.flush()
                sys.exit(-1)

            dai_version_major = self.dai_version.split(".")[0]
            dai_version_minor = self.dai_version.split(".")[1]
            if int(dai_version_major) < 1 or int(dai_version_minor) < 9:
                print("'pred_contribs' is only support with mojo file generated from DAI 1.9.0 or later.", file=sys.stderr)
                sys.stderr.flush()
                sys.exit(-1)

        pydt_col_names = pydt.names

        missing_cols = list(set(self.feature_names) - set(pydt_col_names))

        if missing_cols:
            missing_col_info = ''
            for c in missing_cols:
                missing_col_info += c + '(' + self.feature_types[self.feature_names.index(c)] + '); '
            print('Column(s) missing: ' + missing_col_info, file=sys.stderr)
            sys.stderr.flush()
            sys.exit(-1)

        pydt = pydt[:, self.feature_names]

        str_col_id = []

        for i in range(pydt.ncols):
            if self.feature_types[i] == "bool":
                pydt[:, i] = datatable.bool8(datatable.f[i])
            elif self.feature_types[i] == "int32":
                pydt[:, i] = datatable.int32(datatable.f[i])
            elif self.feature_types[i] == "int64":
                pydt[:, i] = datatable.int64(datatable.f[i])
            elif self.feature_types[i] == "float32":
                pydt[:, i] = datatable.float32(datatable.f[i])
            elif self.feature_types[i] == "float64":
                pydt[:, i] = datatable.float64(datatable.f[i])
            elif self.feature_types[i] == "string":
                pydt[:, i] = datatable.str32(datatable.f[i])
                str_col_id.append(i)
            else:
                print("unknown feature type: " + self.feature_types[i], file=sys.stderr)
                sys.stderr.flush()
                sys.exit(-1)

        nrow = pydt.nrows

        py_list = pydt.to_list()
        del pydt

        # format string not empty
        # the purpose of this step is to 'reformat' the datetime strings
        # some strings, like '9 Jan 2015' cannot be properly handled by libc
        # in some Linux distributions (like CentOS 7),
        # due to the missing '0' before '9'
        if self.format_string:
            for k in self.format_string.keys():
                idx_k = self.feature_names.index(k)
                fmt_str = self.format_string[k]
                col_k = py_list[idx_k]
                py_list[idx_k] = [datetime.strptime(d, fmt_str).strftime(fmt_str) for d in col_k]

        out_list = self.cppmodel.predict(py_list, nrow, pred_contribs, debug)

        pydt_output = datatable.Frame(out_list)

        if pred_contribs:
            pred_contrib_names = self.cppmodel.pred_contrib_names()
            output_names = pred_contrib_names

            pydt_output.names = output_names

            return pydt_output[:, pred_contrib_names]
        elif debug:
            pydt_output.names = self.cppmodel.output_names()
        else:
            pydt_output.names = self.cppmodel.output_names()

            for i in range(pydt_output.ncols):
                if self.output_types[i] == "bool":
                    pydt_output[:, i] = datatable.bool8(datatable.f[i])
                elif self.output_types[i] == "int32":
                    pydt_output[:, i] = datatable.int32(datatable.f[i])
                elif self.output_types[i] == "int64":
                    pydt_output[:, i] = datatable.int64(datatable.f[i])
                elif self.output_types[i] == "float32":
                    pydt_output[:, i] = datatable.float32(datatable.f[i])
                elif self.output_types[i] == "float64":
                    pydt_output[:, i] = datatable.float64(datatable.f[i])
                elif self.output_types[i] == "string":
                    pydt_output[:, i] = datatable.str32(datatable.f[i])
                else:
                    print("unknown output type: " + self.output_types[i], file=sys.stderr)
                    sys.stderr.flush()
                    sys.exit(-1)

        return pydt_output
