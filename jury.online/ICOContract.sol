pragma solidity ^0.4.18;
import "./ERC20Token.sol";
import "./InvestContract.sol";




contract ICOContract {
    
    uint public constant openDisputDays = 5 days;
    uint public constant voteArbiterDays = 5 days;
    uint public constant voteSpareArbiterDays = 5 days;
    
    ///address of the project developer
    address public projectWallet; 

    ///Jury.online commission will be transfered to this address
    address public JuryOnlineComission = 0x123; //should be hardcoded

    ///Before this timestamp, projectWallet can add milestones
    uint public lastDateAddMilestone; 

    ///pending InvestContracts not yet accepted by the project
    address[] public pendingInvestContracts; 
    mapping(address => uint) public pendingInvestContractsIndices;

    ///accepted InvestContracts
    address[] public investContracts; // accepted invest contracts
    mapping(address => uint) public investContractsIndices;
    
    mapping(uint => string) public milestoneResult;
     
    ///When ICOContract is mutable project can add/change milestones. After the project seals by invoking seal()
    ///the contract it's no longer mutable.
    bool public mutable = true; 

    uint public amountOfEth; // how many eth need for all milestones
    uint public amountOfToken; // how many tokens developer will send during all milestones
    uint public commission; // Jury.Online commision
    Token public token;
    
    uint public investorEther;
    uint public investorTokens;
    
    ///ICO caps
    uint public minimumCap; // set in constructor
    uint public maximumCap;  // set in constructor

    mapping(address => uint[]) public ethInMilestone; // investContractAddress => Milestone => weis
    mapping(address => uint[]) public tokenInMilestone; // investContractAddress => Milestone => tokens

    enum MilestoneStatus {Waiting, Active, Checking, Finished}
    
    //Structure for milestone
    struct Milestone {
        uint etherAmount; //how many Ether is needed for this milestone
        uint tokenAmount; //how many tokens releases this milestone
        uint startTime;
        uint finishTime;
        string description; 
        string results;
        MilestoneStatus status;
    }

    Milestone[] public milestones;
    
    event MilestoneStarted(address indexed ICOContractAddress, uint indexed _MileStoneNumber);
    event MilestoneFinished(address indexed ICOContractAddress, uint indexed _MileStoneNumber);
    event InvestContractAccepted(address indexed ICOContractAddress);
    event investContractAdded(address indexed ICOContractAddress, address indexed InvestContractAddress);
    event investContractFunded(address indexed ICOContractAddress, address indexed InvestContractAddress);
    event DisputeOpened(address indexed _contractAddres, string _reason);
    event DisputeClosed(address indexed _contractAddres, uint whoWin);

    modifier only(address _sender) {
        require(msg.sender == _sender);
        _;
    }


    
    
    
    // OK
    function ICOContract(address _tokenAddress, address _projectWallet, uint _lastDateAddMilestone, uint _minimumCap,
                         uint _maximumCap) public {
        token = Token(_tokenAddress);
        projectWallet = _projectWallet;
        commission = 1;  // 1%
        lastDateAddMilestone = _lastDateAddMilestone;
        minimumCap = _minimumCap;
        maximumCap = _maximumCap;
    }

    // OK
    function createInvestContract(address _investor, uint _etherAmount, uint _tokenAmount)
        public
        //only(projectWallet)
        returns(address)
    {
        require(mutable == false);
        require(milestones[0].startTime - now >= 5 days);
        require(maximumCap >= _etherAmount + investorEther);
        require(token.balanceOf(address(this)) >= _tokenAmount + investorTokens);
        address investContract = new InvestContract(address(this), _investor, _etherAmount, _tokenAmount);
        pendingInvestContracts.push(investContract);
        pendingInvestContractsIndices[investContract]=(pendingInvestContracts.length); //note that indexes start from 1
        return(investContract);
    }
   
    // OK
    function getCurrentMilestone() public constant returns(uint) {
        for(uint i=0; i< milestones.length; i++) {
            if(milestones[i].startTime <= now && now <= milestones[i].finishTime + 7 days){
                return i;
            }
        }
        return 999; // not found
    }
   
       // OK
    function GetMilestones() public view returns( Milestone[]) {
        return milestones;
    }

    
    // OK
    function getMilestoneStatus(uint _milestone) public constant returns(uint) {
        return uint(milestones[_milestone].status);
    }
    
    // OK
    function isInvestorCanOpenDispute() public constant  returns(bool) {
        if(now >= milestones[getCurrentMilestone()].finishTime  && now <= milestones[getCurrentMilestone()].finishTime + openDisputDays) {
            return true;
        }
        else {
            return false;
        }
    }
    
    
    // OK
    function seal() public
    //only(projectWallet)
    {
        mutable = false;
    }
  
    // OK
    // deprecated
    function addMilestone(uint _etherAmount, uint _tokenAmount, uint _startTime, uint _finishTime,
                         string _milesoneDescription, string _milestoneResults) public  {
                             require(mutable == true);
        require(msg.sender == projectWallet);
        require(now <= lastDateAddMilestone && mutable == true);
        amountOfEth += _etherAmount;
        amountOfToken += _tokenAmount;
        milestones.push(Milestone(_etherAmount, _tokenAmount, _startTime, _finishTime, _milesoneDescription, _milestoneResults, MilestoneStatus.Waiting));
    }

  
    function updateMilestone(uint[5] _etherAmount, uint[5] _tokenAmount, uint[5] _startTime, uint[5] _finishTime,
                            byte[50][5] _description, byte[50][5] _results, bool _mutable) public 
                            //only(projectWallet)
                            {
        require(mutable == true);
        for(uint i=0; i<5; i++) {
            if(_finishTime[i] != 0) {
                amountOfEth += _etherAmount[i];
                amountOfToken += _tokenAmount[i];
                milestones.push(Milestone(_etherAmount[i], _tokenAmount[i], _startTime[i], _finishTime[i], 
                                            bytes32ToStr(_description[i]), bytes32ToStr(_results[i]), MilestoneStatus.Waiting));
            }
        }
        if(_mutable == false) {
            mutable = false;
        }
    }
    
    
    function editMilestone(uint _milestoneID, uint _etherAmount, uint _tokenAmount, uint _startTime, uint _finishTime,
                         string _milesoneDescription, string _milestoneResults, uint _status) public {
    // onlyProject
        require(mutable == true);
        uint etherAmountOLD = milestones[_milestoneID].etherAmount;
        uint tokenAmountOLD = milestones[_milestoneID].tokenAmount;
        milestones[_milestoneID].etherAmount = _etherAmount;
        milestones[_milestoneID].tokenAmount = _tokenAmount;
        milestones[_milestoneID].startTime = _startTime;
        milestones[_milestoneID].finishTime = _finishTime;
        milestones[_milestoneID].description = _milesoneDescription;
        milestones[_milestoneID].results = _milestoneResults;
        milestones[_milestoneID].status = MilestoneStatus(_status);
        if(_etherAmount > etherAmountOLD) {
            amountOfEth += _etherAmount - etherAmountOLD;
        }
        else {
            amountOfEth -= etherAmountOLD - _etherAmount;
        }
        
        if(_tokenAmount > tokenAmountOLD) {
            amountOfToken += _tokenAmount - tokenAmountOLD;
        }
        else {
            amountOfToken -= tokenAmountOLD - _tokenAmount;
        }
        
        
    }
    
    
    function bytes32ToStr(byte[50] _bytes32) public pure returns (string){

    // string memory str = string(_bytes32);
    // TypeError: Explicit type conversion not allowed from "bytes32" to "string storage pointer"
    // thus we should fist convert bytes32 to bytes (to dynamically-sized byte array)

    bytes memory bytesArray = new bytes(50);
    for (uint256 i; i < 50; i++) {
        bytesArray[i] = _bytes32[i];
        }
    return string(bytesArray);
    }



    // OK
    function deleteInvestContract() public  {
        uint index = investContractsIndices[msg.sender];
        require(index > 0);
        uint len = investContracts.length;
        investContracts[index-1] = investContracts[len-1];
        delete investContracts[len-1];
    }
    
    function transferTokensBack(uint _amount) public
    only(projectWallet) 
    {
        token.transfer(projectWallet, _amount);
    }
    
    // OK
    function ICOTokenBalance() public constant returns(uint) {
        return token.balanceOf(address(this));
    }
    
    // OK
    // This function calls by investor contract
    function depositedInvestContract(uint investEthAmount, uint investTokenAmount) public {
        require(maximumCap >= investEthAmount + investorEther);
        require(token.balanceOf(address(this)) >= investTokenAmount + investorTokens);
        uint index = pendingInvestContractsIndices[msg.sender];
        require(index > 0);
        uint len = pendingInvestContracts.length;
        InvestContract investContract = InvestContract(pendingInvestContracts[index-1]);
        pendingInvestContracts[index-1] = pendingInvestContracts[len-1];
        delete pendingInvestContracts[len-1];
        investContracts.push(address(investContract));
        investContractsIndices[address(investContract)]=(investContracts.length); //not that starts from 1
        uint tempEhterAmount = 0;
        uint tempTokenAmount = 0;
        uint _tokenAmount = investContract.tokenAmount();
        investorTokens += _tokenAmount;
        uint _etherAmount = investContract.etherAmount();
        investorEther += _etherAmount;
        for(uint i=0; i< milestones.length; i++) {
            tempEhterAmount += _etherAmount * milestones[i].etherAmount / amountOfEth;  
            tempTokenAmount += _tokenAmount * milestones[i].tokenAmount / amountOfToken;
            ethInMilestone[investContract].push(_etherAmount * milestones[i].etherAmount / amountOfEth);  
            tokenInMilestone[investContract].push(_tokenAmount * milestones[i].tokenAmount / amountOfToken);
            if(milestones.length - i == 1) { // last for
               ethInMilestone[investContract][i] += _etherAmount - tempEhterAmount;
               tokenInMilestone[investContract][i] += _tokenAmount - tempTokenAmount;
            }
        }
        token.transfer(msg.sender, investContract.tokenAmount()); 
    }

    function firstMilestoneDate() public constant returns(uint) {
       return  milestones[0].startTime;
    }

   
    // OK
    function closeMilestone(string _results) public  
    //only(projectWallet)
    {
        milestones[getCurrentMilestone()].status = MilestoneStatus.Checking; // Checking
        milestoneResult[getCurrentMilestone()] = _results;
    }
    
    // OK
    function startNextMileStone() public
    //only(projectWallet)
    {
        require(investorEther >= minimumCap);
        uint mileStone = getCurrentMilestone();
        require(milestones[mileStone].status == MilestoneStatus.Waiting);
        milestones[mileStone].status = MilestoneStatus.Active; 
        for(uint i=0; i< investContracts.length; i++) {
                InvestContract contractInvestor =  InvestContract(investContracts[i]); 
                contractInvestor.startMileStone(mileStone);
                //token.transfer(contractInvestor.investor(), tokenInMilestone[investContracts[i]][mileStone]); 
        }
        for(uint a=0; a< pendingInvestContracts.length; a++) {
            InvestContract pendingContractInvestor =  InvestContract(pendingInvestContracts[a]); 
            pendingContractInvestor.sendEthBack();
        }
    }

}

