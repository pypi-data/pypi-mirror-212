from yattag import Doc


def generateNewHTML(userData, reposData, githubUserData):
    '''
    Generates a new HTML from user input

    Parameters
    ------------
        userData: user data
        reposData: projects data
        githubUserData: github user data
    '''

    # print(reposData[0])
    # print(reposData[0].name)

    # Create a new document
    doc, tag, text = Doc().tagtext()

    # Generate the HTML content
    doc.asis('<!DOCTYPE html>')
    with tag('html', lang='en'):
        with tag('head'):
            doc.stag('meta', charset='UTF-8')
            doc.stag('meta', http_equiv='X-UA-Compatible', content='IE=edge')
            doc.stag('meta', name='viewport',
                     content='width=device-width, initial-scale=1.0')
            with tag('script',
                     src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/js/all.min.js",
                     integrity="sha512-6PM0qYu5KExuNcKt5bURAoT6KCThUmHRewN3zUFNaoI6Di7XJPTMoT6K0nsagZKk2OB4L7E3q1uQKHNHd4stIQ==",
                     crossorigin="anonymous",
                     referrerpolicy="no-referrer"):
                pass
            doc.stag('link', rel='stylesheet',
                     href='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css')
            with tag('script', src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'):
                pass
            with tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js'):
                pass
            with tag('script', src='https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js'):
                pass

            doc.stag('link', rel='preconnect',
                     href='https://fonts.googleapis.com')
            doc.stag('link', rel='preconnect',
                     href='https://fonts.gstatic.com', crossorigin='')
            doc.stag(
                'link', href='https://fonts.googleapis.com/css2?family=ABeeZee&display=swap', rel='stylesheet')
            doc.stag(
                'link', href='https://fonts.googleapis.com/css2?family=Nunito&display=swap', rel='stylesheet')
            doc.stag('link', rel='stylesheet',
                     href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css')

            with tag('script',
                     src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
                     integrity='sha384-geWF76RCwLtnZ8qwWowPQNguL3RmwHVBC9FhGdlKrxdiJJigb/j/68SIy3Te4Bkz',
                     crossorigin='anonymous'):
                pass
            with tag('script',
                     src='https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js',
                     integrity='sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r',
                     crossorigin='anonymous'):
                pass
            with tag('script',
                     src='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js',
                     integrity='sha384-fbbOQedDUMZZ5KreZpsbe1LCZPVmfTnH7ois6mU1QK+m14rQ1l2bGBq41eYeM/fS',
                     crossorigin='anonymous'):
                pass
            with tag('title'):
                text('My portfolio')

        with tag('body'):
            # Navbar
            with tag('nav', klass='navbar navbar-expand-sm bg-dark navbar-dark sticky-top', id='navbar'):
                with tag('a', klass='navbar-brand', href='#jumbotron'):
                    text(userData['name'])

                with tag('ul', klass='navbar-nav'):
                    with tag('li', klass='nav-item'):
                        with tag('a', klass='nav-link', href='#about-section'):
                            text('About')
                    with tag('li', klass='nav-item'):
                        with tag('a', klass='nav-link', href='#projects-section'):
                            text('Projects')
                    with tag('li', klass='nav-item'):
                        with tag('a', klass='nav-link', href='#contact-section'):
                            text('Contact')

            # Jumbotron
            with tag('div', klass='jumbotron jumbotron-fluid', style='margin-bottom: 0', id='jumbotron'):
                with tag('div', klass='d-flex align-items-center justify-content-center'):
                    # Profile Photo
                    with tag('div', klass='col-lg-4 d-flex align-items-center justify-content-center flex-wrap'):
                        doc.stag('img',
                                 src=githubUserData['profilePic'],
                                 alt='GitHub profile photo',
                                 klass='',
                                 style='width: 200px; height: 200px; border-radius: 50%')
                        with tag('div', klass='d-flex flex-column align-items-center justify-content-center'):
                            with tag('h1'):
                                text(userData['name'])
                            with tag('h2'):
                                text("Github: " + githubUserData['username'])

                            if githubUserData['bio'] != None:
                                with tag('p', style='padding-left: 10px; padding-right: 10px'):
                                    text(githubUserData['bio'])

            # About
            with tag('div', klass='row d-flex align-items-center justify-content-center', id='about-section'):
                # with tag('div', klass='col-sm-6'):
                #     doc.stag('img',
                #              src='https://picsum.photos/600/600',
                #              klass='card-img-top',
                #              alt='...',
                #              height='300px')
                with tag('div', klass='col-sm-6'):
                    with tag('div', style='padding: 20px'):
                        with tag('h2'):
                            text('About')
                        with tag('p'):
                            text(userData['about'])

            doc.stag('br')

            # Projects
            with tag('div', klass='container', id='projects-section'):
                with tag('div', klass='col text-center'):
                    with tag('h2'):
                        text('Projects')
                doc.stag('br')

                with tag('div', klass='row text-center d-flex align-items-center justify-content-center'):
                    for i in range(len(reposData)):
                        # print(reposData[i])
                        if reposData[i]["display"] == True:
                            with tag('div', klass='col-lg-4', style='padding: 10px'):
                                # doc.stag('img',
                                #          src='https://picsum.photos/140/140',
                                #          klass='card-img-top',
                                #          style='width: 140px; height: 140px; border-radius: 50%',
                                #          alt='...')
                                with tag('h3', klass='fw-normal'):
                                    text(reposData[i]["name"])
                                if reposData[i]["about"] != None:
                                    with tag('p'):
                                        text(reposData[i]["about"])
                                with tag('p'):
                                    with tag('a', klass='btn btn-secondary', href=reposData[i]["url"], target='_blank'):
                                        text('View details')

            doc.stag('br')

            # Footer
            with tag('footer'):
                with tag('div', klass='bg-dark text-white'):
                    with tag('div', klass='container', style='padding: 20px'):
                        with tag('div', klass='row', id='contact-section'):
                            with tag('div', klass='col-md-4'):
                                with tag('h3'):
                                    text('Contact')
                                with tag('p'):
                                    text(
                                        'Thanks for visiting my portfolio. Feel free to contact me.')
                            with tag('div', klass='col-md-4'):
                                with tag('p'):
                                    text('Email: ')
                                    with tag('a', href='mailto:' + userData['email']):
                                        text(userData['email'])
                                with tag('p'):
                                    text('Phone: ' + userData['phone'])
                            with tag('div', klass='col-md-4'):
                                with tag('h3'):
                                    text('Social Media')
                                with tag('a', klass='btn btn-outline-light', href=githubUserData['url']):
                                    with tag('i', klass='fab fa-github'):
                                        pass
                                if userData['socialMedia']['twitter'] != None and userData['socialMedia']['twitter'] != "":
                                    with tag('a', klass='btn btn-outline-light', href='https://twitter.com/' + userData['socialMedia']['twitter']):
                                        with tag('i', klass='fab fa-twitter'):
                                            pass
                                if userData['socialMedia']['facebook'] != None and userData['socialMedia']['facebook'] != "":
                                    with tag('a', klass='btn btn-outline-light', href=userData['socialMedia']['facebook']):
                                        with tag('i', klass='fab fa-facebook'):
                                            pass
                                if userData['socialMedia']['instagram'] != None and userData['socialMedia']['instagram'] != "":
                                    with tag('a', klass='btn btn-outline-light', href=userData['socialMedia']['instagram']):
                                        with tag('i', klass='fab fa-instagram'):
                                            pass

    # Save the HTML code to a file
    with open('index.html', 'w') as file:
        file.write(doc.getvalue())


# # Test
# if __name__ == '__main__':
#     userData = {
#         'name': 'John Doe',
#         'email': 'johnDoe@gmail.com',
#         'phone': '(123) 456-7890',
#         'about': 'I am a web developer with experience in HTML, CSS, JavaScript, and PHP. I am passionate about creating beautiful and functional websites.',
#         'socialMedia': {
#             'twitter': 'https://twitter.com/',
#             'facebook': 'https://www.facebook.com/',
#             'instagram': 'https://www.instagram.com/'
#         }
#     }

#     reposData = [
#         {
#             'name': 'Project 1',
#             'about': 'This is a project.',
#             'url': 'https://bard.google.com/',
#             'display': True
#         },
#         {
#             'name': 'Project 2',
#             'about': 'This is a project.',
#             'url': 'https://bard.google.com/',
#             'display': False
#         },
#         {
#             'name': 'Project 3',
#             'about': 'This is a project.',
#             'url': 'https://bard.google.com/',
#             'display': True
#         },
#         {
#             'name': 'Project 4',
#             'about': 'This is a project.',
#             'url': 'https://bard.google.com/',
#             'display': False
#         },
#         {
#             'name': 'Project 5',
#             'about': 'This is a project.',
#             'url': 'https://bard.google.com/',
#             'display': True
#         },
#         {
#             'name': 'Project 6',
#             'about': 'This is a project.',
#             'url': 'https://bard.google.com/',
#             'display': True
#         }

#     ]

#     githubUserData = {
#         'username': 'JohnDoeGithub',
#         'profilePic': 'https://avatars.githubusercontent.com/u/8?v=4',
#         'bio': 'An aspiring web developer.',
#     }


#     generateNewHTML(userData, reposData, githubUserData)