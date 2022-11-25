import timeit
from jpylyzer import jpylyzer
import os
import json
from argparse import ArgumentParser


def get_jp2_files(main_dir):
    """
    Get all the file paths to files which end with jp2, we could also do that
    via passing the siegfried log to identify the files we need but this might
    be the easier and more user-friendly approach
    :param main_dir:
    :return:
    """
    jp2_file_paths = []
    for dirpath, subdirs, files in os.walk(main_dir):
        for f in files:
            if f.endswith("jp2"):
                jp2_file_paths.append(os.path.join(dirpath, f))
    return jp2_file_paths


def create_jpylyzer_info(fp):
    jp_info = {"file": {"fileInfo": {"fileName": "KACKA",
                                     "filePath": "",
                                     "fileLastModified": ""},
                        "isValid": "",
                        "properties": {"contiguousCodestreamBox":
                                           {"cod":
                                               {"order": "",
                                                "sop": "",
                                                "eph": "",
                                                "codeBlockWidth": "",
                                                "codeBlockHeight": "",
                                                "transformation": "",
                                                "layers": "",
                                                "levels": "",
                                               },
                                            "com":
                                                {"comment": "",
                                                 },
                                           },
                                       },

                        },
               "toolInfo": {"toolVersion": ""}
               }
    xml_base = jpylyzer.checkOneFile(fp)
    name = xml_base.findtext('./fileInfo/fileName')
    path = xml_base.findtext('./fileInfo/filePath')
    is_valid = xml_base.findtext('./isValid')
    prop_ccb_cod_order = xml_base.findtext('./properties/contiguousCodestreamBox/cod/order')
    prop_ccb_cod_sop = xml_base.findtext('./properties/contiguousCodestreamBox/cod/sop')
    prop_ccb_cod_eph = xml_base.findtext('./properties/contiguousCodestreamBox/cod/eph')
    prop_ccb_cod_cbw = xml_base.findtext('./properties/contiguousCodestreamBox/cod/codeBlockWidth')
    prop_ccb_cod_cbh = xml_base.findtext('./properties/contiguousCodestreamBox/cod/codeBlockHeight')
    prop_ccb_cod_trans = xml_base.findtext('./properties/contiguousCodestreamBox/cod/transformation')
    prop_ccb_cod_layers = xml_base.findtext('./properties/contiguousCodestreamBox/cod/layers')
    prop_ccb_cod_levels = xml_base.findtext('./properties/contiguousCodestreamBox/cod/levels')
    prop_ccb_com_comment = xml_base.findtext('./properties/contiguousCodestreamBox/com/comment')
    tool_version = jpylyzer.__version__
    jp_info["toolInfo"]["toolVersion"] = tool_version
    jp_info["file"]["fileInfo"]["fileName"] = name
    jp_info["file"]["fileInfo"]["filePath"] = path
    jp_info["file"]["isValid"] = is_valid
    jp_info["file"]["properties"]["contiguousCodestreamBox"]["cod"]["order"]= prop_ccb_cod_order
    jp_info["file"]["properties"]["contiguousCodestreamBox"]["cod"]["sop"]= prop_ccb_cod_sop
    jp_info["file"]["properties"]["contiguousCodestreamBox"]["cod"]["eph"]= prop_ccb_cod_eph
    jp_info["file"]["properties"]["contiguousCodestreamBox"]["cod"]["codeBlockWidth"]= prop_ccb_cod_cbw
    jp_info["file"]["properties"]["contiguousCodestreamBox"]["cod"]["codeBlockHeight"]= prop_ccb_cod_cbh
    jp_info["file"]["properties"]["contiguousCodestreamBox"]["cod"]["transformation"]= prop_ccb_cod_trans
    jp_info["file"]["properties"]["contiguousCodestreamBox"]["cod"]["layers"]= prop_ccb_cod_layers
    jp_info["file"]["properties"]["contiguousCodestreamBox"]["cod"]["levels"]= prop_ccb_cod_levels
    jp_info["file"]["properties"]["contiguousCodestreamBox"]["com"]["comment"]= prop_ccb_com_comment
    return jp_info


def write_to_json(f_info, output_file):
    with open(output_file, 'a') as outfile:
        json.dump(f_info,outfile)
        outfile.write('\n')


def empty_file(output_file):
    open(output_file, "w").close()


def main(output_file, main_dir):
    start = timeit.default_timer()
    empty_file(output_file)
    stop = timeit.default_timer()
    empty_file_time = stop-start
    print(f"Time to empty file {empty_file_time}")
    start = timeit.default_timer()
    jp2_files = get_jp2_files(main_dir)
    stop = timeit.default_timer()
    get_jpfiles_time = stop - start
    print(f"Time to get jp2 files {get_jpfiles_time}")
    for jp_fp in jp2_files:
        start = timeit.default_timer()
        create_jpylyzer_info(jp_fp)
        jpylyzer_info = create_jpylyzer_info(jp_fp)
        stop = timeit.default_timer()
        creation_time = stop - start
        print(f"Creation of jpylyzer info takes {creation_time}")
        start = timeit.default_timer()
        write_to_json(jpylyzer_info, output_file)
        stop = timeit.default_timer()
        write_time = stop - start
        print(f"Writing of jpylyzer info takes {write_time}")


if __name__ == "__main__":
    parser = ArgumentParser(description="...")
    parser.add_argument("-main_dir", metavar="main_dir",
                        help="Path to the the dir with the jp2 files")
    parser.add_argument("-output_file", "--output_file",
                        dest="output_file",
                        help="Path to write the json file")
    args = parser.parse_args()
    main(args.output_file, args.main_dir)