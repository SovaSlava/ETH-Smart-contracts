var vote =  artifacts.require("vote");

contract('Vote contract', async (accounts) => {
  owner = accounts[0];
  it("check owner", async () => {
     voteContract = await vote.new(accounts[1], accounts[2], 1544572800);
     let owner = await voteContract.owner.call();
     assert.equal(owner, accounts[0]);
 })

 it("voting for first candidat", async () => {
    await voteContract.makeVote(1);
    votesCount = await voteContract.votes.call(accounts[1]);
    assert.equal(votesCount, 1);
})

it("voting for first candidat without changig account, we should get an error", async () => {
  try {
    await voteContract.makeVote(1);
    assert.isTrue(false,"tx is ok");
}
catch(error) {
    assert.isTrue(true);
  }
})

it("voting for second candidat", async () => {
   await voteContract.makeVote(2, {from: accounts[5]});
   votesCount = await voteContract.votes.call(accounts[2]);
   assert.equal(votesCount, 1);
})

it("voting for second candidat again", async () => {
   await voteContract.makeVote(2, {from: accounts[6]});
   votesCount = await voteContract.votes.call(accounts[2]);
   assert.equal(votesCount, 2);
})

it("try finish vote before end date, we should get an error", async () => {
  try {
    await voteContract.finishVote();
    assert.isTrue(false,"tx is ok");
}
catch(error) {
    assert.isTrue(true);
  }
})

it("finish voting after increase time", async () => {
  await web3.currentProvider.send({
      jsonrpc: "2.0",
      method: "evm_increaseTime",
      params: [131536000],
      id: 0
  });
  await web3.currentProvider.send({jsonrpc: "2.0", method: "evm_mine", params: [], id: 0})
   await voteContract.finishVote();
   whoWin = await voteContract.whoWin.call();
   assert.equal(whoWin, accounts[2]);
})

})
