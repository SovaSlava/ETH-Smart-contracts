var Migrations = artifacts.require("./Migrations.sol");
var vote = artifacts.require("./vote.sol");
module.exports = function(deployer, network, accounts) {
  deployer.deploy(Migrations);
  deployer.deploy(vote,accounts[1], accounts[2], 1544572800);
};
