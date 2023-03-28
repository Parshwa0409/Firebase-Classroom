import ascii_art
import GUI2_LOGIN_SCREEN
import GUI2_REGISTER_SCREEN

print(ascii_art.logo)

user_choice = int(input('1) Already A Registered User ,Sign-In.\n2) Not A User ,Register.\nEnter Your Choice (1/2) : '))
if user_choice == 1:
    GUI2_LOGIN_SCREEN.main()
elif user_choice == 2:
    GUI2_REGISTER_SCREEN.main()
else:
    print('Invalid Choice')
