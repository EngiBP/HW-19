import os
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_get_user_pets_with_valid_key(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_photo_of_pet_with_valid_data(pet_photo='images/belka.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception("There is no my pets")


def test_add_photo_of_pet_with_valid_data_format_png(pet_photo='images/belka.png'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 500
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_negative_age(name='Ron', animal_type='Заяц', age='-3', pet_photo='images/заяц.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    assert age not in result['age']
    assert int(age) < 0


def test_create_new_pet_with_invalid_format_Photo(name='Dosya', animal_type='ЁЖ', age='0', pet_photo='images/Ёж.txt'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_add_new_pet_with_valid_data(name='Дося', animal_type='ЁЖ', age='0', pet_photo='images/Ёж.jpg'):
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
        assert status == 200


def test_success_update_pet_info(name='Дося', animal_type='ЁЖ', age='0'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update.pet.info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['age'] == age
    else:
        raise Exception("There is no my pets")