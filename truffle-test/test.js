var main =  artifacts.require("main");
var FE = artifacts.require("FE");


contract('testing main contract', async (accounts) => {

mainOwner = accounts[0];
//instance = await main.new();
  it("check owner", async () => {
      mainContract = await main.new(100);
      let ow = await mainContract.owner.call();
      let superNumber = await mainContract.superNumber.call();
      assert.equal(ow, mainOwner);
      assert.equal(superNumber, 100, 'incorrect superNumber');
  })

  it("update number", async () => {
     newNumber = 999;
     await mainContract.updateNumber(newNumber);
     superNumber = await mainContract.superNumber.call();
     assert.equal(superNumber, newNumber);
  })

  it("update name", async () => {
     newName = "truffle";
     await mainContract.updateName(newName);
     name = await mainContract.name.call();
     assert.equal(name, newName);
  })

  it("set uint array", async () => {
    uarr = [1,2,3,4,5];
    await mainContract.setAges(uarr);
    arrFromContract = await mainContract.ages.call(1);
    assert.equal(uarr[1],arrFromContract);
  })

  it("set bytes32", async () => {
    newStr = "privet";
    await mainContract.setBytes(web3.fromAscii(newStr));
    strFromContract = await mainContract.stroka.call();
    assert.equal(web3.toAscii(strFromContract).replace(/\u0000/g, ''),newStr);
  })

  it("set string", async () => {
    news = "lalala"
    await mainContract.setS(news);
    stringFromContract = await mainContract.ns.call();
    assert.equal(news,stringFromContract);
  })

  it("set new onwer", async () => {
    newOwner = accounts[1];
    await mainContract.setNewOwner(newOwner);
    ownerFromContract = await mainContract.owner.call();
    assert.equal(newOwner,ownerFromContract);
  })

  it("set new onwer - way2", async () => {
    newOwner = "0xe9ad0f9e7739a9db0015a410ec0758141d3cd9ca";
    await mainContract.setNewOwner(newOwner);
    ownerFromContract = await mainContract.owner.call();
    assert.equal(newOwner,ownerFromContract);
  })

  it("set struct", async () => {
    await mainContract.setStruct();
    lens = await mainContract.ls.call();
    structFromContract = await mainContract.peoples.call(0);
    assert.equal("ivan",structFromContract[0]);
  })

  it("get bool", async () => {
    boolvar = await mainContract.rb.call();
    assert.equal(true,boolvar);
  })

  it("check require", async () => {
    try {
    boolvar = await mainContract.tr.call({from: accounts[1]});
    assert.isTrue(false,"tx is ok");

  }
  catch(error) {
      assert.isTrue(true,"Error - " + error);
    }

  })

  it("check balance", async () => {
    accBalance = web3.eth.getBalance(accounts[0]);
    assert.isTrue(accBalance > 0 ? true:false);
  })

  it("deploy contracts ", async () => {
    await mainContract.deployAnotherContract();
    bb = await mainContract.newContract.call();
  })

  it("read var from another contract", async () => {
    FEContract = FE.at(bb);
    varAA = await FEContract.aa.call();
    assert.equal(varAA,55);
  })

  it("read private var from stoarage", async () => {
    privVar = await web3.eth.getStorageAt(mainContract.address, 0)
  })

  it("play with time", async () => {
    await mainContract.funTime();
    neoTime1 = await mainContract.neoTime.call();
    assert.isTrue(neoTime1 > 0 ? true: false);
    await web3.currentProvider.send({
        jsonrpc: "2.0",
        method: "evm_increaseTime",
        params: [999999],
        id: 0
    });
    await web3.currentProvider.send({jsonrpc: "2.0", method: "evm_mine", params: [], id: 0})
    await mainContract.funTime();
    neoTime2 = await mainContract.neoTime.call();
    assert.isTrue(neoTime2-neoTime1>=999999 ? true : false);
  })


















});
