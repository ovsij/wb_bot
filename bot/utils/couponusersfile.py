
def create_file(db_request, coupon_id : int):
    coupon = db_request.get_coupon(id=coupon_id)
    users = [f'Список пользователей, использовавших купон {coupon.name}: \n\n']
        
    for user in db_request.get_user(coupon_id=coupon_id):
        user_str = f'- '
        if user.username:
            user_str += f'@{user.username} | '
        else:
            user_str += f'{user.tg_id} | '
        if user.first_name:
            user_str += f'{user.first_name} '
        if user.last_name:
            user_str += f'{user.last_name}'
        user_str += '\n'
        users.append(user_str)
    with open('users.txt', 'w') as file:
        for line in users:
            file.write(line)
    return 'users.txt'
                