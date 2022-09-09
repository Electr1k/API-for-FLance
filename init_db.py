from models import *
#data = {
#    "item": ["Кофе", "Печеньки"],
#    "price": [100, 250]
#}
#for i in range(0,5):
#    setattr(EstablishmentsFullInfo.query.filter_by(id=i).first(), 'prices', data)
#    db.session.commit()
#print(EstablishmentsFullInfo.query.all()[0].booking)
users = Users.query.all()
for user in users:
    print("=========User======")
    print("Name :", user.name, "Surname: ", user.surname)
    print("Email: ", user.email, "Password: ", user.password)
    print("Booking: ", user.booking)
# обнова дат для брони
#data = {'data': ['07.09', '08.09', '09.09', '10.09', '11.09', '12.09', '13.09'], '07.09': [0, 1, 2, 3, 4, 5, 6, 7, 21, 22, 23], '08.09': [0, 1, 2, 3, 4, 5, 6, 7, 21, 22, 23], '09.09': [0, 1, 2, 3, 4, 5, 6, 7, 21, 22, 23], '10.09': [0, 1, 2, 3, 4, 5, 6, 7, 21, 22, 23], '11.09': [0, 1, 2, 3, 4, 5, 6, 7, 21, 22, 23], '12.09': [0, 1, 2, 3, 4, 5, 6, 7, 21, 22, 23], '13.09': [0, 1, 2, 3, 4, 5, 6, 7, 21, 22, 23]}
#est = Establishments.query.all()[4]
#setattr(est, "address", "Пер. Тургеневский, 2А")

#db.session.commit()
#ests = EstablishmentsFullInfo.query.all()
#for esr in ests:
#    setattr(esr, "booking", data)
#db.session.commit()
#ests = EstablishmentsFullInfo.query.all()
#for est in ests:
#    print(f'======{est.name}======')
#    print(est.booking)