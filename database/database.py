import pymongo as mdb
import datetime


class Database:
    def __init__(self):
        self.__client = mdb.MongoClient(
            "mongodb+srv://fdlbro:mo53RQKbzbmcBcEm@cluster0.rucjgyl.mongodb.net/"
        )
        self.__user = self.__client.hostel.users
        self.__rooms = self.__client.hostel.rooms
        self.__services = self.__client.hostel.services
        self.__products = self.__client.hostel.products
        
    def __is_admin(self, user_id: int) -> bool:
        if self.__user.find_one({'user_id': user_id}).get('admin'):
            return True
        else:
            return False

    def add_user(self, user_id: int) -> bool:
        base_info = {
            "user_id": user_id,
            "date": str(datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=3))).date()),
            "admin": False,
            "room": 0,
            "cash": 0
        }
        if self.__user.find_one({"user_id": user_id}):
            return False
        else:
            self.__user.insert_one(base_info)
            return True
        
    def add_room(self, room_number: int, room_price: int, user_id: int) -> bool:
        base_info = {
            "room_number": room_number,
            "usage": False,
            "user_id": user_id,
            "price": room_price
        }
        if self.__is_admin(user_id):
            if self.__rooms.find_one({"room_number": room_number}):
                return False
            else:
                self.__rooms.insert_one(base_info)
                return True
        else:
            return False
        
    
    def get_admin(self, user_id: int, admin_code: str) -> int:
        if admin_code == 'pbzbest':
            self.__user.update_one({"user_id": user_id}, {"$set": {"admin": True}})
            return True
        else:
            return False
        

    def add_cash(self, user_id: int, cash: int) -> bool:
        if self.__user.find_one({"user_id": user_id}):
            self.__user.update_one({"user_id": user_id}, {"$set": {"cash": self.__user.find_one({"user_id": user_id}).get("cash")+cash}})
            return True
        else:
            return False
        
    def list_rooms(self) -> str:
        rooms = self.__rooms.count_documents({"usage": False})
        if rooms != 0:
            room_array = []
            for i in range(1, rooms+1):
                room = self.__rooms.find_one({"usage": False, "room_number": i})
                room_array.append(f"\n Номер комнаты: {room.get('room_number')}, Стоимость: {room.get('price')}")
            return f"Доступные комнаты: \n{' '.join(room_array)}"
        else:
            return f"Нет доступных комнат"
        
    def get_room(self, user_id: int, room_number: int) -> int:
        room = self.__rooms.find_one({"room_number": room_number, "usage": False})
        availiability = self.__user.find_one({"user_id": user_id}).get("cash") >= room.get("price")

        if room and availiability:
            self.__rooms.update_one({"room_number": room_number}, {"$set": {"usage": True, "user_id": user_id}})
            self.__user.update_one({"user_id": user_id}, {"$set": {"room": room_number}})
            self.__user.update_one({"user_id": user_id}, {"$set": {"cash": self.__user.find_one({"user_id": user_id}).get("cash")-room.get("price")}})
            return 1
        elif not availiability:
            return 2
        else:
            return 0
    
    def leave_room(self, user_id: int) -> bool:
        room_number = self.__user.find_one({"user_id": user_id}).get("room")
        
        if room_number != 0:
            self.__rooms.update_one({"room_number": room_number}, {"$set": {"usage": False, "user_id": None}})
            self.__user.update_one({"user_id": user_id}, {"$set": {"room": 0}})
            return True
        else:
            return False

    def add_service(self, user_id: int, service_name: str, service_price: int) -> bool:
        service_info = {
            "service_name": service_name,
            "service_price": service_price,
            "available": True,
            "service_count": self.__services.count_documents({"available": True}) + 1
        }
        if self.__is_admin(user_id):
            if self.__services.find_one({"service_name": service_name}):
                return False
            else:
                self.__services.insert_one(service_info)
                return True
        else:
            return False

    def list_services(self) -> str:
        services = self.__services.count_documents({"available": True})
        if services != 0:
            service_array = []
            for i in range(0, services):
                service = self.__services.find_one({"service_count": i+1})
                service_array.append(f"\n Услуга: {service.get('service_name')}, Стоимость: {service.get('service_price')}")
            return f"Доступные услуги: \n{' '.join(service_array)}"
        else:
            return f"Нет доступных услуг"

    def get_service(self, user_id: int, service_name: str) -> int:
        service = self.__services.find_one({"service_name": service_name, "available": True})
        availiability = self.__user.find_one({"user_id": user_id}).get("cash") >= service.get("service_price")

        if service and availiability:
            self.__services.update_one({"service_name": service_name}, {"$set": {"available": False}})
            self.__user.update_one({"user_id": user_id}, {"$set": {"cash": self.__user.find_one({"user_id": user_id}).get("cash") - service.get("service_price")}})
            return 1
        elif not availiability:
            return 2
        else:
            return 0

    def add_product(self, user_id: int, product_name: str, product_price: int, product_count: int) -> bool:
        product_info = {
            "product_name": product_name,
            "product_price": product_price,
            "product_number": self.__products.count_documents({"product_available": True}) + 1,
            "product_available": True,
            "product_count": product_count
        }
        if self.__is_admin(user_id):
            if self.__products.find_one({"product_name": product_name}):
                if self.__products.find_one({"product_name": product_name}).get("product_count") == 0:
                    self.__products.update_one({"product_name": product_name}, {"$set": {"product_price": product_price}})
                    return True
            else:
                self.__products.insert_one(product_info)
                return True
        else:
            return False
    
    def list_products(self) -> str:
        products = self.__products.count_documents({"product_available": True})
        if products != 0:
            product_array = []
            for i in range(0, products):
                product = self.__products.find_one({"product_number": i+1})
                if product:
                    product_array.append(f"\n Продукт: {product.get('product_name')}, Стоимость: {product.get('product_price')}, Количество: {product.get('product_count')}")
            return f"Доступные продукты: \n{' '.join(product_array)}"
        else:
            return f"Нет доступных продуктов"

    def get_product(self, user_id: int, product_name: str, quantity: int) -> int:
        product = self.__products.find_one({"product_name": product_name})
        availiability = self.__user.find_one({"user_id": user_id}).get("cash") >= product.get("product_price") * quantity

        if product and availiability:
            self.__products.update_one({"product_name": product_name}, {"$inc": {"product_count": -quantity}})
            self.__user.update_one({"user_id": user_id}, {"$set": {"cash": self.__user.find_one({"user_id": user_id}).get("cash") - product.get("product_price") * quantity}})
            if self.__products.find_one({"product_name": product_name}).get("product_count") == 0:
                self.__products.update_one({"product_name": product_name}, {"$set": {"product_available": False}})
            return 1
        elif not availiability:
            return 2
        else:
            return 0