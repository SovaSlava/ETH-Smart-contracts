pragma solidity ^0.4.16;


library SafeMath {
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a * b;
        assert(a == 0 || c / a == b);
        return c;
    }

    function div(uint256 a, uint256 b) internal  pure returns (uint256) {
    // assert(b > 0); // Solidity automatically throws when dividing by 0
        uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold
        return c;
    }

    function sub(uint256 a, uint256 b) internal  pure returns (uint256) {
        assert(b <= a);
        return a - b;
    }

    function add(uint256 a, uint256 b) internal pure  returns (uint256) {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }
}


contract Base {
    modifier only(address allowed) {
        require(msg.sender == allowed);
        _;
    }
}


contract Owned is Base {

    address public owner;
    address public newOwner;
    event OwnershipTransferred(address indexed _from, address indexed _to);

    function Owned() public {
        owner = msg.sender;
    }

    function transferOwnership(address _newOwner) public only(owner) {
        owner = _newOwner;
    }

    function acceptOwnership() public only(newOwner) {
        OwnershipTransferred(owner, newOwner);
        owner = newOwner;
    }

}


contract ERC20 is Owned {
    using SafeMath for uint;

    event Transfer(address indexed _from, address indexed _to, uint _value);
    event Approval(address indexed _owner, address indexed _spender, uint _value);

    function transfer(address _to, uint _value) public returns (bool success) {
        require(_to != address(0));
        require(_value <= balances[msg.sender]);

        // SafeMath.sub will throw if there is not enough balance.
        balances[msg.sender] = balances[msg.sender].sub(_value);
        balances[_to] = balances[_to].add(_value);
        Transfer(msg.sender, _to, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint _value) public returns (bool success) {
        require(_to != address(0));
        require(_value <= balances[_from]);
        require(_value <= allowed[_from][msg.sender]);

        balances[_from] = balances[_from].sub(_value);
        balances[_to] = balances[_to].add(_value);
        allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);
        Transfer(_from, _to, _value);
        return true;
    }

    function balanceOf(address _owner) public constant  returns (uint balance) {
        return balances[_owner];
    }

    function approve_fixed(address _spender, uint _currentValue, uint _value) public returns (bool success) {
        if (allowed[msg.sender][_spender] == _currentValue) {
            allowed[msg.sender][_spender] = _value;
            Approval(msg.sender, _spender, _value);
            return true;
        } else {
            return false;
        }
    }

    function approve(address _spender, uint _value) public returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        Approval(msg.sender, _spender, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public constant returns (uint remaining) {
        return allowed[_owner][_spender];
    }

    mapping (address => uint) public balances;
    mapping (address => mapping (address => uint)) public allowed;

    uint public totalSupply;
}


contract FreeToken is ERC20 {
    using SafeMath for uint;

    string public name;
    string public symbol;
    uint public decimals;
    uint public lastMint;
    uint public needWei;

    function FreeToken(string _name, string _symbol, uint8 _decimals) public {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        lastMint = now;
        needWei = 100;
    }

    function getTotalSupply()
    public
    constant
    returns(uint)
    {
        return totalSupply;
    }

    function getFreeToken() public payable
    {
        require(now - lastMint >= 1 hours);
        require(msg.value == needWei);
        lastMint = now;
        needWei += 100;
        totalSupply = totalSupply.add(1);
        balances[msg.sender] = balances[msg.sender].add(1);
        if (!msg.sender.send(msg.value)) {
            owner.send(msg.value);
        }
    }

}
