pragma solidity ^0.4.13; 

contract FamilyBudget {
    

    uint bigPrice; // Сумма транзакции, превысив которую, транзакция должна быть одобрена двумя членами семьи 
    uint wishId = 0;
    uint[] wishIds;
    event newPurchase(uint amount, uint time);
    
    mapping(address => uint) family; // адрес => timestamp последнего действия (для отслеживания активности)
    struct Wish {
        address owner;
        string name;
        uint amount;
        uint vote;
        address to;
    }
    
    mapping(uint => Wish) Wishes;
    
    function FamilyBudget(address person2, uint _bigPrice) {
        family[msg.sender] = block.timestamp;
        family[person2] = block.timestamp;
        bigPrice = _bigPrice;
    }
    
    modifier onlyFamily() {
        require(family[msg.sender] != 0);
        _;
    }
    
    function() payable { } // Принимаем эфир от всех :)
    
    function getBalance() constant onlyFamily returns(uint) {
        return this.balance;
    }
    
    
    function addWish(string _name, uint _amount, address _address) onlyFamily {
        wishId++;
        wishIds.push(wishId);
        Wishes[wishId].owner = msg.sender;
        Wishes[wishId].name = _name;
        Wishes[wishId].amount = _amount;
        Wishes[wishId].to = _address;
        Wishes[wishId].vote = 1; //Голосуем за свою покупку
    }
    
    function getWishIds() onlyFamily returns(uint[]) {
        return wishIds;
    }
    
    function getWishById(uint _id) onlyFamily returns(address, string, uint, uint, address) {
        return (Wishes[_id].owner,
                Wishes[_id].name,
                Wishes[_id].amount,
                Wishes[_id].vote,
                Wishes[_id].to
                );
    }
    
    function vote(uint whishId, bool decision) onlyFamily returns(bool) {
        require(msg.sender == Wishes[whishId].owner); //Нельзя голосовать за свою покупку
        if(decision == true && Wishes[wishId].vote == 1) {
            if(Wishes[wishId].to.send(Wishes[wishId].amount)) {
                //отправка прошла успешна
                newPurchase(Wishes[wishId].amount, block.timestamp);
                return true;
            }
            else { return false;  } 
        }
        //втоорой голос - против, поэтому удаляем 
        deleteWish(wishId);
        return false;
    }
    
    function deleteWish(uint _id) onlyFamily {
        delete Wishes[_id];
        uint i = 0;
        while (wishIds[i] != _id) {
            i++;
        }
        delete wishIds[i];
    }
    
    function buy(uint amount, string name, address _address) onlyFamily returns(bool) {
        if(amount > bigPrice) {
            //Сумма покупки больше чем bigPrice-значение, поэтому добавляем в WishList
            addWish(name, amount, _address);
            }
        else {
            require(block.timestamp > (3 hours + family[msg.sender]));
            if(_address.send(amount) == true) {
                newPurchase(Wishes[wishId].amount, block.timestamp);
                //обновляем время последней покупки
                family[msg.sender] = block.timestamp;
                return true;
            }
        }
        
    }
    
    function kill() onlyFamily {
        uint amount = this.balance / 2;
        msg.sender.send(amount);
        delete family[msg.sender];
        
    }
 
    
    
}
