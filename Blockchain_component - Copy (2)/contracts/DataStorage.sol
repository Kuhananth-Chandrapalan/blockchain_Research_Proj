// SPDX-License-Identifier: MIT
pragma solidity >=0.5.0 <0.9.0;
pragma experimental ABIEncoderV2;

contract DataStorage {
    struct FileData {
        string fileName;
        string encodedZipFile;
    }

    mapping(uint256 => FileData) public storedFiles;
    uint256 public fileCount;

    event ZipFileStored(uint256 indexed id, string fileName);

    function storeZipFile(string memory _fileName, string memory _zipData) public {
        storedFiles[fileCount] = FileData(_fileName, _zipData);
        emit ZipFileStored(fileCount, _fileName);
        fileCount++;
    }

    function getFileNames() public view returns (string[] memory) {
        string[] memory fileNames = new string[](fileCount);
        for (uint256 i = 0; i < fileCount; i++) {
            fileNames[i] = storedFiles[i].fileName;
        }
        return fileNames;
    }

    function getZipFile(uint256 _fileId) public view returns (string memory) {
        require(_fileId < fileCount, "Invalid file ID");
        return storedFiles[_fileId].encodedZipFile;
    }
}
