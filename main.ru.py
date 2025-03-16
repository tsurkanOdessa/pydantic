from pydantic import BaseModel, EmailStr, Field, ValidationError, model_validator
import json

class Address(BaseModel):
    city: str = Field(...,
                      min_length=2,
                      description="city: строка, минимум 2 символа"
                      )
    street: str = Field(...,
                        min_length=3,
                        description="street: строка, минимум 3 символа."
                        )
    house_number: int = Field(...,
                              ge=1,
                              description="число, должно быть положительным"
                              )

class User(BaseModel):
    name: str = Field(...,
                      min_length=2,
                      max_length=120,
                      pattern=r'^[a-zA-ZА-Яа-яЁё\- ]+$',
                      description="строка, минимум 2 символа.")

    age: int = Field(...,
                     ge=0,
                     le=65,
                     description="число, должно быть между 0 и 65."
                     )
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode="before")
    def check_employment_status(cls, values):
        age = values.get('age')
        is_employed = values.get('is_employed')
        if is_employed and not (18 <= age <= 65):
            raise ValueError("возраст должен быть от 18 до 65 лет.")
        return values

def validate_and_serialize_user(json_str: str):
    try:
        user = User.model_validate_json(json_str)
        return user.model_dump_json(indent=4)
    except ValidationError as e:
        return json.dumps({"errors": e.errors()}, indent=4)

json_users = """[
    {
        "name": "Иван Смирнов",
        "age": 45,
        "email": "ivan.smirnov@gmail.com",
        "is_employed": true,
        "address": {
            "city": "Одесса",
            "street": "Александровский проспект",
            "house_number": 12
        }
    },
    {
        "name": "Елена Иванова",
        "age": 99,
        "email": "elena.ivanova@gmail.com",
        "is_employed": false,
        "address": {
            "city": "Николаев",
            "street": "проспект Мира",
            "house_number": 34
        }
    },
    {
        "name": "Сергей Петров",
        "age": 50,
        "email": "sergey.petrov@gmail.com",
        "is_employed": true,
        "address": {
            "city": "Новосибирск",
            "street": "Ленина",
            "house_number": 56
        }
    },
    {
        "name": "Марина Курц",
        "age": 99,
        "email": "marina.kurz@gmail.com",
        "is_employed": false,
        "address": {
            "city": "Екатеринбург",
            "street": "Малышева",
            "house_number": 78
        }
    },
    {
        "name": "А С",
        "age": 55,
        "email": "alexander.sokolov@gmail.com",
        "is_employed": true,
        "address": {
            "city": "Владивосток",
            "street": "Океанский проспект",
            "house_number": 90
        }
    }
]"""

users = json.loads(json_users)

for i, user in enumerate(users, 1):
    result = validate_and_serialize_user(json.dumps(user))
    print(f"\n🔹 Проверка пользователя"
          f" {i}:"
          f" result {result}:"
          f" {user['name']}")
