var FreeToken =  artifacts.require("FreeToken");

contract('testing FreeCoin contract', async (accounts) => {
owner = accounts[0];
user = accounts[1];


  it("deploy contract and check variables", async () => {
      name = "FreeToken";
      symbol = "FT";
      decimals = 8;
      FreeTokenContract = await FreeToken.new(name,symbol, decimals);
      contractOwner = await FreeTokenContract.owner.call();
      contractName = await FreeTokenContract.name.call();
      contractSymbol = await FreeTokenContract.symbol.call();
      contractDecimals = await FreeTokenContract.decimals.call();
      needWei = await FreeTokenContract.needWei.call();
      assert.equal(contractOwner, owner);
      assert.equal(contractName, name);
      assert.equal(contractSymbol, symbol);
      assert.equal(contractDecimals, decimals);
      assert.equal(needWei, 100);
  })

  it("try get FreeToken right after deploy and we can't do it", async () => {
    try {
      await FreeTokenContract.getFreeToken({from: user, value: 100});
      assert.isTrue(false,"tx is ok");
        }
    catch(error) {
      assert.isTrue(true);
    }
  })



  it("increase time, but send 50 wei. Tx should be fail", async () => {
    await web3.currentProvider.send({
        jsonrpc: "2.0",
        method: "evm_increaseTime",
        params: [4000],
        id: 0
    });
    await web3.currentProvider.send({jsonrpc: "2.0", method: "evm_mine", params: [], id: 0})
    try {
      await FreeTokenContract.getFreeToken({from: user, value: 50});
      assert.isTrue(false,"tx is ok");
        }
    catch(error) {
      assert.isTrue(true);
    }
  })

  it("send correct amount of wei", async () => {
      await FreeTokenContract.getFreeToken({from: user, value: 100});
      amountOfToken = await FreeTokenContract.balances.call(user);
      assert.equal(amountOfToken,1);
  })
})
