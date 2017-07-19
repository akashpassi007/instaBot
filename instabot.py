import requests

import urllib

from textblob import TextBlob

from textblob.sentiments import NaiveBayesAnalyzer

from termcolor import colored
from wordcloud import WordCloud

APP_ACCESS_TOKEN = '5710428978.f0d4dae.3aee0fd5dc794aba91e3faf4db31117c'

tags = []

BASE_URL = 'https://api.instagram.com/v1/'

def self_info():

    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)

    print 'GET request url : %s' % (request_url)

    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if len(user_info['data']):

            print 'Username: %s' % (user_info['data']['username'])

            print 'Number of followers: %s' % (user_info['data']['counts']['followed_by'])

            print 'Number of people you are following: %s' % (user_info['data']['counts']['follows'])

            print 'Number of posts: %s' % (user_info['data']['counts']['media'])

        else:

            print colored('User does not exist!','red')

    else:

        print colored('Error due to Status code other than 200 received!','red')


# Function for getting the ID of a user


def get_user_id(insta_username):

    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)

    print 'GET request url : %s' % (request_url)

    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:

        if len(user_info['data']):

            return user_info['data'][0]['id']
        else:

            return None
    else:
        print 'Status code other than 200 received!'
        exit()

'''
Function declaration to get the information of a user by username
'''

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!', 'red')
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'Number of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'Number of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'Number of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print colored('---There is no data for this user!---', 'red')
    else:
        print colored('---Status code other than 200 received!---', 'red') #error in code


'''
Function declaration to get your recent post
'''

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded!','green')
        else:
            print colored('Post does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')


'''
Function declaration to get the recent post of a user by username
'''


def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored(' This User does not exist!','red')
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded!','green')
        else:
            print colored('Post does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')


'''
Function declaration to get post id
'''

def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print colored('There is no recent post of the user!','red')
    else:
        print colored('Status code other than 200 received!','red')
        exit()

'''
Function declaration to get list of users had liked  post
'''


def get_like_list(insta_username):

    # Getting post id by passing the username .......

    media_id = get_post_id(insta_username)
    request_url = BASE_URL + 'media/%s/likes?access_token=%s' % (media_id, APP_ACCESS_TOKEN)
    print colored('GET request url : %s', 'blue') % (request_url)
    like_list = requests.get(request_url).json()

    if like_list['meta']['code'] == 200:  # checking the status code .....
        if len(like_list['data']):
            position = 1
            print colored("List of people who Liked Your Recent post", 'blue')
            for users in like_list['data']:
                if users['username']!= None:
                    print position, colored(users['username'],'green')
                    position = position + 1
                else:
                    print colored('No one had liked Your post!', 'red')
        else:
            print colored("User Does not have any post",'red')
    else:
        print colored('Status code other than 200 recieved', 'red')



def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print colored('Like was successful!','green')
    else:
        print colored('Your like was unsuccessful. Try again!','red')



def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input(colored("Your comment: ",'blue'))
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print colored("New comment is Successfully added!",'green')
    else:
        print colored("Unable to Add comment. Try again!",'red')



def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print colored('Comment successfully deleted!','green')
                    else:
                        print colored('Unable to delete comment!','red')
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print colored('There are no existing comments on the post!','red')
    else:
        print colored('Status code other than 200 received!','red')


def get_caption(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print
        'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print
    'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            for i in user_media['data']:
                tags.append(i['tags'])
            matplot()
        else:
            print 'no media'
    else:
        print 'status code other than 200'


def matplot():
    l=[]
    for i in tags:
        l.append((" ").join(i))
    words = (" ").join(l)
    wordcloud = WordCloud(mask=mask,
                          stopwords=STOPWORDS,
                          background_color='white',
                          width=1800,
                          height=1400
                          ).generate(words)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

def start_bot():

    while True:

        print '\n'

        print colored('Hello! Welcome to Insabot','blue')

        print colored('Menu:','blue')

        print colored("1.) Get your own details.",'yellow')

        print colored("2.) Get your own recent post.",'yellow')

        print colored("3.) Get details of a user by username.", 'yellow')

        print colored("4.) Get the recent post of a user by username.",'yellow')

        print colored("5.) Get a list of people who have liked the recent post of a user", 'yellow')

        print colored("6.) Like the recent post of a User", 'yellow')

        print colored("7.) Make a comment on the recent post of a user", 'yellow')

        print colored("8.) Delete negative comments from the recent post of a user", 'yellow')

        print colored("9.) Exit", 'yellow')

        choice=raw_input(colored("Enter choice: ",'blue'))

        if choice=="1":

            self_info()

        elif choice=="2":

            get_own_post()

        elif choice == "3":

            insta_username = raw_input(colored("Enter Username of the User: ", 'green'))
            get_user_info(insta_username)

        elif choice == "4":

            insta_username = raw_input(colored("Enter Username of the User: ",'green'))
            get_user_post(insta_username)

        elif choice=="5":

            insta_username = raw_input(colored("Enter Username of the user: ",'green'))
            get_like_list(insta_username)

        elif choice=="6":

            insta_username = raw_input(colored("Enter Username of the user: ",'green'))
            like_a_post(insta_username)

        elif choice =="7":

            insta_username =raw_input(colored("Enter Username of the user: ",'green'))
            post_a_comment(insta_username)

        elif choice=="8":

            insta_username = raw_input(colored("Enter Username of the user: ",'green'))
            delete_negative_comment(insta_username)

        elif choice=="9":

            exit()
        else:
            print colored("You have entered a wrong choice", 'red')  #selected choice is wrong

start_bot()
