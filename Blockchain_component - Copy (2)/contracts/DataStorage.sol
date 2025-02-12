// SPDX-License-Identifier: MIT
pragma solidity >=0.5.0 <0.9.0;
pragma experimental ABIEncoderV2; // Needed for encoding/decoding array of strings

contract DataStorage {
    struct DataEntry {
        string encodedData; // Encoded data from ML model
    }
    mapping(uint256 => DataEntry) public dataEntries; // Mapping to store data
    uint256 public dataCount; // Counter for stored data entries
    address public owner; // Owner of the contract

    event DataAdded(uint256 id, string encodedData); // Event for adding data
    // Constructor to set the contract owner
    constructor() public {
        owner = msg.sender;
    }

    // Modifier to restrict access to the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }
    // Function to add a single encoded data entry
    function addData(string memory _encodedData) public onlyOwner {
        dataEntries[dataCount] = DataEntry(_encodedData);
        emit DataAdded(dataCount, _encodedData);
        dataCount++;
    }
    // Function to add multiple encoded data entries in a batch
    function addBatchData(string[] memory _encodedData) public onlyOwner {
        for (uint256 i = 0; i < _encodedData.length; i++) {
            dataEntries[dataCount] = DataEntry(_encodedData[i]);
            emit DataAdded(dataCount, _encodedData[i]);
            dataCount++;
        }
    }
    // Function to fetch all encoded data
    function getAllData() public view returns (string[] memory) {
        require(dataCount > 0, "No data available.");
        string[] memory allData = new string[](dataCount);
        for (uint256 i = 0; i < dataCount; i++) {
            allData[i] = dataEntries[i].encodedData;
        }
        return allData;
    }
}
