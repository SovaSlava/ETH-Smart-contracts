from database import db_session
from models.users import User
u = User('admin', '123','123secret',1)
db_session.add(u)
db_session.commit()


print(str(User.query.all()))
#[<User u'admin'>]
#>>> User.query.filter(User.name == 'admin').first()
#<User u'admin'>
