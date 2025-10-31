// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract DegreeVerification {
    struct Degree {
        string studentName;
        string course;
        uint256 year;
        bool verified;
    }

    mapping(uint256 => Degree) public degrees;
    uint256 public degreeCount;
    address public owner;

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Not authorized");
        _;
    }

    function issueDegree(string memory _name, string memory _course, uint256 _year) public onlyOwner {
        degrees[degreeCount] = Degree(_name, _course, _year, true);
        degreeCount++;
    }

    function verifyDegree(uint256 _id) public view returns (bool) {
        return degrees[_id].verified;
    }
}
