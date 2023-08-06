
# AFEX SSO (DJANGO)




## simple integration (usage)

instantiate the SSO class


      from AFEX_SSO import SSO
      sso = SSO()

      def get_user_details(View):
        sso_instance = sso.check_credentials(sp_api_key, sp_hash_key, session_key)
        get_user = sso_instance['data'].get('user')
        '''
            # other codes
        '''
      
       def logout(View):
           # get user email
            email = " "
            signout = sso.sign_out(sp_api_key, sp_hash_key, session_key, email)
        '''
            # other codes
        '''

## Keys
    
- sp_api_key: service provider api key
- sp_hash_key : hashed key with api key ,secret key and an idempotency key (random values or timestamps)
- session_key : sent from the service provider client after successful authentication on the sso 

## SETTINGS

- set the sso url on settings.py as **SSO_URL**

    SSO_URL = ""

Sample Response

    {
    "responseCode": "100",
    "data": {
        "session_identifier": "SES_2c73ff51cfe5c5a68fc58934c9be3b",
        "user": {
            "email": "togunbiyi@afexnigeria.com"
        }
    },

    "message": "Successfully Retrieved"

    }


