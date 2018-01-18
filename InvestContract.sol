pragma solidity ^0.4.18;
import "./ICOContract.sol";
import "./ERC20Token.sol";

contract InvestContract {
    address public projectWallet; // person from ico team
    address public investor;
    address[] public arbiters;
    uint public arbitersCount;
    uint countArbitersAccept;
    ICOContract public icoContract;
    Token public token;
    uint public needPay; // how many wei investor should pay with Jury.Online commission
    mapping(address => address) public arbitersSpare;
    mapping(address => uint) public arbitersIndices;
    mapping(address => uint) public spareArbitersIndeces;
    mapping(uint => uint) public countVotres;
    mapping(uint => string) public disputDescritions;   
    mapping(uint => bool) public milestones; // is complete? 
    mapping(uint => bool) public Disputes;
    mapping(uint => uint) public countVotes; // how many votes we have in each milestone
    mapping(uint => mapping(uint => uint)) public votes;  // milestone
    mapping(uint => mapping(address => address)) public arbitersVotes;
    mapping(uint => uint) public whoWin; // milestone => uint  1 - investor, 2 - ico
    mapping(uint => uint) public openDisputeDate; // nilestone => timestamp
    mapping(address => address) spareArbiters;
    mapping(address => uint) public arbitersAcccept;
    uint public etherAmount; 
    uint public tokenAmount; 

    
    modifier only(address _sender) {
        require(msg.sender == _sender);
        _;
    }

    modifier onlyArbiter() {
        require(arbitersAcccept[msg.sender] != 0);
        _;
    }
  
    function InvestContract(address _ICOContractAddress, address _investor,  uint
                           _etherAmount, uint _tokenAmount)
    public {
        icoContract = ICOContract(_ICOContractAddress);
        token = icoContract.token();
        projectWallet = icoContract.projectWallet();
        investor = _investor;
        arbitersCount = 5;
        // Arbiter1 0x111
        address arbiterAddress = 0x111;
        spareArbiters[0x1112] = arbiterAddress;
        arbitersSpare[arbiterAddress] = 0x1112;
        arbitersAcccept[arbiterAddress] = 1; // didn't accept
        arbiters.push(arbiterAddress);
        arbitersIndices[arbiterAddress] = arbiters.length;
        
        // Arbiter2
        arbiterAddress = 0x222;
        spareArbiters[0x2222] = arbiterAddress;
        arbitersSpare[arbiterAddress] = 0x2222;
        arbitersAcccept[arbiterAddress] = 1; // didn't accept
        arbiters.push(arbiterAddress);
        arbitersIndices[arbiterAddress] = arbiters.length;
        
        // Arbiter3
        arbiterAddress = 0x333;
        spareArbiters[0x3332] = arbiterAddress;
        arbitersSpare[arbiterAddress] = 0x3332;
        arbitersAcccept[arbiterAddress] = 1; // didn't accept
        arbiters.push(arbiterAddress);
        arbitersIndices[arbiterAddress] = arbiters.length;
        
        // Aribter4
        arbiterAddress = 0x444;
        spareArbiters[0x4442] = arbiterAddress;
        arbitersSpare[arbiterAddress] = 0x4442;
        arbitersAcccept[arbiterAddress] = 1; // didn't accept
        arbiters.push(arbiterAddress);
        arbitersIndices[arbiterAddress] = arbiters.length;
        
        // Arbiter5
        arbiterAddress = 0x555;
        spareArbiters[0x5552] = arbiterAddress;
        arbitersSpare[arbiterAddress] = 0x5552;
        arbitersAcccept[arbiterAddress] = 1; // didn't accept
        arbiters.push(arbiterAddress);
        arbitersIndices[arbiterAddress] = arbiters.length;
        
        etherAmount = _etherAmount;
        tokenAmount = _tokenAmount;
        needPay = etherAmount + etherAmount / 100 * icoContract.commission();
    }

    function () payable public
    //only(investor)
    { 
        //for(uint i=0; i< arbiters.length; i++) {
        //    require(arbitersAcccept[arbiters[i]] == 2);
        //}
        require(msg.value == etherAmount);
        require(getCurrentMilestone() == 0); //first
        require(getCurrentMilestoneStatus() == 0); // waiting
        checkALL();
    } 

    function InvestContractTokenBalance() public constant returns(uint) {
        return token.balanceOf(address(this));
    }
    
    function arbiterAcccept() public 
    //onlyArbiter 
    {
        arbitersAcccept[msg.sender] = 2;
        countArbitersAccept + 1;
        checkALL();
    }

    function getCurrentMilestone() public constant returns(uint) {
        return icoContract.getCurrentMilestone();
    }

    function getCurrentMilestoneStatus() public constant returns(uint) {
        return icoContract.getMilestoneStatus(getCurrentMilestone());
    }
    
    function vote(address _voteAdress) public
    //onlyArbiter 
    {   
        
        uint _milestone = getCurrentMilestone();
        require(Disputes[_milestone] == true);
        require(arbitersVotes[_milestone][msg.sender] == 0);
        if(arbitersIndices[msg.sender] > 0) {
        // msg.sender == Arbiter
            require(now >= openDisputeDate[_milestone] && now <= openDisputeDate[_milestone] + icoContract.voteArbiterDays() + icoContract.voteSpareArbiterDays());
            // if sparearbiter havn't voted yet
            require(arbitersVotes[_milestone][arbitersSpare[msg.sender]] == 0x0000000000000000000000000000000000000000);
        }
        else if(spareArbitersIndeces[msg.sender] > 0) {
        // msg.sender == spareArbiter
            require(now >= openDisputeDate[_milestone] + icoContract.voteArbiterDays() && now <= openDisputeDate[_milestone] + icoContract.voteArbiterDays() + icoContract.voteSpareArbiterDays());
            // if arbiter havn't voted yet
            require(arbitersVotes[_milestone][spareArbiters[msg.sender]] == 0x0000000000000000000000000000000000000000);
        }
        
        else {
            assert(false);
        }
        
        countVotres[_milestone] += 1;
        if(_voteAdress == projectWallet) {
            votes[_milestone][1] += 1;
        }
        if(_voteAdress == investor) {
            votes[_milestone][2] += 1;
        }
        arbitersVotes[_milestone][msg.sender] = _voteAdress;
        // we have all votes!
        if(countVotres[_milestone] == arbitersCount) {
            makedecision();
        }
    }

    function tokensInMilestone(uint _milestone) public constant returns(uint) {
        return icoContract.tokenInMilestone(address(this), _milestone);
    }

    function makedecision() internal {
        uint _milestone = getCurrentMilestone();
        require(countVotres[_milestone] == arbitersCount);
        if(votes[_milestone][1] > votes[_milestone][2]) {
            whoWin[_milestone] = 1; // icoContract
            // nothing to do
        }
        else {
            whoWin[_milestone] = 2; // investor
            investor.transfer(this.balance); // send back all eth! 
            //token.transfer(address(icoContract),InvestContractTokenBalance()); // send all tokens back
            token.transfer(0x0000000000000000000000000000000000000000,token.balanceOf(address(this)));
            icoContract.deleteInvestContract();
        }
    }

    function startMileStone(uint _milestone) public 
    //only(address(icoContract))
    {   
       
        projectWallet.transfer(icoContract.ethInMilestone(address(this), _milestone));
        token.transfer(investor, icoContract.tokenInMilestone(address(this),getCurrentMilestone())); 
    }


    /*
    // haven't done yet
    function checkArbitersAccepts() public {
       
        for(uint i=0; i< arbiters.length; i++) {
            if(arbitersAcccept[arbiters[i]] != 2) {
                arbiters[i] = spareArbiters[arbiters[i]];
            }
        }
    }
    */


    function openDispute(string _description) public 
    //only(investor)
    {
        uint _milestone = getCurrentMilestone();
        require(icoContract.isInvestorCanOpenDispute() == true);
        Disputes[_milestone] = true;
        disputDescritions[_milestone] = _description;
        openDisputeDate[_milestone] = now;
    }


    function checkALL() internal {
        require(getCurrentMilestoneStatus() == 0);
        require(getCurrentMilestone() == 0);
        if(countArbitersAccept == arbitersCount && this.balance > 0)  {
            icoContract.depositedInvestContract(etherAmount, tokenAmount);
            icoContract.JuryOnlineComission().transfer(etherAmount / 100 * icoContract.commission());
        }
    }


    function sendEthBack() public 
    // only(icoContract)
    {
        investor.transfer(this.balance);
    }
}

