// SPDX-License-Identifier: MIT
pragma solidity >=0.5.0 <0.9.0;
pragma experimental ABIEncoderV2;

contract DataStorage {
    string public encodedZipFile;

    event ZipFileStored(string indexed zipData);

    function storeZipFile(string memory _zipData) public {
        encodedZipFile = _zipData;
        emit ZipFileStored(encodedZipFile);
    }

    function getZipFile() public view returns (string memory) {
        return encodedZipFile;
    }
}