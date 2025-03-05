from .user import User, add_new_user
from .post import Post, add_new_post
from .comment import Comment, add_new_comment
from .like import Like, add_new_like
from .session import Session, add_new_session

def create_default_data():
    user1 = add_new_user('jeremy', 'X23$jer', 'https://images.pexels.com/photos/30495756/pexels-photo-30495756/free-photo-of-rustic-wooden-chairs-in-lush-antalya-field.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')
    user2 = add_new_user('andy', 'CoolAndy99+', 'https://images.pexels.com/photos/30892987/pexels-photo-30892987/free-photo-of-delicious-pancakes-with-honey-and-strawberries.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')
    user3 = add_new_user('sandman', 'SandmanIsCool22++', 'https://images.pexels.com/photos/5846133/pexels-photo-5846133.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')

    post1 = add_new_post(user1, 'https://images.pexels.com/photos/30495756/pexels-photo-30495756/free-photo-of-rustic-wooden-chairs-in-lush-antalya-field.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 'This is a beautiful field.')
    post2 = add_new_post(user2, 'https://images.pexels.com/photos/30892987/pexels-photo-30892987/free-photo-of-delicious-pancakes-with-honey-and-strawberries.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 'Yummy pancakes!')
    post3 = add_new_post(user3, 'https://images.pexels.com/photos/5846133/pexels-photo-5846133.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2', 'A cool photo.')

    comment1 = add_new_comment(post1, user2, 'Nice photo!')
    comment2 = add_new_comment(post1, user3, 'Beautiful!')
    comment3 = add_new_comment(post2, user1, 'Looks delicious!')
    comment4 = add_new_comment(post3, user2, 'Cool photo!')
    comment5 = add_new_comment(post3, user1, 'Nice!')

    like1 = add_new_like(post1, user2)
    like2 = add_new_like(post1, user3)
    like3 = add_new_like(post2, user1)
