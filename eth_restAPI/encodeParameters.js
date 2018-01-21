Web3 = require('web3')
web3 = new Web3()
typesArray = JSON.parse(process.argv[2])
parameters = JSON.parse(process.argv[3])
typesArray.map((t, i) => {
  if(t == 'bytes32') parameters[i] = web3.utils.toHex(parameters[i])
})
encodedParameters = web3.eth.abi.encodeParameters(typesArray, parameters);
console.log(encodedParameters)

