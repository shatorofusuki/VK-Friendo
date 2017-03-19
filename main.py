import credentials
import vk_api

group_name = 'drug_prg'
posts_to_search = 500


def main():

    vk_session = vk_api.VkApi(credentials.login, credentials.password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    tools = vk_api.VkTools(vk_session)
    vk = vk_session.get_api()

    group_info = vk.groups.getById(group_id=group_name)
    group_id = group_info[0]['id']

    new_id = ('-' + str(group_id))
    # wall = tools.get_all('wall.get', 100, {'owner_id': new_id})

    left = posts_to_search
    off = 0
    fetch_at_a_time = 100

    while left > 0:
        _count = fetch_at_a_time if left > fetch_at_a_time else left
        left -= _count
        wall = vk.wall.get(owner_id=new_id, count=_count, offset=off)
        off += _count

        print('Fetched', len(wall['items']), 'posts...')

        for post in wall['items']:
            post_id = post['id']
            t = vk.likes.getList(type='post', owner_id=new_id, item_id=post_id, filter='likes', friends_only=1, extended='1')
            if t['count'] > 0:
                print("\nUser(s)", end="")
                for i in t['items'][:-1]:
                    print(i['first_name'], ' ', i['last_name'], ', ', sep='', end='')
                print(t['items'][-1]['first_name'], ' ', t['items'][-1]['last_name'], sep='')
                print('Liked this :', 'https://vk.com/wall'+str(new_id)+'_'+str(post_id))
                if len(post['text']):
                    print('Text:', post['text'])
                print('-------------------------------')
            else:
                print(".", end="", flush=True)


if __name__ == '__main__':
    main()
