const { ethers } = require("hardhat");

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with account:", deployer.address);

  const Degree = await ethers.getContractFactory("DegreeVerification");
  const contract = await Degree.deploy();
  await contract.deployed();

  console.log("✅ DegreeVerification deployed at:", contract.address);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
