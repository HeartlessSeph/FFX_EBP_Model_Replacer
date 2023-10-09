from binary_reader import BinaryReader
from pathlib import Path
import argparse


def model_check(num):
    num = abs(num)
    mNum = num
    numStr = str(num)

    if 4 <= len(numStr):
        num1 = int(numStr[:1])
        num2 = int(numStr[-3:])
        mNum = (num1 * 4096) + num2
    return mNum


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-p', '--path', action='store', help='Path')
    parser.add_argument('-s', '--search', action='append', help='Model search num')
    parser.add_argument('-r', '--replace', action='append', help='Model replace num')
    parser.add_argument('-b', '--batch', action='store_true', help='Run on folder instead of file')
    parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite original file(s)')
    parser.add_argument('-d', '--delete', action='store_true', help='Delete file(s) if no matches are found')

    args = parser.parse_args()

    if args.path is None:
        raise Exception("The path argument is required to run this program.")
    if args.search is None or args.replace is None:
        raise Exception("Must have at least one model search and model replace to run this program.")
    if len(args.search) != len(args.replace):
        raise Exception("The number of model searches must match the number of model replacements.")
    modelSearch = [model_check(int(i)) for i in args.search]
    modelReplace = [model_check(int(i)) for i in args.replace]
    modelDict = dict(zip(modelSearch, modelReplace))
    mSearches = ','.join([str(x) for x in modelSearch])

    basePath = Path(args.path).resolve()
    mFiles = [Path(x) for x in basePath.glob('**/*.ebp') if x.is_file()] if args.batch else [basePath]

    for binFile in mFiles:
        searchFound = 0
        binName = binFile.stem
        print("Reading " + binName + ".ebp")
        binPath = binFile.parent
        suffix = "_conv.ebp"
        if args.overwrite:
            suffix = ".ebp"
        newBin = binName + suffix
        newBinString = str(binPath / newBin)
        with open(binFile, 'rb') as f:
            reader = BinaryReader(f.read())
        if reader.size() == 0:
            print("File contains no data. File will be skipped.")
            continue
        writer = BinaryReader()

        readerBytes = reader.read_bytes(reader.size())
        writer.write_bytes(readerBytes)

        instructionSplit = readerBytes.split(b'\xD8\x01\x00')[:-1]
        curPos = 0
        for i in instructionSplit:
            if curPos == 0:
                reader.seek(len(i) - 2)
            else:
                reader.seek(curPos + len(i) - 2)
            curModel = reader.read_uint16()
            if curModel in modelDict:
                writer.seek(reader.pos() - 2)
                print("Model number " + str(curModel) + " replaced with " + str(modelDict[curModel]) + " at offset " + str(writer.pos()))
                writer.write_uint16(modelDict[curModel])
                searchFound += 1
            curPos = reader.pos() + 3

        if searchFound == 0:
            print("No instances of model numbers " + mSearches + " was found. No file will be written")
            if args.delete:
                print("File deleted.")
                binFile.unlink()
        else:
            with open(binPath / newBin, 'wb') as f:
                f.write(writer.buffer())
                print("File written to " + newBinString + ".")
        print("")
