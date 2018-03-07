var main = artifacts.require('FreeToken');

module.exports = function(deployer, network, accounts) {
  deployer.deploy(main, "FreeToken", "FT", 8, {from:accounts[1]});
};
