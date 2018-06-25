var Web3 = require('web3');
//var web3 = new Web3();
window.addEventListener("load", function() {
  // Checking if Web3 has been injected by the browser (Mist/MetaMask)
  if (typeof web3 !== "undefined") {
    // Use Mist/MetaMask's provider
    window.web3 = new Web3(web3.currentProvider);
    console.log("metamask found " + web3.currentProvider);
  }
  else {

    $('#metamaskalert').show();
  }

  var contractDesc = [
	{
		"constant": false,
		"inputs": [],
		"name": "finishVote",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": false,
		"inputs": [
			{
				"name": "_vote",
				"type": "uint256"
			}
		],
		"name": "makeVote",
		"outputs": [],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"name": "_candidatA",
				"type": "address"
			},
			{
				"name": "_candidatB",
				"type": "address"
			},
			{
				"name": "_endVoteDate",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "candidatA",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "candidatB",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "endVoteDate",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "needAnotherVote",
		"outputs": [
			{
				"name": "",
				"type": "bool"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"name": "voteOptions",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"name": "votes",
		"outputs": [
			{
				"name": "",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "whoWin",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
];

          //web3.eth.contract(abi).at(address)
          var contract = web3.eth.contract(contractDesc).at("0x0191a6c8b50933802d85df5751aa1d7d6903836d");

          contract.endVoteDate.call(function(err, result) {

        var unix = Math.round(+new Date()/1000);
        if(unix > result) {
          $('#vote1').hide();
          $('#vote2').hide();
          $('#vote3').hide();
          contract.needAnotherVote.call(function(err, needAnotherVote) {
              contract.whoWin.call(function(err, whoWin) {
                if(needAnotherVote==true || whoWin != "0x0000000000000000000000000000000000000000") {
                  $('#voteStatus').append("<h1>Голосование уже закончено - результат на диаграмме ниже</h1>");
                }
                else {
                    $('#finishVote').show();
                  }
                })
              })

          }})


  $( "#finishVoteButton" ).click(function() {
    contract.finishVote.sendTransaction({from: web3.eth.accounts[0]}, function(err) {
      console.log(err);
    });
});
            $( "#vote1" ).click(function() {
  contract.makeVote.sendTransaction(1, {from: web3.eth.accounts[0]}, function(err, result) {
    console.log("res - " + result);
  })});

  $( "#vote2" ).click(function() {
contract.makeVote.sendTransaction(2, {from: web3.eth.accounts[0]}, function(err, result) {
console.log("res - " + result);
})});

$( "#vote3" ).click(function() {
contract.makeVote.sendTransaction(3, {from: web3.eth.accounts[0]}, function(err, result) {
console.log("res - " + result);
})});


  contract.candidatA.call(function (err, result) {
      candidatAAdress = result;
      contract.candidatB.call(function (err, result) {
        candidatBAdress = result;
        contract.votes.call(candidatAAdress, function (err, votesAmountA) {
          candidatAVotes = votesAmountA;
          contract.votes.call(candidatBAdress, function (err, votesAmountB) {

              //console.log("window.candidatA - " + window.candidatA);

              candidatBVotes = votesAmountB;
              allvotes =  parseInt(candidatAVotes) +  parseInt(candidatBVotes);
              percentA = 100 * candidatAVotes / allvotes;
              percentB = 100 * candidatBVotes / allvotes;

              $("#chartContainer").CanvasJSChart({
                  title: {
                    text: "Текущие результаты",
                    fontSize: 24
                  },
                  axisY: {
                    title: ""
                  },
                  legend :{
                    verticalAlign: "center",
                    horizontalAlign: "right"
                  },
                  data: [
                  {
                    type: "pie",
                    showInLegend: true,
                    toolTipContent: "{label} <br/> {y} %",
                    indexLabel: "",
                    dataPoints: [
                      { label: "Иванов Иван",  y: percentA, legendText: "Иванов Иван"},
                      { label: "Иванова Анна ",    y: percentB, legendText: "Иванова Анна"  },

                    ]
                  }
                ]


              })


          });
      });
});
});

})
