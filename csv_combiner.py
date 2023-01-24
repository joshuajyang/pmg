# command line program that takes several CSV files as arguments
# outputs to stdout containing rows from each argument with additional column with files from which the row came (basename)

import pandas
import os
import sys

class CombineCsvClass:
    @staticmethod # dont need instance of class before using so can be static
    # check if files exist
    def checkfiles(argv):
        # check for no args
        if len(argv) <= 1:
            print("error: no files for the arguments")
            return False

        filelist = argv[1:]
        # check each file in list
        for file in filelist:
            # if file does not exist in directory
            if not os.path.exists(file):
                print("error: file or directory invalid " + file)
                return False
        # otherwise files exist
        return True

    def combinefiles(self, argv: list):
        # temp list to store chunks
        chunklist = []
        # check the files using helper method
        if self.checkfiles(argv):
            filelist = argv[1:]

            for file in filelist:
                # read as chunks of 10000 lines to handle larger files gracefully (interpret as DataFrames)
                for chunk in pandas.read_csv(file, chunksize=10000):
                    # add additional filename column with base name of the specified path
                    chunk['filename'] = os.path.basename(file)
                    # add the chunk to the temp list of chunks
                    chunklist.append(chunk)

            # combine chunks within chunklist
            for i, chunk in enumerate(chunklist):
                # only want header for first chunk
                if i == 0:
                    print(chunk.to_csv(header=True, index=False, quoting=1, lineterminator='\n', chunksize=10000), end='')
                else:
                    print(chunk.to_csv(header=False, index=False, quoting=1, lineterminator='\n', chunksize=10000), end='')

# main method
def main():
    # create instance of class and combine files using command line arguments
    CombineCsvClass().combinefiles(sys.argv)

if __name__ == "__main__":
    main()